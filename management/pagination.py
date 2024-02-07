from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = "limit" #upto data
    offset_query_param = "offset" #which page
    max_limit = 500

class PageNumberPagination(PageNumberPagination):
    page_size = 20  # Set your desired page size
    page_size_query_param = 'limit'
    max_page_size = 500  # Set the maximum page size