from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User,Host_hack,Participants,Winner

# class Hostform(forms.ModelForm):
#     title = forms.CharField(required=True)
#     desc = forms.CharField(required=True, widget=forms.Textarea)
#     org_name = forms.CharField(required=True)
#     org_desc = forms.CharField(required=True, widget=forms.Textarea)
#     image = forms.ImageField(required=False)  # Assuming you're using ImageField for the image field

#     class Meta:
#         model = Host_hack
#         exclude = ['host_name', 'from_date', 'end_date']

class WinnerForm(forms.ModelForm):
    class Meta:
        model = Winner
        fields = ['team', 'position']


class CustomCreationForm(UserCreationForm,forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':'password'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password', 'align':'center', 'placeholder':' confirm password'}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", 'roles',"email",'password1','password2')
        widgets = {
             'first_name': forms.TextInput(attrs={'class': "form-control",'placeholder':'First Name '}),
             'last_name': forms.TextInput(attrs={'class': "form-control",'placeholder':'Last Name '}),
             'roles': forms.Select(attrs={'class':"form-control",'placeholder':'Select'}),
             'email': forms.TextInput(attrs={'class': "form-control",'placeholder':'Email '}),
            
            # 'password1': forms.PasswordInput(attrs={'class': "form-control",'type':'password','placeholder':'Password'}),
            # 'password2': forms.PasswordInput(attrs={'class': "form-control",'placeholder':'Confirm Password'}),
            }
        def clean(self):
            cleaned_data = super(UserForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError(
                    "password and confirm_password does not match"
             )



class Participate_data(forms.ModelForm):
    class Meta:
        model = Participants
        fields = '__all__'
        # exclude = ['host_name']
        if('roles' == 'is_student'):
            exclude = ['organization']
     

