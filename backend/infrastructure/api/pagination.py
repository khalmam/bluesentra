"""Standard pagination (ADR-023).

Page-number pagination, default 25 and maximum 100. Pagination details
are returned in the envelope's ``meta`` field.
"""

from typing import Any

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EnvelopePagination(PageNumberPagination):
    """Page-number pagination that returns the standard envelope."""

    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: Any) -> Response:
        page = self.page
        assert page is not None  # set by paginate_queryset
        return Response(
            {
                "success": True,
                "data": data,
                "meta": {
                    "pagination": {
                        "count": page.paginator.count,
                        "page": page.number,
                        "page_size": page.paginator.per_page,
                        "total_pages": page.paginator.num_pages,
                        "next": self.get_next_link(),
                        "previous": self.get_previous_link(),
                    }
                },
            }
        )
