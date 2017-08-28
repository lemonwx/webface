import cv2, numpy
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import lsqr, lsmr

from lmutils import debug_info
from possion_utils import Utils

class possion():
    def __init__(self, prepic, bakpic, cp2pt, zone_width=20):
        """
        prepic: 
        bakpic:
        zone_width
        """