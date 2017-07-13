from django.contrib import admin
from models import Question, Quiz, QuizToQuestion, QuestionUploader, QuizToUploaderTag, Student, ScoreToQuestion, Options, Subject, QuizToStudentTag, QuizToSubject

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(QuizToSubject)
admin.site.register(QuizToStudentTag)
admin.site.register(QuizToUploaderTag)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(ScoreToQuestion)
admin.site.register(Options)
admin.site.register(QuestionUploader)
admin.site.register(QuizToQuestion)


