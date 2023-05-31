from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Host_hack,Details,Data, Winner
from django.contrib.auth import authenticate,login,logout
from .forms import CustomCreationForm,Participate_data,WinnerForm
import datetime
import os
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse


def host_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated and is a host
        if request.user.is_authenticated and request.user.roles == 'is_host':
            # User is a host, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not a host, show an error message and redirect
            # messages.error(request, "You are not authorized to access this page as a host.")
            return redirect('home')  # Replace 'home' with the appropriate URL name for your home page
    return wrapper

def participant_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Check if the user is authenticated and is a participant
        if request.user.is_authenticated and request.user.roles == 'is_part':
            # User is a participant, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not a participant, show an error message and redirect
            # messages.error(request, "You are not authorized to access this page as a participant.")
            return redirect('home')  # Replace 'home' with the appropriate URL name for your home page
    return wrapper


# Create your views here.
today = datetime.date.today()

def home(request):
    return HttpResponse("DSDFsf")


# def home(request):
#     if not request.user.is_authenticated:
#         hackathons = Host_hack.objects.all()
#         total_hackathons = hackathons.count()
#         team_count = Details.objects.count()
#         user_count = User   .objects.count()
#         context = {
#             'total_hackathons': total_hackathons,
#             'hackathons': hackathons,
#             'team_count':team_count,
#             'user_count':user_count
#         }
#         return render(request,"index.html",context)
#     username = None
#     participated_hackathons = Details.objects.filter(Q(team_leader=request.user) | Q(team_m2=request.user) | Q(team_m3=request.user))
#     only_host = Host_hack.objects.filter(host_name = request.user)
#     print(only_host)
#     for host in only_host:
#         print(host)
#     all_host = Host_hack.objects.all()
#     context = {'host': all_host,'only_host':only_host,'today':today,'participated_hackathons':participated_hackathons} 
#     if request.user.is_authenticated:
#         username = request.user
#         return render(request,"home.html",context)
#     return render(request,"index.html",context)


@host_login_required
def part_details(request,id):
    details  = Details.objects.filter(project_id=id)
    data = Data.objects.filter(project_id=id)
    hack = Host_hack.objects.get(id=id)
    print(hack.id)
    print(data)
    return render(request,"part_detail.html",{'details':details,'data':data,'host':hack})   

