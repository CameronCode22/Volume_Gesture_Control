import cv2
import time
import numpy as np
import hand_tracking_module as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

while True:
    success , img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        #print(lmlist[4],lmlist[8])

        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 11, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 11, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img, (cx, cy), 11, (255,0,255), cv2.FILLED)

        length = math.hypot((x2-x1), (y2 -y1))
        print(length)
    
        #hand range max 250 min 10
        #volume range -65 - 0
        vol = np.interp(length, [10, 300],[minVol, maxVol])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length <50:
            cv2.circle(img, (cx, cy), 11, (0,255,0), cv2.FILLED)





    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}',(40,50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 255), 3)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()