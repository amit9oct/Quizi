from django.http.response import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render

from App.models import Question, QuestionUploader, Student, Quiz, Subject, QuizToSubject, QuizToUploaderTag, QuizToStudentTag, QuizToQuestion, Options, ScoreToQuestion

# Globals
TITLE = "IPEC IIT"


# /
def home(request):
    context = {"title": TITLE}
    if 'user_id' in request.session:
        context["user_id"] = request.session['user_id']
        if request.session['user_type'] == 'Uploader':
            uploader = QuestionUploader.objects.filter(user_id=request.session['user_id'])[0]
            context["all_quiz"] = [inst.quiz for inst in QuizToUploaderTag.objects.filter(uploader=uploader)]
            return render(request, "upload.html", context)
        else:
            student = Student.objects.filter(user_id=request.session['user_id'])[0]
            context["all_quiz"] = [inst.quiz for inst in QuizToStudentTag.objects.filter(student=student)]
            return render(request, "upload.html", context)

    return render(request, "index.html", context)


# /login/
def login(request):
    request.session.flush()
    if request.method == 'GET':
        return HttpResponseBadRequest
    elif request.method == 'POST':
        user_id = request.POST['user_id']
        password = request.POST['password']
        user_type = request.POST['user_type']
        temp_user = None
        context = {"title": TITLE}
        if user_type == "Uploader":
            temp_user = QuestionUploader.objects.filter(user_id=user_id, password=password)
        if user_type == "Student":
            temp_user = Student.objects.filter(user_id=user_id, password=password)
        if len(temp_user) == 0:
            context["message"] = "User Id {} is not registered".format(user_id)
            return render(request, "index.html", context)
        elif len(temp_user) == 1:
            user = temp_user[0]
            request.session['user_id'] = user.user_id
            request.session['user_type'] = user_type
            if user_type == "Uploader":
                quiz_to_uploader = [q.quiz for q in QuizToUploaderTag.objects.filter(uploader=user)]
                context['all_quiz'] = quiz_to_uploader
                return render(request, "upload.html", context)
            else:
                quiz_to_student = [q.quiz for q in QuizToStudentTag.objects.filter(student=user)]
                context['all_quiz'] = quiz_to_student
                return render(request, "upload.html", context)


# /logout/
def logout(request):
    context = {"title": TITLE}
    if 'user_id' in request.session:
        request.session.flush()
        context['message'] = 'Successfully Logged Out!!!'
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html', context)


