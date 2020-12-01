import sys
import os
import cv2
import dlib

if len(sys.argv) == 2 and sys.argv[1].isnumeric():
    cap = cv2.VideoCapture(0)
    cascade = cv2.CascadeClassifier("haarcascade.xml")
    tracker = dlib.correlation_tracker()
    trackingFace = 0
    while True:
        ret,frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5, minSize=(85, 85)) # More numbers...
        if not ret:
            print("Unkown Error!")
        if not trackingFace:
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x + w,y + h),(255,0,0),2)
                cv2.putText(frame,"Face",(x,y - 20),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
                tracker.start_track(frame,dlib.rectangle(x,y,x+w,y+h))
                trackingFace = 1
        else:
            trackingQuality = tracker.update(frame)
            if trackingQuality >= 8.75: # TQ
                tracked_position =  tracker.get_position()
                t_x = int(tracked_position.left())
                t_y = int(tracked_position.top())
                t_w = int(tracked_position.width())
                t_h = int(tracked_position.height())
                cv2.rectangle(frame, (t_x, t_y),
                                    (t_x + t_w , t_y + t_h),
                                    (0,255,0) ,2)
                cv2.putText(frame,"Face (Confidinse {}%)".format(round(trackingQuality)),(t_x,t_y - 20),cv2.FONT_HERSHEY_SIMPLEX,1,(0,225,0),2)
            else:
                trackingFace = 0
        cv2.imshow("Camera (Channel : "+sys.argv[1]+")",frame)
        k = cv2.waitKey(int(sys.argv[1])) & 0xFF
        if k == 27:
            break
else:
    print("Error: Argument error: Must Be called like \"python3 "+str(sys.argv[0])+" <arg[NAME:Latency,TYPE:NUMBER]>\"")
    exit
cv2.destroyAllWindows()
exit