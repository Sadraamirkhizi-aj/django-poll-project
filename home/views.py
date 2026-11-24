from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Question, Choice


def welcome(request):
    return render(request, "home/welcome.html")


def index(request):
    """
    Start the poll.
    The user is sent directly to the first question.
    """

    questions = Question.objects.order_by('pub_date')
    first_question = questions.first()

    if not first_question:
        return render(request, "home/index.html", {
            "latest_question_list": []
        })

    # Start a fresh poll session
    request.session['answered_questions'] = []

    return redirect('home:detail', question_id=first_question.id)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Questions in poll order
    questions = list(
        Question.objects.order_by('pub_date')
    )

    current_index = questions.index(question)

    previous_question = None
    next_question = None

    if current_index > 0:
        previous_question = questions[current_index - 1]

    if current_index < len(questions) - 1:
        next_question = questions[current_index + 1]

    answered_questions = request.session.get(
        'answered_questions',
        []
    )

    is_answered = question.id in answered_questions

    context = {
        'question': question,
        'question_number': current_index + 1,
        'total_questions': len(questions),
        'previous_question': previous_question,
        'next_question': next_question,
        'is_answered': is_answered,
    }

    return render(
        request,
        "home/detail.html",
        context
    )


def vote(request, question_id):
    question = get_object_or_404(
        Question,
        pk=question_id
    )

    questions = list(
        Question.objects.order_by('pub_date')
    )

    current_index = questions.index(question)

    previous_question = None
    next_question = None

    if current_index > 0:
        previous_question = questions[current_index - 1]

    if current_index < len(questions) - 1:
        next_question = questions[current_index + 1]

    answered_questions = request.session.get(
        'answered_questions',
        []
    )

    # Prevent duplicate voting
    if question.id in answered_questions:
        if next_question:
            return redirect(
                'home:detail',
                question_id=next_question.id
            )

        return redirect('home:thanks')

    try:
        selected_choice_id = request.POST["choice"]

        selected_choice = question.choice_set.get(
            pk=selected_choice_id
        )

        # Do not allow pending choices
        if selected_choice.is_pending:
            raise Choice.DoesNotExist

    except (KeyError, Choice.DoesNotExist):

        return render(
            request,
            "home/detail.html",
            {
                'question': question,
                'question_number': current_index + 1,
                'total_questions': len(questions),
                'previous_question': previous_question,
                'next_question': next_question,
                'is_answered': False,
                'error_message': "Please choose an available option.",
            },
        )

    # Register vote
    selected_choice.votes += 1
    selected_choice.save()

    # Save answered question in session
    answered_questions.append(question.id)

    request.session['answered_questions'] = answered_questions
    request.session.modified = True

    # Go to next question
    if next_question:
        return redirect(
            'home:detail',
            question_id=next_question.id
        )

    # Poll finished
    return redirect('home:thanks')


def results(request, question_id):
    """
    Display results for the entire poll.
    question_id is kept in the URL for compatibility
    with the existing project.
    """

    questions = Question.objects.prefetch_related(
        'choice_set'
    ).order_by('pub_date')

    results_data = []

    for question in questions:

        choices = list(
            question.choice_set.all()
        )

        total_votes = sum(
            choice.votes for choice in choices
        )

        choice_data = []

        for choice in choices:

            if total_votes > 0:
                percentage = round(
                    (choice.votes / total_votes) * 100,
                    1
                )
            else:
                percentage = 0

            choice_data.append({
                'text': choice.choice_text,
                'votes': choice.votes,
                'percentage': percentage,
            })

        results_data.append({
            'question': question.question_text,
            'choices': choice_data,
            'total_votes': total_votes,
        })

    return render(
        request,
        "home/results.html",
        {
            'results_data': results_data,
        }
    )


def thanks(request):
    last_question = Question.objects.order_by(
        'pub_date'
    ).last()

    return render(
        request,
        "home/thanks.html",
        {
            'last_question': last_question,
        }
    )
def about_me(request):
    return render(request, "home/about.html")