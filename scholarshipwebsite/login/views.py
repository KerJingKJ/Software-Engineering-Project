from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, SecurityQuestionForm, LoginForm, ForgotPasswordForm, SecurityQuestionVerifyForm, ResetPasswordForm
from .models import UserSecurityQuestion, UserProfile
from .models import SECURITY_QUESTION_CHOICES
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib import messages

def index(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            
            user_obj = User.objects.filter(email=email).first()
            
            if user_obj is None:
                messages.error(request, "User not found. Sign up for an account.")
            else:
                
                user = authenticate(username=user_obj.username, password=password)
                
                if user is not None:
                    login(request, user)

                    if not user.is_staff and not UserSecurityQuestion.objects.filter(user=user).exists():
                        return redirect('securityquestion')

                    
                    
                    email_domain = user.email.split('@')[-1]
                    
                    if 'student.mmu.edu.my' in email_domain:
                        return redirect('student')
                    elif 'admin.mmu.edu.my' in email_domain:
                        return redirect('/admin/')
                    elif 'reviewer.mmu.edu.my' in email_domain:
                        return redirect('reviewer')
                    elif 'committee.mmu.edu.my' in email_domain:
                        return redirect('committee')
                    else:
                        return redirect('committee') 
                else:
                    messages.error(request, "Wrong password! Try again")
    else:
        form = LoginForm()
        
    return render(request, "login/login.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            
            user = User.objects.create_user(username=username, email=email, password=password)
            
            
            from django.contrib.auth import login
            login(request, user)
            
            
            return redirect("securityquestion")
    else:
        form = SignUpForm()
    
    return render(request, "login/signup.html", {"form": form})

@login_required(login_url='login')
def securityquestion(request):
    try:
        instance = request.user.security_questions
    except UserSecurityQuestion.DoesNotExist:
        instance = None

    if request.method == "POST":
        form = SecurityQuestionForm(request.POST, instance=instance)
        if form.is_valid():
            security_question = form.save(commit=False)
            security_question.user = request.user
            security_question.save()

             
            email_domain = request.user.email.split('@')[-1]
                    
            if 'admin.mmu.edu.my' in email_domain:
                return redirect('/admin/')
            elif 'reviewer.mmu.edu.my' in email_domain:
                return redirect('reviewer')
            elif 'committee.mmu.edu.my' in email_domain:
                return redirect('committee')
            return redirect('setup_profile') 
    else:
        form = SecurityQuestionForm(instance=instance)

    return render(request, "login/security_question.html", {"form": form})

from .forms import UserProfileForm

@login_required(login_url='login')
def setup_profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == "POST":
        if 'skip' in request.POST:
             return redirect('login')
             
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, "login/setup_profile.html", {"form": form})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)
            request.session['reset_user_id'] = user.id
            return redirect('verify_question')
    else:
        form = ForgotPasswordForm()
    return render(request, 'login/forgot_password.html', {'form': form})

def verify_question(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('forgot_password')
    
    try:
        user = User.objects.get(id=user_id)
        security_questions = UserSecurityQuestion.objects.get(user=user)
    except (User.DoesNotExist, UserSecurityQuestion.DoesNotExist):
        messages.error(request, "Security questions not set for this account.")
        return redirect('forgot_password')

    
    q1_text = next(text for key, text in SECURITY_QUESTION_CHOICES if key == security_questions.question_1)
    q2_text = next(text for key, text in SECURITY_QUESTION_CHOICES if key == security_questions.question_2)

    if request.method == 'POST':
        form = SecurityQuestionVerifyForm(request.POST, question_1_label=q1_text, question_2_label=q2_text)
        if form.is_valid():
            ans1 = form.cleaned_data['answer_1']
            ans2 = form.cleaned_data['answer_2']
            
            
            if (ans1.strip().lower() == security_questions.answer_1.strip().lower() and 
                ans2.strip().lower() == security_questions.answer_2.strip().lower()):
                request.session['reset_verified'] = True
                return redirect('reset_password_confirm')
            else:
                messages.error(request, "One or both answers are incorrect.")
    else:
        form = SecurityQuestionVerifyForm(question_1_label=q1_text, question_2_label=q2_text)

    return render(request, 'login/verify_question.html', {'form': form})

def reset_password_confirm(request):
    user_id = request.session.get('reset_user_id')
    verified = request.session.get('reset_verified')
    
    if not user_id or not verified:
        return redirect('forgot_password')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=user_id)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            
            del request.session['reset_user_id']
            del request.session['reset_verified']
            
            messages.success(request, "Password reset successful. Please login.")
            return redirect('login')
    else:
        form = ResetPasswordForm()
        
    return render(request, 'login/reset_password.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    
    logout(request)
    return redirect('landingpage') 



def get_dashboard_redirect(user):
    
    if hasattr(user, 'student'): 
        return 'student_dashboard' 
    elif user.groups.filter(name='Reviewer').exists() or 'reviewer' in user.username:
        return 'reviewer' 
    return 'committee' 

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated!')
            
            
            return redirect(get_dashboard_redirect(request.user)) 
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    email_domain = request.user.email.split('@')[-1]
    
    if 'student.mmu.edu.my' in email_domain:
        base_template = 'student/base.html'
    elif 'reviewer.mmu.edu.my' in email_domain:
        base_template = 'reviewer/base.html'
    else:
        base_template = 'committee/base.html'

    return render(request, 'login/change_password.html', {
        'form': form,
        'base_template': base_template
    })

@login_required(login_url='login')
def update_security_questions(request):
    try:
        instance = request.user.security_questions
    except UserSecurityQuestion.DoesNotExist:
        instance = None
    security_form = SecurityQuestionForm(instance=instance)
    
    if request.method == "POST":
        form = SecurityQuestionForm(request.POST, instance=instance)
        if form.is_valid():
            security_question = form.save(commit=False)
            security_question.user = request.user
            security_question.save()
            messages.success(request, 'Questions updated!')
            
            
            return redirect(get_dashboard_redirect(request.user))
    else:
        form = SecurityQuestionForm(instance=instance)

    email_domain = request.user.email.split('@')[-1]
    
    if 'student.mmu.edu.my' in email_domain:
        base_template = 'student/base.html'
    elif 'reviewer.mmu.edu.my' in email_domain:
        base_template = 'reviewer/base.html'
    else:
        base_template = 'committee/base.html'

    return render(request, "login/change_securityquestion.html", {
        'form': form,
        'base_template': base_template
        })