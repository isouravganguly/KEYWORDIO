from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import createProForm, createEmpForm, searchEmpForm, searchProForm, signupform, loginform
from .models import book,librarian
from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date, datetime
from rest_framework.views import APIView
from rest_framework.response import response
from rest_framework import status
from .serializer import bookSerializer

import smtplib

# Create your views here.
def home(request):
    return render(request, 'home.html')

def Base(request):
    return render(request, 'Basic.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('/home')
    if (request.method=='POST'):
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            return redirect('/home')
        else:
            messages.error(request, "Data seems invalid")
            return render(request,'signup.html',{'form':form})
     
    else:
        form = UserCreationForm()
        return render(request,'signup.html',{'form':form})
        

def signin(request):
    if request.user.is_authenticated:
        return redirect('/home')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            form = AuthenticationForm()
            return render(request,'signin.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('/signin/')

class booklist(APIView):
    def get(self,request):
        books=book.objects.all()
        serializer= bookSerializer(books, many=True)
        return Response(serializer.data)
        
def createpro(request):
    if request.method=='POST':
        form = createProForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['Name']
            subject = form.cleaned_data['subject']
            quantity = form.cleaned_data['Quantity']
            author = form.cleaned_data['author']
            addedOn = date.today()

        p= book.objects.create(Name=name, subject=subject, addedOn=addedOn, Quantity=quantity, author=author)
        p.save()

    form = createProForm()

    return render(request, 'createPro.html', {'form': form})

def createemp(request):
    if request.method=='POST':
        form = createEmpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['Name']
            empID = form.cleaned_data['EmpID']
            email= form.cleaned_data['email']
            
        e= librarian.objects.create(Name=name, EmpID=empID, email=email)
        e.save()
        s = smtplib.SMTP('smtp.gmail.com', 587)
  
# start TLS for security
        s.starttls()
# Authentication
        s.login("dummy.mail.hain@gmail.com", "skyishigh100!")
# message to be sent
        message = "Welcome to the BCCL Resource Management System. Now you can see all details about the book on our website... Use your special Username and Password to start the journey. \n\n  Password- dummypass\n  Username- " + name.replace(" ", "")+str(empID)
        
        print(message)
# sending the mail
        s.sendmail("dummy.email.hain@gmail.com", email, message)
# terminating the session
        s.quit()
    form = createEmpForm()

    return render(request, 'createEmp.html', {'form': form})


def viewEmpList(request):
    if request.method=='POST':
        form = searchEmpForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data.get('Name')
            d= e= librarian.objects.all()
            if( name != 'All'):
                e= librarian.objects.filter(Name=name)
            e= [ i for i in e ]
    else:
        form = searchEmpForm()
        e= librarian.objects.all()
        u= User.objects.all()
        
    context= {'form':form,
                'e' : e,
                   }
    return render(request, 'viewEmpList.html', context=context)

def empUpdate(request, pk):
    if not request.user.is_superuser:
        return redirect('index')
    obj = librarian.objects.get(id=pk)
    form = createEmpForm(instance=obj)
    if request.method == 'POST':
        form = createEmpForm(data=request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('base')
    return render(request, 'createEmp.html', locals())



def empdel(request, pk):
    obj = librarian.objects.get(id=pk)
    obj.delete()
    return redirect('base')



def viewProList(request):
    if request.method=='POST':
        form = searchProForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = form.cleaned_data['Name']
            subject = form.cleaned_data['subject']
            author = form.cleaned_data['author']
            
            p= book.objects.all()
            if( name != 'Show All Data'):
                n= book.objects.filter(Name=name)
            else: n=book.objects.all()

            if(subject != 'Show All Data'):
                c= book.objects.filter(subject=subject)
            else: c=book.objects.all()

            if(author != 'Show All Data'):
                co= book.objects.filter(author=author)
            else: co=book.objects.all()

            p= [ i for i in p if i in n if i in c if i in co]
            
    else:
        form = searchProForm()
        p= book.objects.all()
    
    context= {'form':form,
                'p' : p    }
    return render(request, 'viewProList.html', context=context)