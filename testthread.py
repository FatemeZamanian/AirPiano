import cv2
import time

from threading import Thread
from cv2 import VideoCapture

from playsound import playsound
import mediapipe as mp
from mediapipe.python.solutions import hands
from mediapipe.framework.formats import landmark_pb2


mp_drawing=mp.solutions.drawing_utils
mp_hands=mp.solutions.hands

base_0=base_1=base_2=base_3=base_4=-1
counter=0
flagsound=False





# defining a helper class for implementing multi-threading 
class WebcamStream :
    # initialization method 
    def __init__(self, stream_id=0):
        self.stream_id = stream_id # default is 0 for main camera 
        
        # opening video capture stream 
        self.vcap      = VideoCapture(self.stream_id)
        if self.vcap.isOpened() is False :
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5)) # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))
            
        # reading a single frame from vcap stream for initializing 
        self.grabbed , self.frame = self.vcap.read()
        if self.grabbed is False :
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False 
        self.stopped = True
        # thread instantiation  
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True # daemon threads run in background 
        
    # method to start thread 
    def start(self):
        self.stopped = False
        self.t.start()
    # method passed to thread to read next available frame  
    def update(self):
        while True :
            if self.stopped is True :
                break
            self.grabbed , self.frame = self.vcap.read()
            if self.grabbed is False :
                print('[Exiting] No more frames to read')
                self.stopped = True
                break 
        self.vcap.release()
    # method to return latest read frame 
    def read(self):
        return self.frame
    # method to stop reading frames 
    def stop(self):
        self.stopped = True

# initializing and starting multi-threaded webcam input stream 
webcam_stream = WebcamStream(stream_id=0) # 0 id for main camera
webcam_stream.start()
# processing frames in input stream
num_frames_processed = 0 
start = time.time()
with hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5) as hands:
    while True :
        if webcam_stream.stopped is True :
            break
        else :
            frame = webcam_stream.read()
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
                    t1=Thread(playsound(r'sounds/1.wav'))
                    # beepy.beep(sound=1)
                    # a = beeps(1154)
                    flagsound=True
                    t1.start()
                    print(11111)
                    # t1.join()
                
                else:
                    flagsound=False
                
                # mp_drawing.draw_landmarks(image,mp_drawing.DrawingSpec(color=(102,0,204),thickness=10,circle_radius=10),mp_drawing.DrawingSpec(color=(102,0,204),thickness=10,circle_radius=10),landmark_list=temp)

                # cv2.circle(image,(int(keypoints[0]['X']*100)+w, int(keypoints[0]['Y']*100)+h),radius=5, color=(255, 0, 255),thickness= cv2.FILLED)
                
            if base_1>abs(base.y-keypoints[1]['Y'])*1.3:
                if flagsound==False:
                    t2=Thread(playsound(r'sounds/6.wav'))
                    flagsound=True
                    t2.start()
                    print(2222)
                    # t2.join()
                
                else:
                    flagsound=False
               
            if base_2>abs(base.y-keypoints[2]['Y'])*1.3:
                if flagsound==False:
                    t3=Thread(playsound(r'sounds/3.wav'))
                    flagsound=True
                    t3.start()
                    print(3333)
                    # t3.join()
                
                else:
                    flagsound=False
                
            if base_3>abs(base.y-keypoints[3]['Y'])*1.4:
                if flagsound==False:
                    t4=Thread(playsound(r'sounds/4.wav'))
                    flagsound=True
                    t4.start()
                    print(4444)
                    # t4.join()
                
                else:
                    flagsound=False
                
            if base_4>abs(base.y-keypoints[4]['Y'])*1.5:
                if flagsound==False:
                    t5=Thread(playsound(r'sounds/5.wav'))
                    t5.start()
                    flagsound=True
                    # t5.join()
                    print(5555)
                
                else:
                    flagsound=False
            else:
                counter=0
        # adding a delay for simulating video processing time 
        delay = 0.03 # delay value in seconds
        time.sleep(delay) 
        num_frames_processed += 1

        # displaying frame 
        cv2.imshow('frame' , image)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break
end = time.time()
webcam_stream.stop() # stop the webcam stream

# printing time elapsed and fps 
elapsed = end-start
fps = num_frames_processed/elapsed 
print("FPS: {} , Elapsed Time: {} ".format(fps, elapsed))
# closing all windows 
cv2.destroyAllWindows()