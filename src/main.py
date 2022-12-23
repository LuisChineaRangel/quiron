import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

capture = cv2.VideoCapture(0)
with mp_hands.Hands(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as hands:
  while capture.isOpened():
    success, frame = capture.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # Flip the frame horizontally for a selfie-view display.
    frame = cv2.flip(frame, 1)

    # To improve performance, optionally mark the frame as not writeable to
    # pass by reference.
    frame.flags.writeable = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame)

    # Draw the hand annotations on the frame.
    frame.flags.writeable = True
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # height, width and depth (RGB=3) of frame
    (height, width, depth) = frame.shape

    # Count of raised fingers
    finger_count = 0

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # Index Position and Handedness (left hand or rigth hand)
        index = results.multi_hand_landmarks.index(hand_landmarks)
        label = results.multi_handedness[index].classification[0].label

        # Drawing within frame of the hand landmark with its connections and mediapipe default style
        mp_drawing.draw_landmarks(
          frame,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())

      # ----------------
      # Detect fingers
      # ----------------
      # list of finger tips locators, 4 is thumb, 20 is pinky finger
      tipIds = [4, 8, 12, 16, 20]
      
      landmark = hand_landmarks.landmark

      # x,y coordinates of pinky tip. Coordinates are normalized to [0.0,1.0] with width and height of the frame
      # x = landmark[tipIds[4]].x
      # y = landmark[tipIds[4]].y

      # Checking Thumb
      if label == "Left" and landmark[tipIds[0]].x > landmark[3].x:
        finger_count += 1
      if label == "Right" and landmark[tipIds[0]].x < landmark[3].x:
        finger_count += 1

      # Checking Index
      if landmark[tipIds[1]].y < landmark[6].y:
        finger_count += 1

      # Checking Index
      if landmark[tipIds[2]].y < landmark[10].y:
        finger_count += 1

      # Checking Index
      if landmark[tipIds[3]].y < landmark[14].y:
        finger_count += 1

      # Checking Index
      if landmark[tipIds[4]].y < landmark[18].y:
        finger_count += 1

      # OpenCV function to draw a circle:
      # cv2.circle(frame, center_coordinates, radius in pixels, color (Blue 0-255, Green 0-255, Red 0-255), thickness in pixels (-1 solid))
      # Example: draw a red solid circle of 10 pixel radius in the tip of pinky finger:
      # cv2.circle(frame, (int(landmark[tipIds[4]].x * width),int(landmark[tipIds[4]].y * height)), 10, (0,0,255), -1)

      # OpenCV function to draw text on frame
      # cv2.putText(frame, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
      # Example: draw a blue "hello" on the upper left corner of the frame
      # cv2.putText(frame, "hello", (20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0), thickness = 5)

      # See other OpenCV functions to draw a line or a rectangle:
      # cv2.line(frame, start_point, end_point, color, thickness)
      # cv2.rectangle(frame, start_point (top-left), end_point (bottom-right), color, thickness)

      # Display finger count
      cv2.putText(frame, str(finger_count), (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 10)

    cv2.imshow('MediaPipe Hands', frame)
    if cv2.waitKey(5) & 0xFF == 27:
      break
capture.release()