import mediapipe as mp
import cv2
import time




class handdetector():
    def __init__(self):
        self.mphands = mp.solutions.hands
        self.hnds = self.mphands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findhands(self,img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hnds.process(imgRGB)

        if self.results.multi_hand_landmarks :
            for handlms in self.results.multi_hand_landmarks :
                self.mpDraw.draw_landmarks(img, handlms, self.mphands.HAND_CONNECTIONS)
               
                            
        return img

    def findList(self, img):
        lmlist1 = []
        lmlist2 = []
        if self.results.multi_hand_landmarks :
            rhand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(rhand.landmark):
                    h,w,c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmlist1.append([id,cx,cy])
                    # if id == 8 :
                        
                    #     cx4,cy4 = cx,cy
                    # if id ==12:
                    #     difx ,dify = abs(cx4-cx),abs(cy4-cy)
                    #     if difx < 25 and dify < 120 :
                    #         cv2.putText(img,'Fingers Touched',(110,70), cv2.FONT_HERSHEY_COMPLEX, 1,(250,0,0),2)
                    #         centx,centy = int((cx+cx4)/2),int((cy+cy4)/2)
                    #         cv2.circle(img,(centx,centy),15,(250,250,0),cv2.FILLED)
            if len(self.results.multi_hand_landmarks) >1:
                lhand = self.results.multi_hand_landmarks[1]
                for id, lm in enumerate(lhand.landmark):
                        h,w,c = img.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        lmlist2.append([id,cx,cy])

        return lmlist1,lmlist2



def main():
    cap = cv2.VideoCapture(0)
    pTime = 0
    cTime = 0
    detector = handdetector()
    while True:
        lmlist1 = []
        success, img = cap.read()
        img= detector.findhands(img)
        lmlist1 = detector.findList(img)
        # if len(lmlist1) != 0:
        #     print(lmlist1[4])

        
        cTime = time.time()
        fps = int(1/(cTime-pTime))
        pTime = cTime
        cv2.putText(img,str(fps),(10,70), cv2.FONT_HERSHEY_COMPLEX, 2,(250,0,250),3)
        cv2.imshow("image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    return lmlist1


if __name__ == "__main__":
    main()