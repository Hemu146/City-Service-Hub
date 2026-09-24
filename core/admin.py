from django.contrib import admin
from .models import Users,ServiceProvider, Services,Service
# Register your models here.
@admin.register(Users)
class UsersCus(admin.ModelAdmin):
    list_display=('id','name','email','phone','adress')
    search_fields=('name','email','phone')
    list_filter=['name']

@admin.register(ServiceProvider)
class ServiceProviderCus(admin.ModelAdmin):
    list_display=('id','name','email','phone','address','password')
    search_fields=('name','email','phone','id')
    list_filter=['name']


@admin.register(Services)
class ServicesCus(admin.ModelAdmin):
    list_display=('id','service_name')
    search_fields=('service_name','id')
    list_filter=['service_name']
    filter_horizontal=['providers']


@admin.register(Service)
class ServiceCus(admin.ModelAdmin):
    list_display=('id','SERVICE_TYPES','name','type','description','address','phone','open_time','close_time')

    search_fields=('SERVICE_TYPES','provider','name','type','address','open_time','close_time')
    
    list_filter=['type','provider']
    