from django.contrib import admin

from .models import Post, Discussion,Course, Professor, Rating, Approval, Job, Vacancy
 
class PostAdmin(admin.ModelAdmin):
    list_display = ('text', 'pub_date', 'author') 
    search_fields = ('text',) 
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'

admin.site.register(Post, PostAdmin)
admin.site.register(Vacancy)
admin.site.register(Professor)
admin.site.register(Course)
admin.site.register(Job)
admin.site.register(Rating)
admin.site.register(Approval)