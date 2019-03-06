from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    # 显示需要显示的属性
    list_display = ['name', 'password']
    # 过滤属性
    list_filter = ['password']
    # 分页
    list_per_page = 3
    # 修改指定属性
    fields = ['name']
    # 修改表头位置
    actions_on_bottom = True
    actions_on_top = False
    # 设置搜索框
    search_fields = ['name', 'password']
    # 设置默认排序负号是倒序
    ordering = ['-name']
    # 设置默认可编辑子段
    # list_editable = ['name']
    # 设置点击进入编辑界面
    list_display_links = ['name', 'password']





# admin.site.register(models.User, UserAdmin)
admin.site.register(models.Article)
# Register your models here.
