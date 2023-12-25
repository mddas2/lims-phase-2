from rest_framework.pagination import LimitOffsetPagination

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 500 #max-limit set

