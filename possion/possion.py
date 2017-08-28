import cv2, numpy
from scipy.sparse import coo_matrix, csc_matrix
from numpy.linalg import solve, norm
from scipy.sparse.linalg import lsqr, lsmr, qmr

from lmutils import debug_info
from possion_utils import Utils

class possion():
    def __init__(self, prepic, bakpic, cp2pt, zone_width=20):
        """
        prepic: 
        bakpic:
        zone_width:
        """
        self.prepic = cv2.imread("{0}".format(prepic))
        self.bakpic = cv2.imread("{0}".format(bakpic))

        self.ph, self.pw, nchannel = self.prepic.shape
        self.bh, self.bw, nchannel = self.bakpic.shape

        print(debug_info(), self.prepic.shape)
        print(debug_info(), self.bakpic.shape)
        print(debug_info(), cp2pt)

        self.zone_width = zone_width
        self.cp2h, self.cp2w = cp2pt

        self.conAfromH = self.cp2h - zone_width
        self.conAfromW = self.cp2w - zone_width

        self.bh = self.cp2h + self.ph + zone_width
        self.bw = self.cp2w + self.pw + zone_width

        self.matAh = self.bh - self.conAfromH
        self.matAw = self.bw - self.conAfromW
        self.utils = Utils(self.conAfromH, self.conAfromW, self.bh, self.bw)

        self.row = list()
        self.col = list()

        self.data = list()

        self.matb = [list(), list(), list()]

        self.area = numpy.array([
            (self.cp2h, self.cp2w),
            (self.cp2h, self.cp2w + self.pw - 1),
            (self.cp2h + self.ph - 1, self.cp2w + self.pw  -1),
            (self.cp2h + self.ph - 1, self.cp2w)
            ])
        self.counts = {
            "horn":0,
            "bdy":0,
            "inner":0
        }

        self.bdylist = list()
        self.counts_ = {
            "1":0,
            "2":0,
            "3":0,
            "4":0,
            "5":0,
        }

    def __str__(self):
        return ""

    def __isinarea__(self, pt):
        #print(debug_info(), self.area)
        return cv2.pointPolygonTest(self.area, pt, 0)

    def __sparse_mat_set_v__(self, x, y, v):
        self.row.append(x)
        self.col.append(y)
        self.data.append(v)

    def __b_mat_set_v__(self, pic, pt, pt_list):

        #print(debug_info(), pt, pt_list)
        self.counts_[str(len(pt_list))] += 1
        tmp = [0, 0, 0]
        tmp[0] = pic[pt[0], pt[1]][0] * len(pt_list)
        tmp[1] = pic[pt[0], pt[1]][1] * len(pt_list)
        tmp[2] = pic[pt[0], pt[1]][2] * len(pt_list)
        #print(debug_info(), tmp, pic[1,165])

        for p in pt_list:
            tmp[0] -= pic[p[0], p[1]][0]
            tmp[1] -= pic[p[0], p[1]][1]
            tmp[2] -= pic[p[0], p[1]][2]
            #print(debug_info(), tmp)

        self.matb[0].append(tmp[0])
        self.matb[1].append(tmp[1])
        self.matb[2].append(tmp[2])

    def construct_mat(self):
        for j in range(self.conAfromH, self.bh):
            for i in range(self.conAfromW, self.bw):
                idx = (j-self.conAfromH) * self.matAw + i - self.conAfromW
                horn = self.utils.ishorn([j,i])
                if horn != -1:
                    #print(debug_info(), "horn", j, i)
                    self.bdylist.append([j,i])
                    self.counts['horn'] += 1
                    self.__sparse_mat_set_v__(idx, idx, 2)
                    self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromH)+(i-self.conAfromW)+horn[1], -1)
                    self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromH+horn[0])+(i-self.conAfromW), -1)

                    isina = self.__isinarea__((j,i))
                    if isina == 1:
                        self.__b_mat_set_v__(self.prepic, (j-self.cp2h, i-self.cp2w), [
                            (j+horn[0]-self.cp2h, i-self.cp2w),
                            (j-self.cp2h, i+horn[1]-self.cp2w)
                            ])
                    else:
                        self.__b_mat_set_v__(self.bakpic, (j, i), [
                            (j+horn[0], i),
                            (j, i+horn[1])
                            ])
                else:
                    bdy = self.utils.isbdy([j, i])
                    if bdy != -1:
                        #print(debug_info(), "bdy", j, i)
                        self.bdylist.append((j,i))
                        self.counts['bdy'] += 1
                        self.__sparse_mat_set_v__(idx, idx, 3)
                        for item in bdy[0]:
                            self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromH+item)+i-self.conAfromW, -1)
                        for item in bdy[1]:
                            self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromW)+i-self.conAfromW+item, -1)

                        isina = self.__isinarea__((j,i))

                        if isina == 1:
                            tmp1 = list((j+item-self.cp2h, i-self.cp2w) for item in bdy[0])
                            tmp2 = list((j-self.cp2h, i-self.cp2w+item) for item in bdy[1])

                            self.__b_mat_set_v__(self.prepic, (j-self.cp2h, i-self.cp2w), tmp1, tmp2)
                        else:
                            tmp1 = list((j+item, i) for item in bdy[0])
                            tmp2 = list((j+item, i) for item in bdy[1])

                            self.__b_mat_set_v__(self.bakpic, (j, i), tmp1+tmp2)
                    else:
                        #print(debug_info(), "inner", j, i)
                        self.__sparse_mat_set_v__(idx, idx, 4)
                        self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromH)+i-self.conAfromW-1, -1)
                        self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromH)+i-self.conAfromW+1, -1)
                        self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromH-1)+i-self.conAfromW, -1)
                        self.__sparse_mat_set_v__(idx, self.matAw*(j-self.conAfromH+1)+i-self.conAfromW, -1)

                        isina = self.__isinarea__((j,i))
                        if isina == 1:
                            #rint(debug_info(), "in in pic", j, i)
                            '''
                            print(debug_info(), "pre", [
                                (j-self.cp2h+1, i-self.cp2w),
                                (j-self.cp2h-1, i-self.cp2w),
                                (j-self.cp2h, i-self.cp2w+1),
                                (i-self.cp2h, i-self.cp2w-1)
                                ])
                                '''
                            self.__b_mat_set_v__(self.prepic, (j-self.cp2h, i-self.cp2w), [
                                (j-self.cp2h+1, i-self.cp2w),
                                (j-self.cp2h-1, i-self.cp2w),
                                (j-self.cp2h, i-self.cp2w+1),
                                (j-self.cp2h, i-self.cp2w-1)
                                ])
                        else:
                            '''
                            print(debug_info(), "bak", [
                                (j+1, i),
                                (j-1, i),
                                (j, i+1),
                                (j, i-1)
                                ])
                                '''
                            self.__b_mat_set_v__(self.bakpic, (j, i), [
                                (j+1, i),
                                (j-1, i),
                                (j, i+1),
                                (j, i-1)
                                ])

        index = 0
        for pt in self.bdylist:
            continue
            self.__sparse_mat_set_v__(index+self.matAw*self.matAh, (pt[0]-self.conAfromH)*self.matAw+pt[1]-self.conAfromW, 1)
            index += 1
            self.matb[0].append(self.bakpic[pt[0], pt[1]][0])
            self.matb[1].append(self.bakpic[pt[0], pt[1]][1])
            self.matb[2].append(self.bakpic[pt[0], pt[1]][2])
        #shape=(self.matAw*self.matAh, self.matAh*self.matAw)
        shape=(self.matAw*self.matAh+len(self.bdylist), self.matAh*self.matAw)
        print(debug_info(), (self.conAfromH, self.bh), (self.conAfromW, self.bw))
        print(debug_info(), len(self.row), len(self.col), len(self.data))
        x = [(x,y,z) for x,y,z in zip(self.row, self.col, self.data)]
        #print(debug_info(), x)
        print(debug_info(), max(self.row), max(self.col))
        print(debug_info(), shape, len(self.bdylist))

        #print(debug_info(), self.row)
        #print(debug_info(), self.col)
        #print(debug_info(), self.data)

        print(debug_info(), self.matAw*self.matAh)
        self.matA = coo_matrix( 
            (self.data, (self.row, self.col) ), 
            shape=(self.matAw*self.matAh, self.matAh*self.matAw)
            )
        print(debug_info(), self.counts_)

        #print(debug_info(), "\n", self.matA.toarray())

    def __normalization__(self, x):

        res = []
        for item in x:
            if item > 255:
                res.append(255)
            elif item < 0:
                res.append(0)
            else:
                res.append(item)
        return res

    def __save_img__(self, img, path):
        cv2.imwrite(path, img)

    def calc_x(self):
        
        from scipy.sparse.linalg import spsolve
        print(debug_info(), "START TRAN")
        #print(debug_info(), matA.toarray())
        #print(debug_info(), len(self.matb), self.matb)
        #x = spsolve(matA, self.matb[0])
        #print(debug_info(), "END TRAN")
        #tmp0 = lsqr(self.matA, self.matb[0])
        #print(debug_info(),  "R calc done.")
        #tmp1 = lsqr(self.matA, self.matb[1])
        #print(debug_info(),  "G calc done.")
        #tmp2 = lsqr(self.matA, self.matb[2])
        #print(debug_info(),  "B calc done.")

        #print(debug_info()) 
        #@for arr in matA.toarray():
        #    print(list(arr))
        #print(debug_info(), self.matA.shape())
        tmp0 = lsqr(self.matA, self.matb[0], show=True, atol=1.0e-9, btol=1.0e-9, calc_var=False)
        tmp1 = lsqr(self.matA, self.matb[1], show=True, atol=1.0e-9, btol=1.0e-9, calc_var=False)
        tmp2 = lsqr(self.matA, self.matb[2], show=True, atol=1.0e-9, btol=1.0e-9, calc_var=False)

        #print(debug_info() , tmp0)
        #print(debug_info() , self.matb[0])
        res = list(map(self.__normalization__, zip(tmp0[0], tmp1[0], tmp2[0])))
        

        print(debug_info(), self.ph, self.pw)
        print(debug_info(), self.cp2h, self.cp2w)

        for j in range(0, self.ph):
            for i in range(0, self.pw):
                self.bakpic[j+self.cp2h, i+self.cp2w] = self.prepic[j,i]

        self.__save_img__(self.bakpic, "cp2bak.jpg")

        for j in range(self.conAfromH, self.bh):
            for i in range(self.conAfromW, self.bw):
                self.bakpic[j,i] = (
                    res[(j-self.conAfromH)*self.matAw+i-self.conAfromW][0],
                    res[(j-self.conAfromH)*self.matAw+i-self.conAfromW][1],
                    res[(j-self.conAfromH)*self.matAw+i-self.conAfromW][2],
                    )

        self.__save_img__(self.bakpic, "autopossion.jpg")