# /submit_answer/
def submit_answer(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        question_pk = request.POST.get('question_pk', None)
        answer = request.POST.get('answer', None)
        quiz_name = request.POST.get('quiz_name', None)
        is_valid = reduce(lambda x, y: x and y, [not (u is None) for u in [user_id, question_pk, answer, quiz_name]])
        if is_valid:
            user = Student.objects.filter(user_id=user_id)[0]
            question = Question.objects.get(pk=int(question_pk))
            quiz = Quiz.objects.filter(name=quiz_name)[0]
            score = 0
            if quiz.is_active:
                if question.options.answer == int(answer):
                    score = question.score
                else:
                    score = question.penalty
                score_to_question_list = ScoreToQuestion.objects.filter(question=question, student=user)
                if len(score_to_question_list) == 0:
                    score_to_question = ScoreToQuestion()
                    score_to_question.question = question
                    score_to_question.score = score
                    score_to_question.student = user
                    score_to_question.answer = int(answer)
                    score_to_question.save()
                else:
                    score_to_question = score_to_question_list[0]
                    score_to_question.score = score
                    score_to_question.answer = int(answer)
                    score_to_question.save()
                return HttpResponse("Your answer was saved successfully!")
            else:
                return HttpResponse("Sorry the quiz is over!! you cannot submit answers now. Click on complete to see your scores")
        else:
            return HttpResponse("Couldn't submit the request")
    else:
        return HttpResponse("Get requests not allowed")


# /add_quiz_home/
def add_quiz_home(request):
    context = {'title': TITLE}
    if 'user_id' in request.session and request.session['user_type'] == 'Uploader':
        subjects = Subject.objects.all()
        context["subjects"] = subjects
        return render(request, 'add-quiz.html', context)
    else:
        return HttpResponseBadRequest


# /load_quiz/?quiz_name=
def load_quiz(request):
    context = {'title': TITLE}
    if 'user_id' in request.session and request.session['user_type'] == 'Uploader':
        quiz_name = request.GET.get('quiz_name', None)
        if quiz_name is None:
            quiz_name = request.POST.get('quiz_name', None)
            if quiz_name is None:
                return HttpResponseBadRequest
        subject_query = request.GET.get('subject_to_list', None)
        if subject_query is None:
            subject_query = request.POST.get('subject_to_list', None)
        selected_subject = "All" if subject_query is None else str(subject_query)
        uploader = QuestionUploader.objects.filter(user_id=request.session['user_id'])[0]
        quizes = [q.quiz for q in QuizToUploaderTag.objects.filter(uploader=uploader)]
        is_valid_quiz = quiz_name in [q.name for q in quizes]
        if is_valid_quiz:
            quiz = None
            for q in quizes:
                if q.name == quiz_name:
                    quiz = q
                    break
            quiz_to_question = [(q.seq_num, q.question) for q in QuizToQuestion.objects.filter(quiz=quiz)]
            context['subjects'] = [q.subject for q in QuizToSubject.objects.filter(quiz=quiz)]
            context['quiz_name'] = quiz_name
            quiz_to_question.sort()
            if selected_subject != "All":
                temp = []
                for q in quiz_to_question:
                    if q[1].subject.name == selected_subject:
                        temp.append(q)
                quiz_to_question = temp
            context['questions'] = [q[1] for q in quiz_to_question]
            return render(request, "uploader-quiz.html", context)
        else:
            return HttpResponseBadRequest
    elif request.session['user_type'] == "Student":
        quiz_name = request.GET.get('quiz_name', None)
        if quiz_name is None:
            quiz_name = request.POST.get('quiz_name', None)
            if quiz_name is None:
                return HttpResponseBadRequest
        subject_query = request.GET.get('subject_to_list', None)
        if subject_query is None:
            subject_query = request.POST.get('subject_to_list', None)
        selected_subject = "All" if subject_query is None else str(subject_query)
        student = Student.objects.filter(user_id=request.session['user_id'])[0]
        quizes = [q.quiz for q in QuizToStudentTag.objects.filter(student=student)]
        is_valid_quiz = quiz_name in [q.name for q in quizes]
        if is_valid_quiz:
            quiz = None
            for q in quizes:
                if q.name == quiz_name:
                    quiz = q
                    break
            quiz_to_question = [(q.seq_num, q.question) for q in QuizToQuestion.objects.filter(quiz=quiz)]
            context['subjects'] = [q.subject for q in QuizToSubject.objects.filter(quiz=quiz)]
            context['quiz_name'] = quiz_name
            quiz_to_question.sort()
            if selected_subject != "All":
                temp = []
                for q in quiz_to_question:
                    if q[1].subject.name == selected_subject:
                        temp.append(q)
                quiz_to_question = temp
            if quiz.is_active:
                context['questions'] = []
                for q in quiz_to_question:
                    check = {}
                    score_to_question_list = ScoreToQuestion.objects.filter(student=student, question=q[1])
                    score_to_question = None
                    if len(score_to_question_list) == 0:
                        score_to_question = ScoreToQuestion()
                        score_to_question.question = q[1]
                        score_to_question.score = 0
                        score_to_question.student = student
                        score_to_question.answer = 0
                        score_to_question.save()
                    else:
                        score_to_question = score_to_question_list[0]
                    check["option1"] = ""
                    check["option2"] = ""
                    check["option3"] = ""
                    check["option4"] = ""
                    check["option5"] = ""
                    check["option"+str(score_to_question.answer)] = "checked"
                    context['questions'].append({"question": q[1], "answer": check})
                return render(request, "uploader-quiz.html", context)
            else:
                context["message"] = "Quiz Yet to start. Is likely to start from {}".format(str(quiz.start_time))
                quiz_to_student = [q.quiz for q in QuizToStudentTag.objects.filter(student=student)]
                context['all_quiz'] = quiz_to_student
                return render(request, "upload.html", context)
        else:
            return HttpResponseBadRequest
    else:
        return HttpResponseBadRequest


# /add_quiz/
def add_quiz(request):
    context = {"title": TITLE}
    if request.method == 'POST':
        if 'user_id' in request.session and request.session['user_type'] == 'Uploader':
            quiz_name = request.POST.get("quiz_name", None)
            subjects = request.POST.getlist("subjects", None)
            num_ques = request.POST.get('num_ques', None)
            if quiz_name is None or subjects is None or num_ques is None:
                return HttpResponseBadRequest
            else:
                quiz = Quiz()
                quiz.name = quiz_name
                quiz.num_ques = int(num_ques)
                quiz.is_active = False
                quiz.save()
                subject_objects = [Subject.objects.filter(name=str(subject))[0] for subject in subjects]
                for subject in subject_objects:
                    quiz_to_subject = QuizToSubject()
                    quiz_to_subject.quiz = quiz
                    quiz_to_subject.subject = subject
                    quiz_to_subject.save()
                quiz_to_uploader = QuizToUploaderTag()
                uploader = QuestionUploader.objects.filter(user_id=request.session['user_id'])[0]
                quiz_to_uploader.quiz = quiz
                quiz_to_uploader.uploader = uploader
                quiz_to_uploader.save()

                # Add all the questions
                for i in range(quiz.num_ques):
                    options = Options()
                    options.option1 = "1"
                    options.option2 = "2"
                    options.option3 = "3"
                    options.option4 = "4"
                    options.option5 = "5"
                    options.answer = 0
                    options.save()
                    question = Question()
                    question.description = "{} question number {}".format(quiz.name, str(i+1))
                    question.options = options
                    question.subject = subject_objects[0]
                    question.score = 0
                    question.penalty = 0
                    question.save()
                    quiz_to_question = QuizToQuestion()
                    quiz_to_question.question = question
                    quiz_to_question.quiz = quiz
                    quiz_to_question.seq_num = i+1
                    quiz_to_question.save()

                context["all_quiz"] = [inst.quiz for inst in QuizToUploaderTag.objects.filter(uploader=uploader)]
                return render(request, "upload.html", context)
        else:
            return HttpResponseBadRequest
    else:
        return HttpResponseBadRequest


# /update_question/
def update_question(request):
    if request.method == "POST":
        if 'user_id' in request.session and request.session['user_type'] == 'Uploader':
            question_pk = request.POST.get("question_pk", None)
            description = request.POST.get("description", None)
            subject = request.POST.get("subject", None)
            option1 = request.POST.get("option1", None)
            option2 = request.POST.get("option2", None)
            option3 = request.POST.get("option3", None)
            option4 = request.POST.get("option4", None)
            option5 = request.POST.get("option5", None)
            answer = request.POST.get("answer", None)
            quiz_name = request.POST.get("quiz_name", None)
            score = request.POST.get('score', None)
            penalty = request.POST.get('penalty', None)
            l = [description, option1, option2, option3, option4, option5, quiz_name, score, penalty, question_pk]
            valid_entries = reduce(lambda x, y: x and y, [not (opn is None) for opn in l])
            if valid_entries:
                uploader = QuestionUploader.objects.filter(user_id=request.session['user_id'])[0]
                quiz_to_uploader = QuizToUploaderTag.objects.filter(uploader=uploader)
                quiz = None
                for q in quiz_to_uploader:
                    if q.quiz.name == quiz_name:
                        quiz = q.quiz
                        break
                if quiz is None:
                    return HttpResponseBadRequest
                else:
                    try:
                        answer = int(answer)
                        score = int(score)
                        penalty = int(penalty)
                    except:
                        return HttpResponseBadRequest
                    if answer > 5 or answer < 1:
                        return HttpResponseBadRequest
                    if penalty > 0 or score < 0:
                        return HttpResponseBadRequest
                    if description.strip() == "":
                        return HttpResponseBadRequest
                    question = Question.objects.get(pk=int(question_pk))
                    subject = question.subject if subject is None else Subject.objects.filter(name=str(subject))[0]
                    options = question.options
                    options.option1 = option1
                    options.option2 = option2
                    options.option3 = option3
                    options.option4 = option4
                    options.option5 = option5
                    options.answer = answer
                    options.save()
                    question.description = description
                    question.options = options
                    question.subject = subject
                    question.score = score
                    question.penalty = penalty
                    question.save()
                    return load_quiz(request)
            else:
                return HttpResponseBadRequest
        else:
            return HttpResponseBadRequest
    else:
        return HttpResponseBadRequest


# /complete_test/
def complete_test(request):
    context = {'title': TITLE}
    if request.method == "POST" and "user_id" in request.session:
        student_id = request.POST.get("user_id", None)
        quiz_name = request.POST.get("quiz_name", None)
        if (not (student_id is None)) and (not (quiz_name is None)):
            user = Student.objects.filter(user_id=student_id)[0]
            quiz = Quiz.objects.filter(name=quiz_name)
            quiz_to_question = [q.question for q in QuizToQuestion.objects.filter(quiz=quiz)]
            subject_scores = {}
            total_subjects = {}
            subject_to_quiz = [s.subject for s in QuizToSubject.objects.filter(quiz=quiz)]
            for sub in subject_to_quiz:
                subject_scores[sub] = 0
                total_subjects[sub] = 0
            score = 0
            total = 0
            for question in quiz_to_question:
                score_to_question = ScoreToQuestion.objects.filter(question=question,student=user)[0]
                subject_scores[score_to_question.question.subject] += score_to_question.score
                score += score_to_question.score
                total += score_to_question.question.score
                total_subjects[score_to_question.question.subject] += score_to_question.question.score
            context["your_score"] = score
            context["total_score"] = total
            temp = [{"subject": sub, "score": subject_scores[sub], "total": total_subjects[sub]} for sub in subject_to_quiz]
            context["subject_scores"] = temp
            return render(request, 'results.html', context)
        else:
            return HttpResponseBadRequest
    else:
        return HttpResponseBadRequest
