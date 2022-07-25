import threading
import cv2
from playsound import playsound
import mediapipe as mp
from mediapipe.python.solutions import hands
from mediapipe.framework.formats import landmark_pb2


def play_sound(id):
    global flagsounds

    flagsounds[id] = True
    playsound(f'sounds/{id}.wav')
    flagsounds[id] = False


def main():
    global flagsounds

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    flagsounds = [False, False, False, False, False]
    cap = cv2.VideoCapture(0)
    base_0 = base_1 = base_2 = base_3 = base_4 = -1
    counter = 0

    hands = mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
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
                keypoints.append({'X': data_point.x,
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
                if flagsounds[0] == False:
                    thread = threading.Thread(target=play_sound, args=[0])
                    thread.start()

            if base_1>abs(base.y-keypoints[1]['Y'])*1.3:
                if flagsounds[1] == False:
                    thread = threading.Thread(target=play_sound, args=[1])
                    thread.start()
                    
            if base_2>abs(base.y-keypoints[2]['Y'])*1.3:
                if flagsounds[2] == False:
                    thread = threading.Thread(target=play_sound, args=[2])
                    thread.start()
                
            if base_3>abs(base.y-keypoints[3]['Y'])*1.4:
                if flagsounds[3] == False:
                    thread = threading.Thread(target=play_sound, args=[3])
                    thread.start()
                
            if base_4>abs(base.y-keypoints[4]['Y'])*1.5:
                if flagsounds[4] == False:
                    thread = threading.Thread(target=play_sound, args=[4])
                    thread.start()
                        
        else:
            counter=0
    
        cv2.imshow('res',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
