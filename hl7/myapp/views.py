from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from myapp.forms import CreateForm, EditForm, CreateRoadMap, AnotherCreateForm
from django.views.decorators.csrf import csrf_exempt
from .models import Task, RoadMap, Scores
from django.db import transaction
import datetime


@csrf_exempt
def show_tasks(request):
    tasks = Task.objects.all()
    ctx = {'titles': tasks}
    return render_to_response('tasks.html', ctx)


@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        instance = get_object_or_404(RoadMap, rd_id=request.POST.get('road_map'))
        a = Task(title=request.POST.get('title'),
                 estimate=request.POST.get('estimate'),
                 road_map=instance)
        a.save()
        return HttpResponseRedirect('/tasks/')
    form = CreateForm()
    return render_to_response('form1.html', {'form': form})


@csrf_exempt
def edit_task(request, context):
    instance = get_object_or_404(Task, my_id=context)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/roadmaps/')
    else:
        form = EditForm(instance=instance)
    return render_to_response('form2.html', {'form': form})


@csrf_exempt
def delete_task(request, context):
    get_object_or_404(Task, my_id=context).delete()
    return start(request)


@csrf_exempt
def start(request):
    return render_to_response('start_page.html')


@csrf_exempt
def create_roadmap(request):
    if request.method == 'POST':
        a = RoadMap(rd_id=request.POST.get('rd_id'), name=request.POST.get('name'))
        a.save()
        return HttpResponseRedirect('/start_page/')
    form = CreateRoadMap()
    return render_to_response('create_roadmap.html', {'form': form})


@csrf_exempt
def delete_roadmap(request, context):
    get_object_or_404(RoadMap, rd_id=context).delete()
    return start(request)


@csrf_exempt
def roadmaps(request):
    roads = RoadMap.objects.all()
    ctx = {'roads': roads}
    return render_to_response('roadmaps.html', ctx)


@csrf_exempt
def roadmap(request, context):
    tasks = Task.objects.filter(road_map=context)
    ctx = {'titles': tasks, 'context': context}
    return render_to_response('tasks_in_roadmap.html', ctx)


@csrf_exempt
def add_to_roadmap(request, context):
    if request.method == 'POST':
        a = Task(title=request.POST.get('title'),
                 estimate=request.POST.get('estimate'),
                 road_map_id=str(context)
                 )
        a.save()
        return roadmap(request, context)
    form = AnotherCreateForm()
    return render_to_response('form1.html', {'form': form, 'context': context})

@csrf_exempt
@transaction.atomic(savepoint=False)
def created_and_solved(request, context):
    tasks = Task.objects.filter(road_map=context)
    created = {}
    solved = {}
    for day in tasks:
        key = day.create_date.isocalendar()[1]
        if key not in created:
            list = []
            list.append(day.create_date)
            created[key] = []
            created[key].append(list)
            if day.state == 'ready':
                zn = 1
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
            else:
                zn = 0
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
        else:
            flag = False
            for i in range(len(created[key])):
                if day.create_date.isocalendar()[0] == created[key][i][0].isocalendar()[0]:
                    created[key][i].append(day.create_date)
                    flag = True
                    break
            if flag == True:
                if day.state == 'ready':
                    solved[key][i][0] = solved[key][i][0] + 1
                continue
            list = []
            list.append(day.create_date)
            created[key] = []
            created[key].append(list)
            if day.state == 'ready':
                zn = 1
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
            else:
                zn = 0
                sp = [zn]
                solved[key] = []
                solved[key].append(sp)
    my_dict = {}
    for key in created:
        spis = []
        for ind in range(len(created[key])):
            spis.append(first_and_last_day_in_week(created[key][ind][0]))
        my_dict[key] = spis
    created_end = {}
    for key in created:
        spis = []
        for ind in range(len(created[key])):
            spis.append(len(created[key][ind]))
        created_end[key] = spis
    for key in solved:
        spis = []
        for ind in range(len(solved[key])):
            spis.append(solved[key][ind][0])
        solved[key] = spis
    ctx = {'ctx': get_table(my_dict, created_end, solved)}
    return render_to_response('Stat1.html', ctx)

@csrf_exempt
@transaction.atomic(savepoint=False)
def points(request, context):
    tasks = Task.objects.filter(road_map=context)
    diff = calculate_max_estimate(tasks)
    for values in tasks:
        a = Scores(task_id=values.my_id, points=calculate_points(values, diff))
        a.save()
    point = Scores.objects.all()
    res = {}
    for key in point:
        year = key.date.strftime("%Y")
        month = key.date.strftime("%m")
        string = year + "-" + month
        if string not in res:
            res[string] = key.points
        else:
            res[string] = res[string] + key.points
    Scores.objects.all().delete()
    return render_to_response('points.html', {"res": res})



def calculate_points(self,max_estimate):
    if self.state == "ready":
        points=((datetime.date.today() - self.create_date) / (self.estimate - self.create_date)) + (
            (self.estimate - self.create_date) / max_estimate)
        return points
    else:
        return 0

def get_table(my_dict, created_end, solved):
    result = {}
    for key in my_dict:
        list = []
        for ind in range(len(my_dict[key])):
            list.append(my_dict[key][ind])
            list.append(created_end[key][ind])
            list.append(solved[key][ind])
        result[key] = list
    return result


def first_and_last_day_in_week(value):
    monday = value - datetime.timedelta(datetime.datetime.weekday(value))
    sunday = value + datetime.timedelta(6 - datetime.datetime.weekday(value))
    sunday = sunday.strftime("%Y-%m-%d")
    monday = monday.strftime("%Y-%m-%d")
    a = monday + "-" +sunday
    return a


def calculate_max_estimate(tmp):
    maximum = datetime.date.today() - datetime.date.today()
    for x in tmp:
        value = x.estimate - x.create_date
        if value > maximum:
            maximum = value
    return maximum
