from django.http import HttpResponse

from lmutils import debug_info

def hello(request):
    nums1 = [1,2,3,4]
    nums2 = [5,6,7,8]
    print(debug_info(), request)
    return HttpResponse("123")