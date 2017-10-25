from __future__ import absolute_import
from proj.celery import app
from proj.possion import possion_transform
from lmutils import debug_info


@app.task
def add1(x, y):
    print("this is jd cloud's vps celery server")
    return x+y


