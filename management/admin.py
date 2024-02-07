from django.contrib import admin
from .models import ClientCategory, SampleForm, Commodity, CommodityCategory


admin.site.register(ClientCategory)
admin.site.register(SampleForm)
admin.site.register(Commodity)
admin.site.register(CommodityCategory)
