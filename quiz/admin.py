from django.contrib import admin
from .models import Quiz, Answer, AnswerDetail, Option, Question, QuestionSet


admin.site.register(Quiz)
admin.site.register(Answer)
admin.site.register(AnswerDetail)
admin.site.register(Option)
admin.site.register(Question)
admin.site.register(QuestionSet)
