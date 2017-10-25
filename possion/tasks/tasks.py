from webface.celery import app
import time
from .possion import possion as possion_alg


@app.task
def possion(pre_pic, bak_pic, cp2pt=(500, 500)):
    p = possion_alg(pre_pic, bak_pic, cp2pt)
    p.construct_mat()
    p.calc_x()
    return "success"

