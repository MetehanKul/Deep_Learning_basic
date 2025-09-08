import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX    

while  cap.isOpened():
    rval, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 1.5, 1.5)
    edge = cv2.Canny(blur, 0, 50, 3)
    contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    try: hierarchy = hierarchy[0]
    except: hierarchy = []
    for contour, hier in zip(contours, hierarchy):
        (x,y,w,h) = cv2.boundingRect(contour)
        if (w >= 150 and h >= 150):
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, ('width = %d, height = %d' % (w, h)),
                        (x, y), font, 1, (0, 255, 0), 2, cv2.LINE_AA)


    cv2.imshow('Lines', frame)
    c = cv2.waitKey(1)  
    if c == 27 or c ==10:
         break

cap.release() 
cv2.destroyAllWindows()

while True:
    _, frame = cap.read()

    frame = frame[0:350, 15:540]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 3)

    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY|cv2.THRESH_TRIANGLE)

    kernel = np.ones((5,5),np.uint8)

    dilation = cv2.erode(threshold,kernel,iterations = 1)

    contours,_ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for (i,c) in enumerate(contours):
        (x,y,w,h) = cv2.boundingRect(c)
        area = cv2.contourArea(c)

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2, cv2.LINE_AA)
        cmY = (h*15)/120
        cmX = (w*10)/71
        cv2.putText(frame, str(int(cmY)), (x, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255),1)
        cv2.putText(frame, str(int(cmX)), (x+w+15, y+h+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255),1)

        # Çap ölçümü ekle
        (x_c, y_c), radius = cv2.minEnclosingCircle(c)
        diameter = radius * 2
        # Pikselden cm'ye çevirmek için örnek bir oran (w*10/71 gibi), burada w genişlikti.
        # Aynı oranı çap için de kullanabilirsin:
        cmDiameter = (diameter * 10) / 71
        cv2.circle(frame, (int(x_c), int(y_c)), int(radius), (255, 0, 0), 2)
        cv2.putText(frame, f"Cap: {cmDiameter:.1f}cm", (int(x_c), int(y_c)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)

    cv2.imshow("Frame", frame)


    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()