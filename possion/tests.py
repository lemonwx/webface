from django.test import TestCase

# Create your tests here.
import sys
from possion import possion

try:
	t = (int(sys.argv[1]), int(sys.argv[2]))
except Exception as e:
	t = (500, 500)

p = possion("transform.jpg", "bak.jpg", t)
p.construct_mat()
p.calc_x()

