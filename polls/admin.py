from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['g_question_text']}),
        ('Date information', {'fields': ['g_pub_date'], 'classes': ['collapse']}),
    ]

    # getting choices in line per question
    inlines = [ChoiceInline]
    # list display
    list_display = ('g_question_text', 'g_pub_date', 'was_published_recently')
    # adding filter side bar by pub date
    list_filter = ['g_pub_date']
    # adding search
    search_fields = ['g_question_text']


admin.site.register(Question, QuestionAdmin)
