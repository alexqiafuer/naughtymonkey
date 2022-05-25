from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from .models import Profile, Message
from .forms import MyUserCreationForm, ProfileForm, SkillForm, MessageForm

from .util import search


def loginUser(request):
    # if request.user.is_authenticated:
    #     return redirect('profiles')
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method != 'POST':
        return render(request, 'users/login_register.html')

    username = request.POST['username'].lower()
    password = request.POST['password']

    try:
        user = User.objects.get(username=username)
    except:
        messages.error(request, 'Username does not exist')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # print('logged in, next = ', request)
        # print(request.GET)
        login(request, user)
        return redirect(request.GET['next'] if 'next' in request.GET else 'user-account')
    else:
        messages.error(request, 'Wrong Username or Password')
        return redirect('user-login')


def logoutUser(request):
    logout(request)
    messages.info(request, 'You are logged out now')
    return redirect('profiles')


def registerUser(request):
    page = 'register'
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'You have just created your account')

            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Something is wrong')

    context = {'page': page, 'form': form}

    return render(request, 'users/login_register.html', context)


def profiles(request):

    profiles, search_query = search(request)

    page = request.GET.get('page')
    profiles_per_page = 6
    paginator = Paginator(profiles, profiles_per_page)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    context = {'profiles': profiles, 'search_query': search_query,
               'pages': paginator.page_range}

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topskills': topskills,
               'otherskills': otherskills}

    return render(request, 'users/user-profile.html', context)


@login_required(login_url='user-login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    social_fields = [field.name for field in Profile._meta.get_fields()
               if field.name.startswith('social')]
    socials = {}
    for name in sorted(social_fields):
        title = name.split('_')[1]
        value = getattr(profile, name)
        socials[title] = value

    #print('socials', socials)

    context = {'profile': profile, 'skills': skills,
               'projects': projects, 'socials': socials}
    return render(request, 'users/account.html', context)


@login_required(login_url='user-login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-account')

    context = {'form': form}

    return render(request, 'users/profile_form.html', context)


@login_required(login_url='user-login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added')
            return redirect('user-account')

    context = {'form': form}

    return render(request, 'users/skill.html', context)


@login_required(login_url='user-login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated')
            return redirect('user-account')

    context = {'form': form}

    return render(request, 'users/skill.html', context)


@login_required(login_url='user-login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was Deleted')
        # return redirect('user-account')

    context = {'obj': skill}
    return render(request, 'delete_obj.html', context)


@login_required(login_url='user-login')
def inbox(request):
    profile = request.user.profile
    user_messages = profile.messages.all()
    unread = user_messages.filter(is_read=False).count()

    context = {'user_messages': user_messages, 'unread':unread}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='user-login')
def viewMessage(request, pk):
    profile = request.user.profile
    user_message = profile.messages.get(id=pk)
    if not user_message.is_read:
        user_message.is_read = True
        user_message.save()

    context = {'user_message': user_message}

    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    exclude = set()
    if request.user.is_authenticated:
        exclude = set(['name', 'email'])

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            return redirect('user-profile', pk=recipient.id)

    context = {'form': form, 'recipient': recipient, 'exclude': exclude}

    return render(request, 'users/message_form.html', context)
