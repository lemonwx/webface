from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^upload/$', UploadView.as_view(), name="upload"),
    url(r'^addpossiontask/$', AddPossionTask.as_view(), name="add_possion_task"),
    url(r'^test/$', test, name="test"),
]
