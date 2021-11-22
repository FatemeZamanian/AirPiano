import math
import cv2
from playsound import playsound
import mediapipe as mp
from mediapipe.python.solutions import hands
from mediapipe.framework.formats import landmark_pb2

import beepy

# import required module
from beeply.notes import *

# Creating obj of beeply
# It's has another arg of duration
# By default it's 900 ms
a = beeps()

# It's has another arg of duration
# By default it's 900 ms
a.hear('A_')


print("Done ")

# To acknowledge us
a.hear("A")




mp_drawing=mp.solutions.drawing_utils
mp_hands=mp.solutions.hands


cap=cv2.VideoCapture(0)
base_0=base_1=base_2=base_3=base_4=-1
counter=0
flagsound=False
with hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        ret,frame=cap.read()
        image=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        image.flags.writeable=False

        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        h, w, c = image.shape

        if results.multi_hand_landmarks:
            counter+=1
            landmark_subset = landmark_pb2.NormalizedLandmarkList(landmark = [
            results.multi_hand_landmarks[0].landmark[4],
            results.multi_hand_landmarks[0].landmark[8], 
            results.multi_hand_landmarks[0].landmark[12],
            results.multi_hand_landmarks[0].landmark[16],
            results.multi_hand_landmarks[0].landmark[20],])
            mp_drawing.draw_landmarks(image,landmark_list=landmark_subset)

            base=results.multi_hand_landmarks[0].landmark[0]
            keypoints = []
            for data_point in landmark_subset.landmark:
                keypoints.append({
                                    'X': data_point.x,
                                    'Y': data_point.y,
                                    'Z': data_point.z
                                    })
        
            if counter==5:
                base_0=abs(base.x-keypoints[0]['X'])
                base_1=abs(base.y-keypoints[1]['Y'])
                base_2=abs(base.y-keypoints[2]['Y'])
                base_3=abs(base.y-keypoints[3]['Y'])
                base_4=abs(base.y-keypoints[4]['Y'])
                cv2.putText(image,'Your hand saved...',(100,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)


            if base_0>abs(base.x-keypoints[0]['X'])*1.3 and base_0<abs(base.x-keypoints[0]['X'])*1.6:
                # temp=[]
                # temp.append(results.multi_hand_landmarks[0].landmark[4])
                if flagsound==False:
                    # playsound(r'sounds/1.wav')
                    # beepy.beep(sound=1)
                    a = beeps(1154)
                    flagsound=True
                    print(11111)
                
                else:
                    flagsound=False
                
                # mp_drawing.draw_landmarks(image,mp_drawing.DrawingSpec(color=(102,0,204),thickness=10,circle_radius=10),mp_drawing.DrawingSpec(color=(102,0,204),thickness=10,circle_radius=10),landmark_list=temp)

                # cv2.circle(image,(int(keypoints[0]['X']*100)+w, int(keypoints[0]['Y']*100)+h),radius=5, color=(255, 0, 255),thickness= cv2.FILLED)
                
            if base_1>abs(base.y-keypoints[1]['Y'])*1.3:
                if flagsound==False:
                    playsound(r'sounds/6.wav')
                    flagsound=True
                    print(2222)
                
                else:
                    flagsound=False
               
            if base_2>abs(base.y-keypoints[2]['Y'])*1.3:
                if flagsound==False:
                    playsound(r'sounds/3.wav')
                    flagsound=True
                    print(3333)
                
                else:
                    flagsound=False
                
            if base_3>abs(base.y-keypoints[3]['Y'])*1.4:
                if flagsound==False:
                    playsound(r'sounds/4.wav')
                    flagsound=True
                    print(4444)
                
                else:
                    flagsound=False
                
            if base_4>abs(base.y-keypoints[4]['Y'])*1.5:
                if flagsound==False:
                    playsound(r'sounds/5.wav')
                    flagsound=True
                    print(5555)
                
                else:
                    flagsound=False
                
        else:
            counter=0
    
        cv2.imshow('res',image)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()