from __future__ import unicode_literals
from django.utils import timezone
from django.db import models

# class UserDetail(models.Model):
#     name = models.CharField(max_length=50,default="")
#     email = models.CharField(max_length=50,default="")
#     password = models.CharField(max_length=50,default="")
#     user = models.OneToOneField(User)
#
#     def __unicode__(self):
#         return self.name


#class Exam(models.Model):
#    name = models.CharField(max_length=100,default="")
#    user = models.ForeignKey(User)
#
#    def __unicode__(self):
#        return self.name


#class Question(models.Model):
#    question = models.TextField(max_length=200,default="")
#    option1 = models.CharField(max_length=50,default="")
#    option2 = models.CharField(max_length=50, default="")
#    option3 = models.CharField(max_length=50, default="")
#    option4 = models.CharField(max_length=50, default="")
#    answer = models.CharField(max_length=50, default="")
#    exam = models.ForeignKey(Exam)
#
#    def __unicode__(self):
#        return self.question

class Quiz(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    num_ques = models.IntegerField(null=False)
    is_active = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=False, default=timezone.now())
    end_time = models.DateTimeField(null=False, default=timezone.now())

    def __unicode__(self):
        return str(self.name)


class Subject(models.Model):
    name = models.CharField(primary_key=True,max_length=100)

    def __unicode__(self):
        return str(self.name)


class Options(models.Model):
    answer = models.IntegerField(null=False)
    option1 = models.TextField(max_length=500)
    option2 = models.TextField(max_length=500)
    option3 = models.TextField(max_length=500)
    option4 = models.TextField(max_length=500)
    option5 = models.TextField(max_length=500)    

    def __unicode__(self):
        return str(self.answer[:20])            


class Question(models.Model):
    description = models.TextField(max_length=1000)
    options = models.ForeignKey(Options)
    subject = models.ForeignKey(Subject)
    score = models.IntegerField(default=4)
    penalty = models.IntegerField(default=-1)

    def __unicode__(self):
        return str(self.description[:30])


class QuizToQuestion(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    seq_num = models.IntegerField(null=False)

    def __unicode__(self):
        return str(self.quiz) + ' - ' + str(self.seq_num)


class QuizToSubject(models.Model):
    quiz = models.ForeignKey(Quiz)
    subject = models.ForeignKey(Subject)

    def __unicode__(self):
        return str(self.quiz) + ' - ' + str(self.subject)


class Student(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    password = models.TextField(max_length=100)    
    name = models.TextField(max_length=100)

    def __unicode__(self):
        return str(self.name)


class QuestionUploader(models.Model):
    name = models.TextField(max_length=100)
    user_id = models.CharField(primary_key=True, max_length=50)
    password = models.TextField(max_length=100)

    def __unicode__(self):
        return str(self.name)


class QuizToUploaderTag(models.Model):
    quiz = models.ForeignKey(Quiz)
    uploader = models.ForeignKey(QuestionUploader)

    def __unicode__(self):
        return str(self.quiz) + ' - ' + str(self.uploader)


class QuizToStudentTag(models.Model):
    quiz = models.ForeignKey(Quiz)
    student = models.ForeignKey(Student)

    def __unicode__(self):
        return str(self.quiz) + ' - ' + str(self.student)


class ScoreToQuestion(models.Model):
    score = models.IntegerField(null=False)
    question = models.ForeignKey(Question)
    student = models.ForeignKey(Student)
    answer = models.IntegerField(null=False)

    def __unicode__(self):
        return str(self.question) + ' - ' + str(self.student) + ' - ' + str(self.score)