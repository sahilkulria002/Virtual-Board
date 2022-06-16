import numpy as np
import cv2
from collections import deque
import HTrackModule as htm
# import mediapipe as mp
import time
pTime = 0
import math


def draw(drawseq,drawlen,frame,isboard) :
    for i in range(drawlen) :
        
        fstats,fid = drawseq[i]  ### feature statics and feature id (eg 1 for circle)
    ### Draw circle
        if fid == 1 :
            c,r,clr,th = fstats
            if isboard :
                clr2= [clr[0]/255,clr[1]/255,clr[2]/255]
            else : clr2 = clr.copy()
            cv2.circle(frame,c,r,clr2,th)

    ### draw elipse
        elif fid == 5 :
            c,r,a,clr,ang,th = fstats
            if isboard :
                clr2= [clr[0]/255,clr[1]/255,clr[2]/255]
            else : clr2 = clr.copy()
            cv2.ellipse(frame,c,(r,r),ang,a+2,360-a-2,clr2,th)
        #### draw line 
        elif fid == 3 :
            pt1,pt2,clr,th = fstats
            if isboard :
                clr2= [clr[0]/255,clr[1]/255,clr[2]/255]
            else : clr2 = clr.copy()
            cv2.line(frame,pt1,pt2,clr2,th)
        ## draw rectangle
        elif fid == 2 :
            s,e,clr,th = fstats
            if isboard :
                clr2= [clr[0]/255,clr[1]/255,clr[2]/255]
            else : clr2 = clr.copy()
            cv2.rectangle(frame,s,e,clr2,th)
        elif fid == 6 :
            trp,clr = fstats
            if isboard :
                clr2= [clr[0]/255,clr[1]/255,clr[2]/255]
            else : clr2 = clr.copy()
            cv2.drawContours(frame,[trp],0,clr2,-1)
    #### draw line
        elif fid == 4 :
            lpt = fstats
            k = 1
            while k < len(lpt) :
                
                if lpt[k][0][0] == -1 :
                    k += 2     ###### if fingers are untouched and then touched, line drawn should not be continuous
                    continue
                if isboard :
                    cv2.line(frame,lpt[k-1][0],lpt[k][0],lpt[k][2],lpt[k][3])
                else :
                    cv2.line(frame,lpt[k-1][0],lpt[k][0],lpt[k][1],lpt[k][3])
                # cv2.line(paintWindow,lpt[k-1][0],lpt[k][0],lpt[k][2],lpt[k][3])
                k += 1



lpoints = [((-1,-1),0,0)]
# Here is code for Canvas setup
butYlen = 43
bdif = 0
butXlne = 77
textsp = 10
textspY = 17
textthick = 1
backcolor = tuple([0.8]*3)
paintWindow = np.zeros((481,641,3)) + backcolor[0]
botbuttext = ['Thick ','Thin',"No Fill","Pen","Clear","Prev ",'Next ',"Export"]
top1buttext = ["Circle","Rect","Line","Undo","Redo"]
top2buttext = ["","","","",""]
curtool = "Pen"
mxy,mxx = 480,640
nstep = 85
clrbxx = mxx-3*nstep
butbotheight = 20
textclr = (0,0,0)


for i in range(nstep) :
    for j in range(clrbxx,mxx) :
        paintWindow[i][j][2] = i/nstep
        if j <= clrbxx+nstep :
            paintWindow[i][j][0] = (j-clrbxx)/nstep
            paintWindow[i][j][1] = 0
        elif j < clrbxx+2*nstep :
            paintWindow[i][j][0] = 1
            paintWindow[i][j][1] = (j-clrbxx-nstep)/nstep
        else :
            paintWindow[i][j][0] = (mxx-j)/nstep
            paintWindow[i][j][1] = 1
