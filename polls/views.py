from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Question, Choice

# Create your views here.

# Get questions and display them
def index(request):
    # order by pub_date limit 5
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# Show specific question and choices
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'polls/detail.html', {'question': question})

# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', { 'question': question })

# Vote for a question choice
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did\'t select a choice',
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # !! DO NOT FORGET COMMA after question_id, it gives and error
        # It is required for it to qualify as a tuple.
        # https://stackoverflow.com/questions/52575418/reverse-with-prefix-argument-after-must-be-an-iterable-not-int
        # _reverse_with_prefix() argument after * must be an iterable, not int
        # Wrong args=(question_id)
        # Correct args=(question_id, )
        #
        # What is tuple? https://blog.codecamp.jp/python-tuple
        return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))
