import cv2
pic = cv2.imread("{0}".format("pre4.jpg"))
h, w, _ = pic.shape
print(h, w)
dst = cv2.resize(pic, (int(w/50), int(h/50)), interpolation=cv2.INTER_CUBIC)
cv2.imwrite("transform.jpg", dst)
