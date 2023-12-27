from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 500 #max-limit set

class PageNumberPagination(PageNumberPagination):
    page_size = 10  # Set your desired page size
    page_size_query_param = 'limit'
    max_page_size = 500  # Set the maximum page size
  

