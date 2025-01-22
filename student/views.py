from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL


#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)


# Add this temporary code to student_exam_view to check question data
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()

    # Debug: Print question data
    for course in courses:
        questions = QMODEL.Question.objects.filter(course=course)
        for q in questions:
            print(f"Question: {q.question}")
            print(f"Type: {q.question_type}")
            print(f"MCQ Answer: {q.mcq_answer}")
            print(f"Model Answer: {q.model_answer}")
            print("---")

    return render(request, 'student/student_exam.html', {'courses': courses})
@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        # Add debug print
        print("POST data:", request.POST)

    response = render(request, 'student/start_exam.html', {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)
        student = models.Student.objects.get(user_id=request.user.id)

        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)

        for i in range(len(questions)):
            question = questions[i]
            question_number = str(i + 1)

            # Get the selected answer based on question type
            if question.question_type == 'MCQ':
                selected_ans = request.COOKIES.get(question_number)
            else:
                selected_ans = request.COOKIES.get(f"{question_number}_{question.question_type.lower()}")

            marks_for_question = 0
            if selected_ans:
                selected_ans = selected_ans.strip()

                if question.question_type == 'MCQ':
                    correct_ans = question.mcq_answer.strip()
                    if selected_ans == correct_ans:
                        marks_for_question = question.marks
                elif question.question_type in ['ESSAY', 'SHORT']:
                    correct_ans = question.model_answer.strip()
                    if selected_ans.lower() == correct_ans.lower():
                        marks_for_question = question.marks

            # Use update_or_create instead of create
            result, created = QMODEL.Result.objects.update_or_create(
                student=student,
                exam=course,
                question=question,
                defaults={
                    'marks_obtained': marks_for_question,
                    'answer_text': selected_ans
                }
            )

            total_marks += marks_for_question

        response = HttpResponseRedirect('view-result')
        response.delete_cookie('course_id')
        # Delete answer cookies
        for i in range(len(questions)):
            response.delete_cookie(str(i + 1))
            response.delete_cookie(f"{i + 1}_essay")
            response.delete_cookie(f"{i + 1}_short")

        return response

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)

    # Get distinct results for this course and student
    results = QMODEL.Result.objects.filter(
        exam=course,
        student=student
    ).values('exam', 'date').annotate(
        marks=Sum('marks_obtained')
    ).order_by('-date')  # Most recent first

    return render(request, 'student/check_marks.html', {'results': results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})
  