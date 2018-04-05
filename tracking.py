import cv2
import sys
import numpy as np
 
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
 
if __name__ == '__main__' :
 
    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[2]
 
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
 
    # Read video
    video = cv2.VideoCapture(0)
 
    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)


    temp_c = (0,0)
    t2 = 0
    why = False
 
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
         
        # Start timer
        timer = cv2.getTickCount()
        t1 = cv2.getTickCount()
 
        # Update tracker
        ok, bbox = tracker.update(frame)
 
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success

            

            # Defining points of the box
            # Upper left point
            p1 = (int(bbox[0]), int(bbox[1]))
            # Bottom right point
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

            # # Bottom left point
            # p3 = (int(bbox[0]), int(bbox[1] + bbox[3]))
            # # Upper right point
            # p4 = (int(bbox[0] + bbox[2]), int(bbox[1]))

            # Center point
            center_x = int(p1[0] + (p2[0] - p1[0])/2)
            center_y = int(p1[1] + (p2[1] - p1[1])/2)
            c = (center_x, center_y)


            # Speed!
            # Time taken from t_start to t_stop in milliseconds
            time = (t1 - t2)/cv2.getTickFrequency()*1000

            # Speed in pixels (?) per ms
            speed_x = int((temp_c[0] - c[0]) / time)
            speed_y = int((temp_c[1] - c[1]) / time)

            # Updating temporary variables for next while loop
            t2 = cv2.getTickCount()
            temp_c = c



            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

            # Text for info
            cv2.putText(frame, "P1: %s" %(p1,), (100, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, "P2: %s" %(p2,), (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, "Center: %s" %(c,), (100, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, "Speed X: %s" %(speed_x), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, "Speed Y: %s" %(speed_y), (100, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, "Time taken: %s ms" %(time), (100, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            # cv2.putText(frame, "P3: %s" %(p3,), (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            # cv2.putText(frame, "P4: %s" %(p4,), (100, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            # cv2.putText(frame, "X: %s" %(x), (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            # cv2.putText(frame, "Y: %s" %(y), (100, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            cv2.putText(frame, ".", c, cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

            if((abs(speed_x) > 3 or abs(speed_y) > 1)):
                why = True

            # Display if speed is above threshold
            if(why == True):
                cv2.putText(frame, "FUCK ME", (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 3,(255,0,200),2)

        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,110), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        # Display timer
        cv2.putText(frame, "Timer: %s" %(timer), (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(50,170,50),2)
 
        # Display result
        cv2.imshow("Tracking", frame)

        
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break