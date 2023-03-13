from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User

# Form for Users to Register (Updates User Model)
class UserForm(forms.ModelForm):
    # User Name Field
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Username', 'class':'register-input'}), label='')
    # Password Field
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder':'Password', 'class':'register-input'}), label='')
    # Email Field
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder':'Email', 'class':'register-input'}), label='')
    # First Name Field
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class':'register-input'}), label='')
    # Last Name Field
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class':'register-input'}), label='')
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name',)

# Second Form for Users to Register (Updates UserAccount Model)
class UserProfileForm(forms.ModelForm):
    # Date Of Birth Field
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1940,2023), 
            attrs={'placeholder':'DOB(mm/dd/yyyy)', 
            'class':'register-input date-birth'}), label='Date Of Birth')
    # Profile Image Field
    profile_image = forms.ImageField(label='Profile Image', required=False)
    class Meta:
        model = UserAccount
        fields = ('dob', 'profile_image')

# Form For User to Update their Account Details (Update User Model)
class UserFormUpdate(forms.ModelForm):
    # Email Field
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class':'profile-update', "id":"profile-update"}), label='Email')
    # First Name Field
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'profile-update'}), label='First Name')
    # Last Name Field
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class':'profile-update'}), label='Last Name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')

# Second Form For User to Update their Account Details (Update UserAccount Model)
class UserProfileFormUpdate(forms.ModelForm):
    # Bio Field
    bio = forms.CharField(required=False, widget=forms.Textarea(), label='Bio')
    # Profile Image Field
    profile_image = forms.ImageField(label='Profile Image', required=False)
    class Meta:
        model = UserAccount
        fields = ('bio', 'profile_image')

# Form for Users to Create a New Post
class NewPostForm(forms.Form):
    # Caption Field
    text = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'placeholder':'Caption'}), label='', help_text="500 Word Limit")
    # Post Image Field
    media = forms.ImageField(label="Image", required=False)
    # User Field (To Link to User Account)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save(self, user, time):
        text = self.cleaned_data['text']
        media = self.cleaned_data['media']
        post = Post(user=user, post_date=time, caption=text,likes=0, image=media,)
        post.save()