@participant_login_required
def hack_details(request,pk):
    # details  = Details.objects.filter()
    winners = Winner.objects.filter(project_id=pk).order_by('position')
    team_details = []
    for winner in winners:
        team = Details.objects.get(team_id=winner.team_id)
        team_details.append({
            'position': winner.get_position_display(),
            'team_leader': team.team_leader,
            'team_members': [team.team_m2, team.team_m3],
        })


    try:
        participated_hackathons = Details.objects.get(
            (Q(team_leader=request.user) & Q(project_id=pk)) |
            (Q(team_m2=request.user) & Q(project_id=pk)) |
            (Q(team_m3=request.user) & Q(project_id=pk))
        )

    except Details.DoesNotExist:

        participated_hackathons = None
    try:
        data = Data.objects.get(Q(project_id=pk) & Q(user=request.user))
    except:
        data = None
    details  = Details.objects.filter(project_id=pk)

    project_id_int = int(participated_hackathons.project_id) if participated_hackathons else None
    hack = Host_hack.objects.get(id=pk)
    print(type(hack.id))
    context = {'hack':hack,'today':today,'data':data,'details':details,'participated_hackathons':project_id_int,'team_details': team_details}
    # print(data.user)
    # print(details)
    return render(request,"host_details.html",context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = CustomCreationForm()
    if request.method == "POST":

        form = CustomCreationForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(commit  = False)
            username = request.POST.get('email')
            password = request.POST.get('password1')
            print(username,password)
            use = authenticate(username=username, password=password)
            user.save()
            print(use)
            if user is not None:
                login(request, user)
                return redirect('home')

    return render(request,"register.html",{'form':form})



def log(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST['email']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                print('Invalid Username or Password')
                return redirect('log')

        else:
            return render(request, 'login.html')

        return render(request,'login.html')

@login_required
def logout_form(request):
    logout(request)
    return redirect('log')

@host_login_required
def host_hack(request):
    
    # if request.method == 'POST':
    #         if request.POST.get('email'):
    #             form.email = 
    if request.method == 'POST':
        image = request.FILES['image']
        Host_hack.objects.create(
            image=image,
            host_name =request.user,
         
            title=request.POST.get('title'),
            org_name=request.POST.get('org_name'),
            org_desc=request.POST.get('org_name'),
            desc=request.POST.get('desc'),
            from_date=request.POST.get('from-date'),
            end_date=request.POST.get('end-date')
        )
        return redirect('home')
    
    return render(request,'host_hack.html')



@host_login_required
def delete(request, id):
    member = Host_hack.objects.get(id=id)
    member.delete()
    return redirect('home')


@participant_login_required
def edit_file(request, id):
    key = id
    data = Data.objects.get(id=id)
    if(request.method == 'POST'):
        if len(request.FILES)!=0:
            if len(data.files)>0:
                if os.path.exists(data.files.path)==True:
                    os.remove(data.files.path)

            data.files = request.FILES.get('files')
            data.save()
            return redirect('home')

    return render(request,'host_details.html',{'data':data})

@host_login_required
def participants_data(request):
    form = Participate_data()
    return render(request, 'user_data.html',{'form':form})

# @login_required   
@participant_login_required
def apply(request, id):
    topic = Host_hack.objects.get(id=id)
    # check_user = Details.objects.filter(project_id=id)
    # print(check_user.team_leader)

    if request.method == 'POST':
        title = request.POST.get('title')
        team_leader_email = request.user.email
        team_m2_email = request.POST.get('t2')
        team_m3_email = request.POST.get('t3')

        # Check if team leader has already participated in the hackathon
        if Details.objects.filter(team_leader=team_leader_email, project_id=id).exists():
            messages.error(request, f"You have already participated in this hackathon as a team leader.")
            return redirect('apply', id=id)

        # Check if team member 2 has already participated in the hackathon
        if team_m2_email and Details.objects.filter(team_m2=team_m2_email, project_id=id).exists():
            messages.error(request, f"The team member 2 '{team_m2_email}' has already participated in this hackathon.")
            return redirect('apply', id=id)

        # Check if team member 3 has already participated in the hackathon
        if team_m3_email and Details.objects.filter(team_m3=team_m3_email, project_id=id).exists():
            messages.error(request, f"The team member 3 '{team_m3_email}' has already participated in this hackathon.")
            return redirect('apply', id=id)
        # Check if team leader email exists
        if not User.objects.filter(email=team_leader_email).exists():
            messages.error(request, f"Email '{team_leader_email}' is not available.")
            return redirect('apply', id=id)

        # Check if team member 2 email exists
        if team_m2_email and not User.objects.filter(email=team_m2_email).exists():
            messages.error(request, f"Email '{team_m2_email}' is not available.")
            return redirect('apply', id=id)

        # Check if team member 3 email exists
        if team_m3_email and not User.objects.filter(email=team_m3_email).exists():
            messages.error(request, f"Email '{team_m3_email}' is not available.")
            return redirect('apply', id=id)

        # All emails are available, proceed with creating the team details
        Details.objects.create(
            title=title,
            project_id=request.POST.get('id'),
            team_leader=request.user,
            team_m2=team_m2_email,
            team_m3=team_m3_email
        )
        return redirect('home')

    return render(request, 'apply.html', {'topic': topic})







# def apply(request,id):
#     # use = User.objects.all()
#     # if request.method == 'POST':
#     #     email = request.POST.get('check')
#     #     data = User.objects.get(email=email)
#     #     # print(data)
#     #     return render(request, 'apply.html',{'data':data})
#     topic = Host_hack.objects.get(id = id)
#     if request.method == 'POST':
#         Details.objects.create(
            
#             title=request.POST.get('title'),
#             project_id = request.POST.get('id'),
#             team_leader =request.user,
#             team_m2 = request.POST.get('t2'),
#             team_m3 =request.POST.get('t3')
           
#         )
#         title=request.POST.get('title')
#         print(title)
#         return redirect('home')

#     return render(request, 'apply.html',{'topic':topic})
@participant_login_required
def store_file(request):
    if request.method == 'POST':
        Data.objects.create(
            user = request.user,
            files=request.FILES.get('files'),
            project_id = request.POST.get('pid')
        )
        return redirect('home')


    return render(request, 'host_details.html')


@host_login_required
def create_winner(request, id):
    project_id = id
    hackathon_teams = Details.objects.filter(project_id=project_id)
    winner = Winner.objects.filter(project_id=id)
    
    if request.method == 'POST':
        team_id = request.POST.get('team')
        position = request.POST.get('position')
        
        # Check if the position is already assigned to a different team
        existing_winner = winner.filter(position=position).exclude(team_id=team_id).first()
        if existing_winner:
            error_message = f"Position {position} is already assigned to Team {existing_winner.team_id}"
            messages.error(request, error_message)
        else:
            # Check if the team is already a winner for the project
            existing_winner = winner.filter(team_id=team_id).first()
            if existing_winner:
                error_message = f"Team {existing_winner.team_id} is already a winner for this project"
                messages.error(request, error_message)
            else:
                Winner.objects.create(
                    project_id=project_id,
                    team_id=team_id,
                    position=position
                )
                return redirect(reverse('create_winner', args=[project_id]))
    
    form = WinnerForm()
    context = {'form': form, 'project_id': project_id, 'hackathon_teams': hackathon_teams, 'winner': winner}
    return render(request, 'result.html', context)

@host_login_required
def clear_winners(request, id):
    Winner.objects.filter(project_id=id).delete()
    return redirect('create_winner', id=id)

# @host_login_required
def winner_results(request, project_id):
    winners = Winner.objects.filter(project_id=project_id).order_by('position')
    team_details = []
    for winner in winners:
        team = Details.objects.get(team_id=winner.team_id)
        team_details.append({
            'position': winner.get_position_display(),
            'team_leader': team.team_leader,
            'team_members': [team.team_m2, team.team_m3],
        })
    context = {'team_details': team_details}
    return render(request, 'winner_results.html', context)


def check_email_availability(request):
    email = request.GET.get('email')
    user_exists = User.objects.filter(email=email).exists()
    print(f"Email: {email}")
    print(f"User Exists: {user_exists}")
    available = not user_exists  # Check if the user with the email exists or not
    print(f"Available: {available}")
    return JsonResponse({'available': available})
