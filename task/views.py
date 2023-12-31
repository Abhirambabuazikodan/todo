
from django.shortcuts import render,redirect
from django.views.generic import View
from django import forms
from task.models import Todos
from django.contrib import messages

class TodoForm(forms.Form):
    task_name=forms.CharField()
   # user=forms.CharField()

class TodoCreateView(View):
    def get(self,request,*args,**kwargs):
        form=TodoForm()
        return render(request,"todo-add.html",{"forms":form})
    def post(self,request,*args,**kwargs):
        form=TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Todos.objects.create(**form.cleaned_data,user=request.user)
            messages.success(request,"todo has been created successfully")
            return redirect("todo-list")
        messages.error(request,"fail to create todo")
        return render(request,"todo-add.html",{"form":form}) 
    
class TodoListView(View):
    def get(self,request,*args,**kwargs):
        qs=Todos.objects.filter(status=False,user=request.user).order_by("-date")
        return render(request,"todo-list.html",{"todos":qs}) 

class TodoUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Todos.objects.filter(id=id).update(status=True)
        messages.success(request,"todo has been changed")
        return redirect("todo-list")
    
class TodoComplitedView(View):
    def get(self,request,*args,**kwargs):
    
        qs= Todos.objects.filter(status=True).order_by("-date")
        return render(request,"todo-complete.html",{"todos":qs})
            

class TodoDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("ps")
        qs=Todos.objects.get(id=id)

        return render(request,"todo-detail.html",{"todo":qs}) 
    
class TodoDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Todos.objects.get(id=id).delete()
        messages.success(request,"todo has been removed successfully")
        return redirect("todo-list")    
       



