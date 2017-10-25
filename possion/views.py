from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ImgForm, TaskForm
from .models import *
from lmutils import debug_info
from .tasks.tasks import possion


# Create your views here.


class UploadView(View):
    def get(self, request):
        img_form = ImgForm()
        return render(request, "base.html", {'img_form': img_form})

    def post(self, request):
        img_form = ImgForm(request.POST, request.FILES)
        print(debug_info(), request.POST)
        if img_form.is_valid():
            img_form.save()
            return HttpResponseRedirect("/hello")
        return render(request, 'base.html', {'img_form': img_form})


class AddPossionTask(View):

    def get(self, request):
        imgs = Img.objects.all()
        return render(request, 'base.html', {'imgs': imgs})

    def post(self, request):
        print(debug_info(), request.POST)
        task_form = TaskForm(request.POST)
        print(debug_info(), task_form.is_valid())
        if task_form.is_valid():
            # 添加一个任务, 通过 celery 添加到后台运行
            pt = PossionTask()
            pt.pre_img_id = request.POST.get("pre_img_id")
            pt.bak_img_id = request.POST.get("bak_img_id")
            pt.user_id = 0
            pt.save()
            print(debug_info(), pt.id)
            # execure done. 保存到相应的目录, 更新数据库中的记录
            # pt.objects.update(tgt_img_path='target/{y}/{m}/task_{pt_id}.jpg'.format(year, month, pt.id))
            return  HttpResponse("add task success")
        else:
            return HttpResponseRedirect("add task error")


def test(request):
    pre = "/home/lim/workSpace/webface/possion/img/pre1.jpg"
    bak = "/home/lim/workSpace/webface/possion/img/bak.jpg"
    task = possion.delay(pre, bak, (500, 500))
    print(debug_info(), "send task done, {}".format(task.task_id))
    return HttpResponse("this is test page, {}".format(task.task_id))
