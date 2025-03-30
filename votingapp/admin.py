from django.contrib import admin
from .models import Topic,Options,User
# Register your models here.
admin.site.site_header = "VoteHala"
admin.site.site_title = "VoteHala Admin Area"
admin.site.index_title = "Welcome to VoteHala Admin Area"

class OptionInLine(admin.TabularInline):
    model = Options
    extra = 3
    
class TopicAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['topic']}),
                 ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),]
    inlines = [OptionInLine]
    
admin.site.register(User)
admin.site.register(Topic, TopicAdmin)
# admin.site.register(Options)