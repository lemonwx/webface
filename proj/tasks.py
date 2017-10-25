from __future__ import absolute_import
from proj.celery import app
from proj.possion import possion_transform

@app.task
def add(x, y):
	print("this is jd cloud's vps celery server")
	return x+y
@app.task
def possion(x, y):
	possion_transform()

