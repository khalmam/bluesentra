"""Spatial smoke test (ADR-017): proves PostGIS works and coordinate order is lon, lat."""

import json

import pytest
from django.db import connection

pytestmark = [pytest.mark.spatial, pytest.mark.django_db]


def test_point_round_trips_as_geojson_in_lon_lat_order():
    longitude, latitude = 3.4219, 6.4281  # Lagos coast: lon, lat
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT ST_AsGeoJSON(ST_SetSRID(ST_MakePoint(%s, %s), 4326))",
            [longitude, latitude],
        )
        geojson = json.loads(cursor.fetchone()[0])

    assert geojson["type"] == "Point"
    assert geojson["coordinates"] == [longitude, latitude]
