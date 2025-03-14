import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break


        frame = cv2.flip(frame, 1)
  
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                handedness = results.multi_handedness[0].classification[0].label
                if handedness == 'Right':
  
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    all_fingers_right = True
                    all_fingers_left = True
                    all_fingers_up = True
                    all_fingers_down = True

                    for id in range(5): 
      
                        tip = hand_landmarks.landmark[mp_hands.HandLandmark(id * 4 + 4)]
                        pip = hand_landmarks.landmark[mp_hands.HandLandmark(id * 4 + 2)]
                        mcp = hand_landmarks.landmark[mp_hands.HandLandmark(id * 4 + 1)]
                        
                        if tip.x < pip.x:
                            all_fingers_right = False

                        if tip.x > pip.x:
                            all_fingers_left = False

                        if tip.y > pip.y:
                            all_fingers_up = False
                        
                        if tip.y < mcp.y:
                            all_fingers_down = False

                    if all_fingers_right:
                        gesture = "Right"
                    elif all_fingers_left:
                        gesture = "Left"
                    elif all_fingers_up:
                        gesture = "Break"
                    elif all_fingers_down:
                        gesture = "MoveBack"
                    else:
                        gesture = "go"

                    if gesture:
                        cv2.putText(frame, gesture, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Hand Gesture Recognition', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows() in here suggest me project name
