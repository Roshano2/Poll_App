from urllib import response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse
from django.template import loader
from django.views import generic


# Create your views here.
def main(request):
     return render(request,"post/main.html")

# def detail(request, question_id):
#     return HttpResponse("you are looking at question %s" % question_id)

# def results(request, question_id):
#     response = "you are looking at the results of question %s"
#     return HttpResponse(response % question_id)

# def vote(request, question_id):
#     return HttpResponse("you are voting on question %s" % question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('post/index.html')
    context = {
        'latest_question_list' : latest_question_list}
    return render(request,'post/index.html',context)

# class IndexView(generic.ListView):
#     template_name: 'post/index.html'
#     context_object_name: 'latest_question_list'
#     def get_queryset(self):
#         return Question.objects.order_by('pub_date')[:5]

# class DetailView(generic.DetailView):
#     model: Question
#     template_name: 'post/detail.html'

# class ResultsView(generic.DetailView):
#     model: Question
#     template_name: 'post/results.html'

def detail(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'post/detail.html', {'question': question})

def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'post/detail.html',{
            'question': question,
            'error_message': "you didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('post:results', args=(question.id,)))

def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request,'post/results.html',{'question': question})
