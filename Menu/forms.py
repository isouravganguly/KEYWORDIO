from django import forms
from django.forms import ModelForm
from .models import book, librarian

e=librarian.objects.all()
OPTIONne= [tuple([x.Name,x.Name]) for x in e]
p=book.objects.all()
OPTIONnp= [tuple([x.Name,x.Name]) for x in p]
OPTIONc= [tuple([x.subject,x.subject]) for x in p]
OPTIONco= [tuple([x.author,x.author]) for x in p]

class loginform(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)

class signupform(forms.Form):
    username = forms.CharField(max_length=20)
    first_name= forms.CharField(max_length=20)
    last_name= forms.CharField(max_length=20)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    email= forms.EmailField(max_length=50)

class createProForm(ModelForm):
    class Meta:
        model = book
        fields = ['Name', 'subject', 'Quantity', 'author']

class createEmpForm(ModelForm):
    class Meta:
        model = librarian
        fields = ['Name','EmpID','email']


class searchEmpForm(forms.Form):
    Name= forms.ChoiceField(choices=OPTIONne)

class searchProForm(forms.Form):

    Name= forms.CharField(label='Book Name:', widget=forms.Select(choices=OPTIONnp))
    subject= forms.CharField(label='Book subject:', widget=forms.Select(choices=OPTIONc))
    author= forms.CharField(label='Book author:', widget=forms.Select(choices=OPTIONco))
    