from django_filters import rest_framework as filters
from .models import Post


class PostFilter(filters.FilterSet):
    text = filters.CharFilter(field_name="group__id", lookup_expr='exact')

    class Meta:
        model = Post
        fields = ['text']
