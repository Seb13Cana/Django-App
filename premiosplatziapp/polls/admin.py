from django.contrib import admin
#importar el modelo que se quiere probar

from .models import Question, Choice

class ChoceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_text']
    inlines = [ChoceInline]
    list_display = ('question_text', 'pub_update', 'was_published_recently')
    list_filter = ['pub_update']
    search_fields = ['question_text']

# Register your models here.
admin.site.register(Question, QuestionAdmin)
