from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=150, label="Name")
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean_name(self):
        name = self.cleaned_data['name']
        if User.objects.filter(username=name).exists():
            raise forms.ValidationError("Username is already taken.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            # Check if passwords match
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")

            # Check password complexity
            # 1. At least 8 characters
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            
            # 2. At least one uppercase letter
            if not any(char.isupper() for char in password):
                self.add_error('password', "Password must contain at least one uppercase letter.")

            # 3. At least one punctuation/special character
            # Using checks for non-alphanumeric characters excluding standard spaces if desired, 
            # or specifically verifying against a set of punctuation.
            # Here we check for any character that is not a letter or number.
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                 self.add_error('password', "Password must contain at least one special character/punctuation.")


        return cleaned_data

from .models import UserSecurityQuestion

class SecurityQuestionForm(forms.ModelForm):
    class Meta:
        model = UserSecurityQuestion
        fields = ['question_1', 'answer_1', 'question_2', 'answer_2']
        labels = {
            'question_1': 'Security Question 1',
            'answer_1': 'Answer 1',
            'question_2': 'Security Question 2',
            'answer_2': 'Answer 2',
        }
        widgets = {
            'answer_1': forms.TextInput(attrs={'placeholder': 'Your Answer'}),
            'answer_2': forms.TextInput(attrs={'placeholder': 'Your Answer'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        question_1 = cleaned_data.get("question_1")
        question_2 = cleaned_data.get("question_2")

        if question_1 and question_2 and question_1 == question_2:
            self.add_error('question_2', "Please select two different security questions.")
        
        return cleaned_data

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your email to reset password")

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user found with this email address.")
        return email

class SecurityQuestionVerifyForm(forms.Form):
    answer_1 = forms.CharField(label="Answer to Question 1")
    answer_2 = forms.CharField(label="Answer to Question 2")

    def __init__(self, *args, **kwargs):
        question_1_label = kwargs.pop('question_1_label', 'Security Question 1')
        question_2_label = kwargs.pop('question_2_label', 'Security Question 2')
        super().__init__(*args, **kwargs)
        self.fields['answer_1'].label = question_1_label
        self.fields['answer_2'].label = question_2_label

class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', "Passwords do not match.")
            
            if len(password) < 8:
                self.add_error('password', "Password must be at least 8 characters long.")
            
            if not any(char.isupper() for char in password):
                self.add_error('password', "Password must contain at least one uppercase letter.")
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                 self.add_error('password', "Password must contain at least one special character/punctuation.")
        
        return cleaned_data

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'contact_number', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4,'class': 'bio-styled'}),
        }
