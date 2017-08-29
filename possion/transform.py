import cv2
pic = cv2.imread("{0}".format("pre.jpg"))
h, w, _ = pic.shape
print(h, w)
dst = cv2.resize(pic, (int(w/5), int(h/5)), interpolation=cv2.INTER_CUBIC)
cv2.imwrite("transform.jpg", dst)