cv2.line(paintWindow,(clrbxx,0),(clrbxx,2*butYlen),(0,0,0),2)
cv2.line(paintWindow,(0,mxy-butbotheight-(butYlen//2)),(butXlne-5,mxy-butbotheight-(butYlen//2)),(0,0,250),15)
cv2.line(paintWindow,(butXlne,mxy-butbotheight-(butYlen//2)),(2*butXlne-2,mxy-butbotheight-(butYlen//2)),(0,0,250),3)
for i in range(7) :
    paintWindow = cv2.rectangle(paintWindow, (i*butXlne,mxy-butYlen-butbotheight), ((i+1)*butXlne,mxy-butbotheight), (00,00,0),2)
    cv2.putText(paintWindow,botbuttext[i],(i*butXlne+textsp,mxy-textspY-butbotheight),cv2.FONT_HERSHEY_SIMPLEX, 0.5,textclr, textthick, cv2.LINE_AA)
    if i < 5 :
        paintWindow = cv2.rectangle(paintWindow, (i*butXlne,1), ((i+1)*butXlne,butYlen), (00,00,0),2)
        cv2.putText(paintWindow, top1buttext[i],(i*butXlne+textsp,butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, textclr, textthick, cv2.LINE_AA)
        # if i > 1 :
        #     paintWindow = cv2.rectangle(paintWindow, (i*butXlne,butYlen), ((i+1)*butXlne,2*butYlen), (00,00,0),2)
        #     cv2.putText(paintWindow, top2buttext[i],(i*butXlne+textsp,2*butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (1,0,0), textthick, cv2.LINE_AA)
cv2.line(paintWindow,(0,2*butYlen),(mxx,2*butYlen),(0,0,0),2)
cv2.rectangle(paintWindow,(7*butXlne,mxy-butYlen-butbotheight),(mxx,mxy-butbotheight),(0.5,0.5,0.5),cv2.FILLED)
cv2.putText(paintWindow,"Export",(7*butXlne+textsp,mxy-textspY-butbotheight),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(1,0,0), textthick, cv2.LINE_AA)
# cv2.rectangle(paintWindow,(0,butYlen),(2*butXlne,2*butYlen),(0,0,0),2)
# cv2.putText(paintWindow,curtool,(textsp,2*butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(1,0,0), textthick, cv2.LINE_AA)
# Loading the default webcam of PC.
cap = cv2.VideoCapture(0)

pTime = 0
cTime = 0
detector = htm.handdetector()
toch = 0
bol = {"circle" : False, "Rectangle" : False , "Line" : False, "Pen" : True, "elp" : False, "elp2" : False,"Undo" : False, 
    "Redo" : False, "Next" : False, "Prev" : False, "Export": False, "thkUp" : False, "thkDn" : False, "Filling" : False}
prevtool = "Pen"
redolist = []
circl = False
ld = False
rectforming = False
penwrite = False
stang = 0
radii = 0
penclr = (1,0,0)
penclrcam  = [255,0,0]
thickness = 2
pthickness = 2
drawseq = []
totapage = 1
pagenum = 0
pagedrawseq = [[[],0,[]]]  ##### stores sequences of all the pages
pages = {}       ##### stores images array of all the pages
# drawsqtool = 4 ######1 for circle, 2 for rect, 3 for line, 4 for pen, 5 for elp, also 5  for epl2  6 for cTriangle
drawlen = 0 ### number of drawings formed 
# Keep looping
while True:
    # drawseq = pagedrawseq[pagenum][0]
    # drawlen = pagedrawseq[pagenum][1]
    # Reading the frame from the camera
    display = "CPage : " + str(pagenum+1) + " TPage : " + str(totapage) +  ' Tool : ' + curtool + '  Th : ' + str(thickness)
    ret, frame = cap.read()
    #Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    lmlist = []
    frame= detector.findhands(frame)
    lmlist,lmRlist = detector.findList(frame)
    if thickness != -1 :
        pthickness = thickness
    draw(drawseq,drawlen,frame,False)
    for i in range(nstep) :
        for j in range(clrbxx,mxx) :
            frame[i][j][2] = i*3
            if j <= clrbxx+nstep :
                frame[i][j][0] = (j-clrbxx)*3
                frame[i][j][1] = 0
            elif j < clrbxx+2*nstep :
                frame[i][j][0] = 255
                frame[i][j][1] = (j-clrbxx-nstep)*3
            else :
                frame[i][j][0] = (mxx-j)*3
                frame[i][j][1] = 255
    cv2.line(frame,(clrbxx,0),(clrbxx,2*butYlen),(0,0,0),2)
    cv2.line(frame,(0,mxy-butbotheight-(butYlen//2)),(butXlne-5,mxy-butbotheight-(butYlen//2)),penclrcam,15)
    cv2.line(frame,(butXlne,mxy-butbotheight-(butYlen//2)),(2*butXlne-2,mxy-butbotheight-(butYlen//2)),penclrcam,3)
    # Adding the  buttons to the live frame for colour access
    # frame = cv2.rectangle(frame, (bdif,1), (butXlne,butYlen),(100,0,200),-1)
    if thickness == -1 :
        botbuttext[2] = "Fill"
    else :
        botbuttext[2] = "No Fill"
    for i in range(7) :
        frame = cv2.rectangle(frame, (i*butXlne,mxy-butYlen-butbotheight), ((i+1)*butXlne,mxy-butbotheight), (0,0,0),2)
        cv2.putText(frame,botbuttext[i],(i*butXlne+textsp,mxy-textspY-butbotheight),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250), textthick, cv2.LINE_AA)
        if i < 5 :
            frame = cv2.rectangle(frame, (i*butXlne,1), ((i+1)*butXlne,butYlen), (00,00,0),2)
            cv2.putText(frame, top1buttext[i],(i*butXlne+textsp,butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,250,250), textthick, cv2.LINE_AA)
            # if i > 1 :
            #     frame = cv2.rectangle(frame, (i*butXlne,butYlen), ((i+1)*butXlne,2*butYlen), (00,00,0),2)
            #     cv2.putText(frame, top2buttext[i],(i*butXlne+textsp,2*butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), textthick, cv2.LINE_AA)
    cv2.line(frame,(0,2*butYlen),(mxx,2*butYlen),(0,0,0),2)
    cv2.rectangle(frame,(7*butXlne,mxy-butYlen-butbotheight),(mxx,mxy-butbotheight),(125,125,125),cv2.FILLED)
    cv2.putText(frame,"Export",(7*butXlne+textsp,mxy-textspY-butbotheight),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0), textthick, cv2.LINE_AA)
    cv2.rectangle(frame,(5,butYlen+10),(25,butYlen+30),penclrcam,cv2.FILLED)
    cv2.putText(frame,display,(30,2*butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0), textthick, cv2.LINE_AA)
    cv2.rectangle(paintWindow,(5,butYlen+10),(25,butYlen+30),penclr,cv2.FILLED)
    cv2.rectangle(paintWindow,(35,butYlen+2),(clrbxx,2*butYlen-2),backcolor,cv2.FILLED)
    cv2.putText(paintWindow,display,(30,2*butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(1,0,0), textthick, cv2.LINE_AA)
    
    # cv2.putText(frame, 'Circle',(bdif+textsp,butYlen-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), textthick, cv2.LINE_AA)
    

    # If hand is detected
    if len(lmlist) != 0:
        ## finding difference between firstfinger and thumb
        difx ,dify = abs(lmlist[4][1]-lmlist[8][1]),abs(lmlist[4][2]-lmlist[8][2])
        if difx < 35 and dify < 35 :
            toch+=1
            # cv2.putText(frame,'Fingers Touched',(110,70), cv2.FONT_HERSHEY_COMPLEX, 1,(250,0,0),2)
            centx,centy = int((lmlist[4][1]+lmlist[8][1])/2),int((lmlist[4][2]+lmlist[8][2])/2)
            cv2.circle(frame,(centx,centy),10,penclrcam,cv2.FILLED)
            cv2.circle(frame,(centx,centy),5,(250,250,250),cv2.FILLED)
            center  = (centx,centy)

        # Now checking if the user wants to click on any button on  screen 
            if center[1] <= 2*butYlen-2 or center[1]>480-butYlen-butbotheight:
                toch = 0
                if center[1] <= 2*butYlen and center[0] >clrbxx :
                    penclr = paintWindow[center[1]][center[0]]
                    penclrcam = [penclr[0]*255,penclr[1]*255,penclr[2]*255]


                if center[1] < butYlen :
                    if bdif <= center[0] <= butXlne  :   ##### Circle butten
                        bol[prevtool] = False
                        bol["circle"] = True
                        curtool = "Circle"
                        prevtool = "circle"
                    elif butXlne<center[0]<=2*butXlne :     ##### Rectangle butten
                        bol[prevtool] = False
                        bol["Rectangle"] = True
                        curtool = "Rect."
                        prevtool = "Rectangle"
                    elif 2*butXlne<center[0]<=3*butXlne :     ##### Line butten
                        bol[prevtool] = False
                        thickness = pthickness
                        bol["Line"] = True
                        curtool = "Line"
                        prevtool = "Line"
                    elif 3*butXlne<center[0]<=4*butXlne :   #####Undo Button
                        bol["Undo"] = True
                    elif 4*butXlne<center[0]<=5*butXlne :   #####Redo Button
                        bol["Redo"] = True
                elif center[1] > 480-butYlen-butbotheight :
                    if center[0] < butXlne :
                        bol["thkUp"] = True
                    if butXlne < center[0] < 2*butXlne :
                        bol["thkDn"] = True
                    if 2*butXlne < center[0] < 3*butXlne :
                        bol["Filling"] = True
                    if 3*butXlne < center[0] < 4*butXlne :     #### Pen butten
                        bol[prevtool] = False
                        thickness = pthickness
                        bol["Pen"] = True
                        curtool = "Pen"
                        prevtool = "Pen"
                    elif 5*butXlne <= center[0] <= 6*butXlne  :     ### Prev butten
                        bol["Prev"] = True
                    elif 6*butXlne <= center[0] <= 7*butXlne  :      #### Next button
                        bol["Next"] = True
                    elif 7*butXlne <= center[0] <= mxx :
                        bol["Export"] = True


                    elif 4*butXlne <= center[0] <= 5*butXlne  : # Clear Button
                        drawseq.clear()
                        drawlen = 0
                        paintWindow[2*butYlen+1:480-butYlen-butbotheight,:,:] = backcolor[0]
                    
            else :
                if bol["circle"] :
                    if toch == 1 :
                        centercirl = center
                    else :
                        radii = int(((center[0]-centercirl[0])**2 + (center[1]-centercirl[1])**2)**0.5)
                        if centercirl[1]-radii < 2*butYlen :
                            stang = int((math.acos((centercirl[1]-2*butYlen)/radii))*180/math.pi)
                            bol["elp"],circl = True,False
                            cr = cv2.ellipse(frame,centercirl,(radii,radii),270,stang+2,360-stang-2,penclrcam,thickness)
                            if thickness == -1 :
                                espt = int((radii**2-(centercirl[1]-2*butYlen)**2)**0.5)
                                # espt = int(radii*math.cos(stang))
                                trianglepts = np.array([centercirl,(centercirl[0]+espt+espt//10,2*butYlen),(centercirl[0]-espt-espt//10,2*butYlen)])
                                # print(trianglepts)
                                # trianglepts = trianglepts.astype(np.int64)
                                cv2.drawContours(frame,[trianglepts],0,penclrcam,-1)
                        elif centercirl[1] + radii > 480-butYlen-butbotheight :
                            stang = int((math.acos((mxy-centercirl[1]-butYlen-butbotheight)/radii))*180/math.pi)
                            bol["elp2"],circl = True,False
                            cr = cv2.ellipse(frame,centercirl,(radii,radii),90,stang+2,360-stang-2,penclrcam,thickness)
                            if thickness == -1 :
                                espt = int((radii**2-(mxy-centercirl[1]-butbotheight-butYlen)**2)**0.5)
                                trianglepts = np.array([centercirl,(centercirl[0]-espt-espt//10,mxy-butbotheight-butYlen),(centercirl[0]+espt+espt//10,mxy-butbotheight-butYlen)])
                                cv2.drawContours(frame,[trianglepts],0,penclrcam,-1)
                        
                        else :
                            circl = True
                            cr = cv2.circle(frame,centercirl,radii,penclrcam,thickness)
                elif bol["Pen"] :
                    if toch == 1 :
                        lpoints.append(((-1,-1),0,0,1))
                    lpoints.append((center,penclrcam,penclr,thickness))
                    k = 1
                    while k < len(lpoints) :
                        
                        if lpoints[k][0][0] == -1 :
                            k += 2     ###### if fingers are untouched and then touched, line drawn should not be continuous
                            continue
                        cv2.line(frame,lpoints[k-1][0],lpoints[k][0],lpoints[k][1],lpoints[k][3])
                        cv2.line(paintWindow,lpoints[k-1][0],lpoints[k][0],lpoints[k][2],lpoints[k][3])
                        k += 1
                    penwrite = True
                elif bol["Line"] :
                    if toch == 1 :
                        pt1 = center
                    else :
                        pt2 = center
                        cv2.line(frame,pt1,pt2,penclrcam,thickness)
                        ld = True
                elif bol["Rectangle"] :
                    if toch == 1 :
                        stpoint = center
                    else :
                        endpoint = center
                        cv2.rectangle(frame,stpoint,endpoint,penclrcam,thickness)
                        rectforming = True
        else:
            toch = 0
            if radii != 0 :
                if circl  :
                    cr = cv2.circle(paintWindow,centercirl,radii,penclr,thickness)
                    drawseq.append(((centercirl,radii,penclrcam,thickness),1))
                    circl,bol["elp"],bol["elp2"] = False,False,False
                    drawlen += 1
                    radii = 0
                if bol["elp"] :
                    cr = cv2.ellipse(paintWindow,centercirl,(radii,radii),270,stang+2,360-stang-2,penclr,thickness)
                    if thickness == -1 :
                        cv2.drawContours(paintWindow,[trianglepts],0,penclr,-1)
                        drawseq.append(((trianglepts,penclrcam),6))
                        drawlen += 1
                    drawseq.append(((centercirl,radii,stang,penclrcam,270,thickness),5))
                    drawlen+=1
                    radii = 0
                    bol["elp"] = False
                elif bol["elp2"] :
                    cr = cv2.ellipse(paintWindow,centercirl,(radii,radii),90,stang+2,360-stang-2,penclr,thickness)
                    if thickness == -1 :
                        cv2.drawContours(paintWindow,[trianglepts],0,penclr,-1)
                        drawseq.append(((trianglepts,penclrcam),6))
                        drawlen+=1
                    drawseq.append(((centercirl,radii,stang,penclrcam,90,thickness),5))
                    drawlen += 1
                    radii = 0
                    bol["elp2"] = False
                
            elif penwrite :

                drawseq.append(((lpoints.copy()),4))
                lpoints.clear()
                drawlen += 1
                lpoints.append(((-1,-1),0,0,1))
                penwrite = False
            elif rectforming :
                cv2.rectangle(paintWindow,stpoint,endpoint,penclr,thickness)
                drawseq.append(((stpoint,endpoint,penclrcam,thickness),2))
                drawlen += 1
                rectforming = False
            elif ld :
                cv2.line(paintWindow,pt1,pt2,penclr,thickness)
                drawseq.append(((pt1,pt2,penclrcam,thickness),3))
                drawlen += 1
                ld = False
            elif bol["thkUp"] :
                if 0 < thickness < 15 :
                    thickness += 1
                bol["thkUp"] = False
            elif bol["thkDn"] :
                if thickness > 1 :
                    thickness -= 1
                bol["thkDn"] = False
            elif bol["Filling"] :
                if thickness != -1 and curtool != 'Pen':
                    cv2.rectangle(paintWindow,(2*butXlne+2,mxy-butbotheight-butYlen+2),(3*butXlne-2,mxy-butbotheight-2),backcolor,-1)
                    cv2.putText(paintWindow,'Fill',(2*butXlne+textsp,mxy-butbotheight-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), textthick, cv2.LINE_AA)
                    pthickness = thickness
                    thickness = -1
                else :
                    cv2.rectangle(paintWindow,(2*butXlne+2,mxy-butbotheight-butYlen+2),(3*butXlne-2,mxy-butbotheight-2),backcolor,-1)
                    cv2.putText(paintWindow,'No Fill',(2*butXlne+textsp,mxy-butbotheight-textspY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), textthick, cv2.LINE_AA)
                    thickness = pthickness
                bol["Filling"] = False
            elif bol["Undo"] :
                if drawlen >0 :
                    redolist.append(drawseq.pop())
                    drawlen -= 1
                    paintWindow[2*butYlen+1:480-butYlen-butbotheight,:,:] = backcolor[0]
                    draw(drawseq,drawlen,paintWindow,True)
                bol["Undo"] = False
            elif bol["Redo"] :
                if len(redolist) >0 :
                    drawseq.append(redolist.pop())
                    drawlen += 1
                    draw(drawseq,drawlen,paintWindow,True)
                bol["Redo"] = False
            elif bol["Next"] :
                pagedrawseq[pagenum][0] = drawseq.copy()
                pagedrawseq[pagenum][1] = drawlen
                pagedrawseq[pagenum][2] = redolist.copy()
                pages[pagenum] = paintWindow[2*butYlen+1:480-butYlen-butbotheight-2,:,:].copy()
                if pagenum < totapage-1 :
                    pagenum += 1
                    drawlen = pagedrawseq[pagenum][1]
                    drawseq = pagedrawseq[pagenum][0]
                    redolist = pagedrawseq[pagenum][2]
                    paintWindow[2*butYlen+1:480-butYlen-butbotheight-2,:,:] = backcolor[0]
                    draw(drawseq,drawlen,paintWindow,True)
                else :
                    pagedrawseq.append([[],0,[]])
                    drawlen = 0
                    drawseq = []
                    redolist = []
                    paintWindow[2*butYlen+1:480-butYlen-butbotheight-2,:,:] = backcolor[0]
                    pagenum += 1
                    totapage += 1
                bol["Next"] = False
            elif bol["Prev"] :
                if pagenum > 0 :
                    pagedrawseq[pagenum][0] = drawseq.copy()
                    pagedrawseq[pagenum][1] = drawlen
                    pagedrawseq[pagenum][2] = redolist.copy()
                    pages[pagenum] = paintWindow[2*butYlen+1:480-butYlen-butbotheight-2,:,:].copy()
                    pagenum -= 1
                    drawseq = pagedrawseq[pagenum][0]
                    drawlen = pagedrawseq[pagenum][1]
                    redolist = pagedrawseq[pagenum][2]
                    paintWindow[2*butYlen+1:480-butYlen-butbotheight,:,:] = backcolor[0]
                    draw(drawseq,drawlen,paintWindow,True)
                bol["Prev"] = False
            elif bol["Export"] : 
                break
                    
    # Draw lines of all the colors on the canvas and frame 
    ########## Draw all drawings on frame
    
        
    
    # Show all the windows
    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime
    cv2.putText(frame,str(fps),(10,70), cv2.FONT_HERSHEY_COMPLEX, 2,(250,0,250),3)
    
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

	# If the 'q' key is pressed then stop the application 
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
if pagenum == totapage-1 :
    pages[pagenum] = paintWindow[2*butYlen+1:480-butYlen-butbotheight-2,:,:].copy()
if not len(pages) :
    cap.release()
    cv2.destroyAllWindows()
mt = pages[0].copy()
for k in range(len(mt)) :
    for j in range(len(mt[0])) :
        mt[k][j][0] *= 255
        mt[k][j][1] *= 255
        mt[k][j][2] *= 255
fimg = mt.copy()
# mt.clear()
fcvimg = pages[0].copy()
for i in pages: 
    if i == totapage-1 :
        break
    mt = pages[i+1].copy()
    for k in range(len(mt)) :
        for j in range(len(mt[0])) :
            mt[k][j][0] *= 255
            mt[k][j][1] *= 255
            mt[k][j][2] *= 255
    fimg = cv2.vconcat([fimg,mt])
    fcvimg = cv2.vconcat([fcvimg,pages[i+1]])
cv2.imwrite('Notes.png',fimg)
print('saved image')
while True :
    cv2.imshow('final notes',fcvimg)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()