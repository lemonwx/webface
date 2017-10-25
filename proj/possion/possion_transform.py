import datetime
import time

def possion_transform():
	time.sleep(300)
	print("this task is running on jd vps by celery, call by remote django")
	return datetime.datetime.now()
