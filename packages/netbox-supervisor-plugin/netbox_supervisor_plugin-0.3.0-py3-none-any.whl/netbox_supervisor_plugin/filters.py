import django_filters
from django.db.models import Q

from utilities.filters import TreeNodeMultipleChoiceFilter
from tenancy.models import Tenant
from .models import Supervisor


class NameSlugSearchFilterSet(django_filters.FilterSet):
    """
    A base class for adding the search method to models which only expose the `name` and `slug` fields
    """
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(slug__icontains=value)
        )


class SupervisorFilter(NameSlugSearchFilterSet):
    q = django_filters.CharFilter(
        method="search",
        label="Поиск",
    )

    class Meta:
        model = Supervisor
        fields = [
            'status',
            'email',
            'phone',
            'tenant',
            'tenants',
            'comments',
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset

        qs_filter = (
            Q(sid__icontains=value)
            | Q(name__icontains=value)
            | Q(status__icontains=value)
            | Q(comments__icontains=value)
            | Q(email__icontains=value)
            | Q(phone__icontains=value)
        )

        return queryset.filter(qs_filter)
