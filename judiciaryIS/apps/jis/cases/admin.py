from django.contrib import admin

# Register your models here
from .models import Case, Hearing, Document

class HearingInline(admin.TabularInline):
    model = Hearing
    extra = 1

class DocumentInline(admin.TabularInline):
    model = Document
    extra = 1

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'title', 'status', 'assigned_judge', 'date_filed')
    list_filter = ('status', 'assigned_judge', 'date_filed')
    search_fields = ('case_number', 'title', 'assigned_judge__username')
    inlines = [HearingInline, DocumentInline]
    
    # Make case_number read-only after creation
    readonly_fields = ('case_number', 'date_filed')

admin.site.register(Hearing)
admin.site.register(Document)