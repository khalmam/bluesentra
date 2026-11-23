"""Tests for the response envelope, error handler and pagination (ADR-013, ADR-023)."""

import json

from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from infrastructure.api.pagination import EnvelopePagination

factory = APIRequestFactory()


class OkView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"name": "Lekki"})


class GeoJSONView(APIView):
    permission_classes = [AllowAny]
    raw_geojson = True

    def get(self, request):
        return Response({"type": "FeatureCollection", "features": []})


class InvalidView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        raise ValidationError({"latitude": ["This field is required."]})


class MissingView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        raise NotFound("No such zone.")


def call(view_cls):
    response = view_cls.as_view()(factory.get("/x"))
    response.render()
    return response, json.loads(response.content)


def test_success_is_wrapped_in_envelope():
    response, body = call(OkView)
    assert response.status_code == 200
    assert body == {"success": True, "data": {"name": "Lekki"}, "meta": {}}


def test_geojson_endpoint_is_not_wrapped():
    _, body = call(GeoJSONView)
    assert body == {"type": "FeatureCollection", "features": []}


def test_validation_error_uses_error_envelope():
    response, body = call(InvalidView)
    assert response.status_code == 400
    assert body["success"] is False
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["details"] == {"latitude": ["This field is required."]}


def test_not_found_keeps_status_and_uses_error_envelope():
    response, body = call(MissingView)
    assert response.status_code == 404
    assert body["error"] == {"code": "not_found", "message": "No such zone.", "details": {}}


def test_pagination_defaults_and_meta():
    paginator = EnvelopePagination()
    assert paginator.page_size == 25
    assert paginator.max_page_size == 100


def test_pagination_response_contains_meta():
    request = factory.get("/items/?page=1&page_size=2")
    from rest_framework.request import Request

    drf_request = Request(request)
    paginator = EnvelopePagination()
    page_items = paginator.paginate_queryset(list(range(5)), drf_request)
    response = paginator.get_paginated_response(page_items)
    assert response.data["success"] is True
    assert response.data["data"] == [0, 1]
    pagination = response.data["meta"]["pagination"]
    assert pagination["count"] == 5
    assert pagination["page_size"] == 2
    assert pagination["total_pages"] == 3
