from django.contrib import admin
from .models import *
# Register your models here.


class ProductVarientInline(admin.TabularInline):
    model = Variants
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update')
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit_price', 'amount', 'discount','total_price')
    inlines = [ProductVarientInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Variants)
admin.site.register(Comment, CommentAdmin)