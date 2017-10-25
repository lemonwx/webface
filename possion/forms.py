from .models import Img, PossionTask
from django import forms


class ImgForm(forms.ModelForm):
    class Meta:
        model = Img
        fields = ["title", "image", "add_time"]


'''
class ImgForm(forms.Form):
    title = forms.CharField(required=True)
    image = forms.ImageField(required=True)
'''

'''
class TaskForm(forms.ModelForm):
    class Meta:
        model = PossionTask
        fields = ["pre_img_id", "bak_img_id", "user_id", "tgt_img_path"]
'''

class TaskForm(forms.Form):
    pre_img_id = forms.IntegerField(required=True)
    bak_img_id = forms.IntegerField(required=True)