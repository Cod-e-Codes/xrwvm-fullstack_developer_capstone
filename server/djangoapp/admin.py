from django.contrib import admin
from .models import CarMake, CarModel

# Inline to manage CarModel from CarMake admin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# Admin classes
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year', 'dealer_id')

# Register models
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
