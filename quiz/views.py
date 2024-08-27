from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz, Answer, AnswerDetail
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Quiz, QuestionSet, Question, Option
from django.forms import modelformset_factory

@login_required
def quiz_create(request):
    if request.method == 'POST':
        quiz_name = request.POST.get('name')
        amount = int(request.POST.get('amount'))

        quiz = Quiz.objects.create(
            name=quiz_name,
            author=request.user,
            amount=amount
        )

        for i in range(4): 
            question_name = request.POST.get(f'question_{i}')
            question_set = QuestionSet.objects.create(quiz=quiz)
            question = Question.objects.create(name=question_name, set=question_set)
            for j in range(4):  
                option_name = request.POST.get(f'question_{i}_option_{j}')
                is_correct = request.POST.get(f'question_{i}_correct_option') == f'question_{i}_option_{j}'
                Option.objects.create(name=option_name, question=question, correct=is_correct)

        return redirect('quiz_list')

    context = {
        'range_4': range(4), 
    }
    return render(request, 'quiz_create.html', context)

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})


@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions

    if request.method == 'POST':
        answer = Answer.objects.create(
            quiz=quiz,
            author=request.user,
            start_time=timezone.now(),
            end_time=timezone.now()
        )

        for question in questions:
            user_choice_id = request.POST.get(f'question_{question.id}')
            if user_choice_id:
                user_choice = question.options.get(id=user_choice_id)
                AnswerDetail.objects.create(
                    answer=answer,
                    question=question,
                    user_choice=user_choice
                )
        return redirect('quiz_result', answer_id=answer.id)

    return render(request, 'quiz_detail.html', {'quiz': quiz, 'questions': questions})


@login_required
def quiz_result(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    details = AnswerDetail.objects.filter(answer=answer)

    correct_count = sum(detail.is_correct for detail in details)
    total_questions = details.count()

    return render(request, 'quiz_result.html', {
        'answer': answer,
        'details': details,
        'correct_count': correct_count,
        'total_questions': total_questions
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('quiz_list')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Login yoki parol noto‘g‘ri'})
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Username yoki password xato'})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

