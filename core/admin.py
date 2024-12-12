from django.contrib import admin
from . models import Categories, Supplier, Products, Orders, OrderItems
# Register your models here.



class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff


    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff


    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff


    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff




@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number',
                    'city', 'address', 'created_at', 'updated_at', 'status')

    list_filter = ('status', 'city')
    search_fields = ('full_name', 'phone_number', 'city', 'address')

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff

    def has_delete_permission(self, request, obj=None):

        return request.user.is_superuser or request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_view_permission(self, request, obj=None):

        return request.user.is_superuser or request.user.is_staff

    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff





@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',
                    'price', 'category', 'stock', 'is_available', 'is_sale', 'sale_price',
                    'is_suggestion', 'supplier', 'created_at', 'updated_at')

    list_filter = ('is_available', 'is_sale', 'is_suggestion')
    search_fields = ('name', 'slug')
    list_editable = ('is_suggestion', 'is_available', 'is_sale', 'stock')


    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_staff


    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff


    def has_change_permission(self, request, obj=None):

        return request.user.is_superuser or request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_module_permission(self, request, obj=None):

        return request.user.is_superuser or request.user.is_staff






@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'city', 'shipping_address', 'postal_code',
                    'created_at', 'status', 'shipped')

    list_filter = ('status', 'city', 'shipped')
    search_fields = ('full_name', 'phone_number', 'city', 'address', 'postal_code')
    list_editable = ('status', 'shipped')

    inlines = [OrderItemsInline]


    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser


    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff

    def has_module_permission(self, request, obj=None):
        return request.user.is_superuser or request.user.is_staff



