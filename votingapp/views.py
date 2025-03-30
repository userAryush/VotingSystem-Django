from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.template import loader
from django.urls import reverse
from .models import Topic, Options
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view , permission_classes
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import AllowAny
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# # Create your views here.





# # # API view for user registration
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def api_register(request):
#     password = request.data.get('password')
#     hashed = make_password(password)
#     request.data['password'] = hashed
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response('User data created successfully!')
#     else:
#         return Response(serializer.errors)
def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        data = {'email': email, 'password': make_password(password)}
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return redirect('polls:login')  # Redirect to login after successful registration
        else:
            return render(request, 'authentication/register.html', {'errors': serializer.errors})

    return render(request, 'authentication/register.html')   


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return redirect('polls:index')  # Redirect to dashboard after successful login
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'authentication/login.html')
# API view for user login (returns token)
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def api_login(request):
#     email = request.data.get('email')
#     password = request.data.get('password')
#     user = authenticate(username=email, password=password)

#     if user is None:
#         return Response('Invalid credentials')
#     else:
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response(token.key)
    
    
    
    
    
    
    
    
# get topic and display
@login_required
def index(request):
    if not request.user.is_authenticated:
        print("User is not authenticated!")  # Debugging
        return HttpResponse("You need to be logged in", status=401)
    latest_question_list = Topic.objects.order_by('-pub_date')[:5] # retrieves the latest 5 polls, -pub_date is for setting the order in descending by time
    context = {'latest_question_list': latest_question_list}
    # dictionary is passed to the template so the HTML page can access the topics.
    return render(request, 'polls/index.html', context)


# show topic and options
def detail(request, topic_id): #Displays the details of a single topic, including its voting options
    # receives topic_id from url when the user clicks on a poll
    #topic = get_object_or_404(Topic, pk=topic_id)
    try:
        # retrives a topic from the database 
        topic = Topic.objects.get(pk=topic_id)
    except Topic.DoesNotExist:
        raise Http404('Topic Does not exists!')#If no topic is found with the given topic_id, an HTTP 404 error is raised,  prevents a broken page from loading

    return render(request, 'polls/details.html', {'topic': topic})

# get topic and display result

def results(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'polls/results.html', {'topics': topic})

#vote for a topic option
#Handles user votes, updates the database, and redirects to the results page
def vote(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if 'option' not in request.POST:
        return render(request, 'polls/details.html', {
            'topic': topic,
            'error_message': 'You didn’t select an option.',
        })
    try:
        # pk=request.POST['option'] # retrieves the option voted by the user through id, this option is in name param in html
        # topic.options_set.all() returns all options related to that topic.
        # topic.options_set.get(id) returns  option related to that topic.
        selected_option = topic.options_set.get(pk=request.POST['option'])
    except(Options.DoesNotExist): # If no option is selected (KeyError) or the option does not exist, the user is sent back to the voting page with an error message.
        return render(request, 'polls/details.html', {'topic':topic,
                                                    'error_message':'Invalid option selected.'})
    else:
        selected_option.votes +=1
        selected_option.save()
        return HttpResponseRedirect(reverse('polls:results', args=(topic.id,)))
    
    