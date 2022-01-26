from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import UserAddress , MyUser

User = settings.AUTH_USER_MODEL



class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields =["reciver_name" , "address" ,
                 "address2" ,
                 "city" ,
                 "state" ,
                 "country" ,
                 "zipcode" ]
    def __init__(self, *args, **kwargs):
        super(UserAddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})




class LoginFrom(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget= forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super(LoginFrom, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'input100' })
        self.fields['password'].widget.attrs.update({'class' : 'input100' })


    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = MyUser.objects.get(username = username)
        except:
            raise forms.ValidationError("Username Entered is incorrect!")
        return username


    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            user = MyUser.objects.get(username = username)
        except:
            user = None
        if user is not None and not user.check_password(password):
            raise forms.ValidationError("Password Entered is invalid!")
        elif user is None:
            pass
        else:
            return password





class RegisterationForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password' , widget= forms.PasswordInput() )
    password2 = forms.CharField(label='Password Confirmation' , widget= forms.PasswordInput())
    class Meta:
        model = MyUser
        fields = ['username', 'IC' ,'first_name', 'last_name' ,'email' , 'phone']

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        self.fields['IC'].label = "IC Number"
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'input100'})


    def clean_email(self):
        email = self.cleaned_data.get("email")
        user_count = MyUser.objects.filter(email = email).count()
        if user_count > 0:
            raise forms.ValidationError("Email is already used!")
        return email


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and  password1 != password2:
            raise forms.ValidationError("Passwords Do Not Match!!")
        else:
            return password2


    def save(self , commit = True):
        user = super(RegisterationForm , self).save(commit = False)
        user.set_password(self.cleaned_data['password2'])
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ["username",
                 "first_name" ,
                 "last_name" ,
                 "email",
                 "phone"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields =["address" ,
                 "address2" ,
                 "city" ,
                 "state" ,
                 "country" ,
                 "zipcode" ]

    def __init__(self, *args, **kwargs):
        super(AddressUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})
