from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django import forms
from django.views.generic import View
from crm.models import Employee

class RegistratinForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"})
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model=Employee
        fields="__all__"
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "department":forms.TextInput(attrs={"class":"form-control"}),
            "gender":forms.Select(attrs={"class":"form-select"}),
            "salary":forms.NumberInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
            "address":forms.Textarea(attrs={"class":"form-control","rows":2})

        }


class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))  


class EmployeeCreateView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeeForm()
        return render(request,"emp-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=EmployeeForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("emp-list")
        return render(request,"emp-add.html",{"form":form})

class EmployeeListView(View):
    def get(self,request,*args,**kwargs):
        form=EmployeeForm()
        qs=Employee.objects.all()
        return render(request,"emp-list.html",{"employees":qs})


class EmployeeDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("ps")
        qs=Employee.objects.get(id=id).delete()
        return redirect("emp-list")
    
class EmployeeDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("ps")
        qs=Employee.objects.get(id=id)
        return render(request,"emp-detail.html",{"employee":qs})
    
class EmployeeEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("ps")
        emp=Employee.objects.get(id=id)
        form=EmployeeForm(instance=emp)
        return render(request,"emp-edit.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("ps")
        emp=Employee.objects.get(id=id)
        form=EmployeeForm(instance=emp,data=request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect("emp-detail",ps=id)
        return render(request,"emp-edit.html",{"form":form})


#registration form

class SignUpview(View):
    def get(self,request,*args,**kwargs):
        form=RegistratinForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistratinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"signup successfully")
            return redirect("signin")
        messages.error(request,"signup has been failed")
        return render(request,"register.html",{"form":form})
   
class SignInView(View):
     def get(self,request,*args,**kwargs):
         form=LoginForm()
         return render(request,"login.html",{"form":form})  
     def post(self,request,*args,**kwargs):
         form=LoginForm(request.POST)
         if form.is_valid():
             uname=form.cleaned_data.get("username")
             pwd=form.cleaned_data.get("password")
             usr=authenticate(request,username=uname,password=pwd)
             if usr:
                 login(request,usr)
                 messages.success(request,"login successfully")             
                 return redirect("todo-list")
         messages.error(request,"invalid candidate")
         return render(request,"login.html",{"form":form}) 
     

#function based view

def signout_view(request,*args,**kwargs):
    logout(request)
    return redirect("signin")     