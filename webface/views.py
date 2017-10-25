import random
import json
from django.http import HttpResponse
from proj import add_, possion as possion_
from lmutils import debug_info

def hello(request):
    nums1 = [1,2,3,4]
    nums2 = [5,6,7,8]
    print(debug_info(), request)
    return HttpResponse("123")


def t_add(request):
    a = random.randint(0, 10)
    b = random.randint(0, 10)
    task = add_.delay(a, b)
    return HttpResponse("add task_add to jd vps's celery done. {}+{}--task_id:{}".format(a, b, task.task_id))

'''
def possion(request):
    task = possion1_.delay(10, 11)
    print(debug_info(), task.task_id)
    # tm = task_mode.save()
    # tm.task_id = task.task_id
    # tm.save()
    return HttpResponse("add possion task to remote celery done, {}".format(task.task_id))
'''

def get_possion_res(request):
    '''
    import redis
    conn = redis.Connection(host='')
    conn.send_command("get {}".format(request.GET.get('task', '')))
    res = conn.read_response()
    res = json.loads(res.decode())

    tm = task_mode.objects.filter(id=task_id)
    tm.status = res['status']
    tm.path = '///...'
    tm.save()
    return render(request, 'task_status.html',
                {'status': tm.status,
                 'tgt_path': tm.path,
                 'tgt'})
    '''

    return HttpResponse("this is page get possion res")
