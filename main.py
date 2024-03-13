import numpy as np
import cv2

cap = cv2.VideoCapture(0)

calibrated = False
fivebaht_width = None

while True:
    result, frame = cap.read()
    frameshape = frame.shape
    frameheight = frameshape[0]

    kernel= np.ones((5,5),np.uint8)
    
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray,(5,5),0)
    canny = cv2.Canny(gray_blur, 90, 255)
    closing = cv2.morphologyEx(canny,cv2.MORPH_CLOSE,kernel,iterations=1)

    copy = closing.copy()

    contours, hierarchy = cv2.findContours(copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0,255,0), 2)

    sorted_contours = sorted(contours, key = cv2.contourArea)

    if not calibrated:
        for i, cont in enumerate(sorted_contours):
            x, y, w, h = cv2.boundingRect(cont)
            center_x = x + int(w/2)
            center_y = y + int(h/2)

            frame = cv2.circle(frame, (center_x,center_y), 2 , (0,255,0), 2)
        
        frame = cv2.putText(img = frame , text = "Press 'g' when only one five baht coin is visible", org = (10,20), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.75, color=(0,0,255), thickness=2)
        
        if len(sorted_contours) < 1:
            frame = cv2.putText(img = frame , text = "No coins detected", org = (10,50), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.75, color=(0,0,255), thickness=2)
        elif len(sorted_contours) > 1:
            frame = cv2.putText(img = frame , text = "Too many coins detected", org = (10,50), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.75, color=(0,0,255), thickness=2)
        else:
            frame = cv2.putText(img = frame , text = "Ready! Press 'g'", org = (10,50), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.75, color=(0,255,0), thickness=2)
            if cv2.waitKey(1) & 0xFF==ord('g'):
                fivebaht_width = w
                calibrated = True

    else:
        coin_list = [0,0,0]
        for i, cont in enumerate(sorted_contours):
            x, y, w, h = cv2.boundingRect(cont)
            center_x = x + int(w/2)
            center_y = y + int(h/2)

            if w > fivebaht_width*(25/24):
                output_text = "10"
                coin_list[2] += 1
            elif w < fivebaht_width*(22/24):
                output_text = "1"
                coin_list[0] += 1
            else:
                output_text = "5"
                coin_list[1] += 1

            total_money = (coin_list[0])+(coin_list[1]*5)+(coin_list[2]*10)

            frame = cv2.putText(img = frame , text = output_text, org = (center_x,center_y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.75, color=(0,0,255), thickness=2)
            frame = cv2.circle(frame, (center_x,center_y), 2 , (0,255,0), 2)

        frame2 = np.zeros((frameheight,200,3), np.uint8)
        frame2 = cv2.putText(img = frame2, text = f"One baht: {coin_list[0]}", org = (5,50), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(255,255,255), thickness=2)
        frame2 = cv2.putText(img = frame2, text = f"Five baht: {coin_list[1]}", org = (5,70), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(255,255,255), thickness=2)
        frame2 = cv2.putText(img = frame2, text = f"Ten baht: {coin_list[2]}", org = (5,90), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.5, color=(255,255,255), thickness=2)

        frame2 = cv2.putText(img = frame2, text = f"Total Money", org = (5,130), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.9, color=(255,255,255), thickness=2)
        frame2 = cv2.putText(img = frame2, text = f"{total_money}", org = (5,160), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.9, color=(255,255,255), thickness=2)
        frame2 = cv2.putText(img = frame2, text = f"Baht", org = (65,160), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.9, color=(255,255,255), thickness=2)

        frame = cv2.putText(img = frame , text = output_text, org = (center_x,center_y), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=0.75, color=(0,0,255), thickness=2)
        frame = cv2.hconcat([frame, frame2]) 

    cv2.imshow("Frame", frame) 
    if cv2.waitKey(1) & 0xFF==ord('q'):
         break

cap.release()
cv2.destroyAllWindows()