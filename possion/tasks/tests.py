# Create your tests here.
import sys

from django.test import TestCase

from possion import possion

try:
	t = (int(sys.argv[1]), int(sys.argv[2]))
except Exception as e:
	t = (600, 600)

# p = possion("transform.jpg", "bak.jpg", t)

p = possion("pre4.jpg", "bak.jpg", t)
p.construct_mat()
p.calc_x()
