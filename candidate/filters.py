from employer.models import Jobs
import django_filters
class JobFilterCandidate(django_filters.FilterSet):
    location = django_filters.CharFilter(lookup_expr='contains')
    Designation=django_filters.CharFilter(lookup_expr='contains')
    skills=django_filters.CharFilter(lookup_expr='contains')
    class Meta:
        model=Jobs
        fields=["location","Designation","skills"]

