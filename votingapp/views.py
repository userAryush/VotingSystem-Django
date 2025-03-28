from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import loader
from django.urls import reverse
from .models import Topic, Options

# Create your views here.

# get topic and display
def index(request):
    latest_question_list = Topic.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


# show topic and options
def detail(request, topic_id):
    try:
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        raise Http404('Topic Does not exists!')

    return render(request, 'polls/details.html', {'topic': topic})

# get topic and display result

def results(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'polls/results.html', {'topics': topic})

#vote for a topic option
def vote(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    try:
        selected_option = topic.options_set.get(pk=request.POST['option'])
    except(KeyError, Options.DoesNotExist):
        return render(request, 'polls/detail.html', {'topics':topic,
                                                    'error_message':'You didnt select a option.'})
    else:
        selected_option.votes +=1
        selected_option.save()
        return HttpResponseRedirect(reverse('polls:results', args=(topic.id,)))
    
    