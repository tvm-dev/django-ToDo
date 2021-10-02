from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import TaskForm
from .models import Task
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import datetime

@login_required
def taskList(request):

    search = request.GET.get('search')
    filter = request.GET.get('filter')
    #Tasks recently
    tasksDoneRecently = Task.objects.filter(done='done', updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30), user=request.user).count()
    #tasksDoneRecently = Task.objects.filter(done='done', updated_at__gt=datetime.datetime.now()-datetime.timedelta(days=30)).count()
    
    #Tasks Done
    tasksDone = Task.objects.filter(done='done', user=request.user).count()
    
    #Tasks Doing
    tasksDoing = Task.objects.filter(done='doing', user=request.user).count()
 
    if search:
        tasks = Task.objects.filter(title__icontains=search, user=request.user) 
        return render(request, 'tasks/list.html', {'tasks': tasks})
    

    elif filter:
        tasks = Task.objects.filter(done=filter, user=request.user)
        return render(request, 'tasks/list.html', {'tasks': tasks})
        

    else:
        #To get all datas of database:
        tasks_list = Task.objects.all().order_by('-created_at').filter(user=request.user)

        paginator = Paginator(tasks_list, 3)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
        return render(request, 'tasks/list.html', {'tasks': tasks, 'tasksrecently': tasksDoneRecently, 'tasksdone': tasksDone, 'tasksdoing': tasksDoing})
@login_required
def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task': task})


@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            return redirect ('/')

    else:
            form = TaskForm()    
            return render(request, 'tasks/addtask.html', {'form': form } )
@login_required
def editTask(request, id):
    #create a variable, rescue the task and id from db
    task = get_object_or_404(Task, pk=id)
    #rescue form to edit then
    form = TaskForm(instance=task) #for pre-popule the form for future edition

    if (request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if (form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html', {'form': form, 'task': task})        


    else:
        return render(request, 'tasks/edittask.html', {'form': form, 'task': task})    

@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()

    messages.info(request, 'Success deleted task ')

    return redirect('/')

@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)

    if (task.done == 'doing'):
        task.done = 'done'
    else:
        task.done = 'doing'
    
    task.save()
    return redirect('/')


def helloworld(request):
    return HttpResponse('Hello World!')



def yourName(request, name):
    return render(request, 'tasks/yourname.html', {'name': name})




