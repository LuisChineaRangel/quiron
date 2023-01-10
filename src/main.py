import cv2
import numpy as np
import mediapipe as mp

# Title of the Window with the Hand Recognition
TITLE = 'Handy Hands'

# Margin of Error used in checking if two fingers are touching each other
MARGIN_OF_ERROR = 0.05

# Margin of Hand movement
MOVEMENT_MARGIN = 0.025

# Flags to detect Hand movement
moving = prev_thumb_pos = prev_index_pos = prev_middle_pos = prev_ring_pos = prev_pinky_pos = False

# Colors used
BLACK = (0, 0, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)

# Fonts used
FONT = cv2.FONT_HERSHEY_COMPLEX

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# list of finger tips locators, 4 is thumb, 20 is pinky finger
TIPIDS = [4, 8, 12, 16, 20]

# Calculates the distance between 2 point in a landmark
def distance(p1, p2):
  return np.sqrt(((p2.x - p1.x)**2) + ((p2.y - p1.y)**2))

# Checks if finger is up or not
def isFingerUp(landmark, label, tip):
  # Vertical Aligned Hand Case
  if not isHandSideways(landmark, label):
    # In thumb case, it must be checked if hand is backward or forward
    if tip == TIPIDS[0]:
      if landmark[tip].x < landmark[TIPIDS[4]].x:
        if (label == "Left" and landmark[tip].x < landmark[tip - 1].x) or (label == "Right" and landmark[tip].x < landmark[tip - 1].x):
          return True
      if landmark[tip].x > landmark[TIPIDS[4]].x:
        if (label == "Right" and landmark[tip].x > landmark[tip - 1].x) or (label == "Left" and landmark[tip].x > landmark[tip - 1].x):
          return True
      return False
    # For rest of fingers, make the comparison between tip and pip
    return landmark[tip].y < landmark[tip - 2].y
  # Horizontal Aligned Hand Case
  else:
    # In thumb case, it must be checked if hand is backward or forward
    if tip == TIPIDS[0]:
      thumb_cmc = landmark[TIPIDS[0]]
      pinky_mcp = landmark[17]
      if thumb_cmc.y < pinky_mcp.y:
        return landmark[tip].y < landmark[tip - 1].y
      return landmark[tip].y > landmark[tip - 1].y
    # For rest of fingers, make the comparison between tip and pip
    return (label == "Left" and landmark[tip].x > landmark[tip - 2].x) or (label == "Right" and landmark[tip].x < landmark[tip - 2].x)
  return False

# Check if hand is sideways (Horizontal Aligned)
def isHandSideways(landmark, label):
  wrist = landmark[0]
  thumb_cmc = landmark[1]
  pinky_mcp = landmark[17]
  if thumb_cmc.y > wrist.y or thumb_cmc.y < pinky_mcp.y:
    return True
  return False

# Counts fingers up in a hand
def countFingers(landmark, label):
  count = 0
  for i in range(5):
    if isFingerUp(landmark, label, TIPIDS[i]):
      count += 1
  return count

# Detect a Thumbs Up Gesture
def detectThumbUp(landmark, label):
  if isHandSideways(landmark, label):
    if not isFingerUp(landmark, label, TIPIDS[0]) or (landmark[TIPIDS[0]].y > landmark[TIPIDS[0] - 1].y):
      return False
    for i in range(1, 5):
      if isFingerUp(landmark, label, TIPIDS[i]):
        return False
  else:
    return False
  return True

# Detect a Thumbs Down Gesture
def detectThumbDown(landmark, label):
  if isHandSideways(landmark, label):
    if not isFingerUp(landmark, label, TIPIDS[0]) or (landmark[TIPIDS[0]].y < landmark[TIPIDS[0] - 1].y):
      return False
    for i in range(1, 5):
      if isFingerUp(landmark, label, TIPIDS[i]):
        return False
  else:
    return False
  return True

# Detect a Peace Sign Gesture
def detectPeaceSign(landmark, label):
  if not isHandSideways(landmark, label):
    if not isFingerUp(landmark, label, TIPIDS[1]) or not isFingerUp(landmark, label, TIPIDS[2]):
      return False
    for i in range(5):
      if i == 1 or i == 2:
        continue
      if isFingerUp(landmark, label, TIPIDS[i]):
        return False
  else:
    return False
  return True

# Detect a Rock N Roll Sign Gesture
def detectRockNRollSign(landmark, label):
  if not isHandSideways(landmark, label):
    if not isFingerUp(landmark, label, TIPIDS[0]) or not isFingerUp(landmark, label, TIPIDS[1]) or not isFingerUp(landmark, label, TIPIDS[4]):
      return False
    for i in range(2, 4):
      if isFingerUp(landmark, label, TIPIDS[i]):
        return False
  else:
    return False
  return True

# Detect a Surf Sign Gesture
def detectSurfSign(landmark, label):
  if isHandSideways(landmark, label):
    if not isFingerUp(landmark, label, TIPIDS[0]) or not isFingerUp(landmark, label, TIPIDS[4]) or (landmark[TIPIDS[0]].y > landmark[TIPIDS[0] - 1].y):
      return False
    for i in range(1, 4):
      if isFingerUp(landmark, label, TIPIDS[i]):
        return False
  else:
    return False
  return True

# Detect a Ok Sign Gesture
def detectOkSign(landmark, label):
  if not isHandSideways(landmark, label):
    for i in range(2, 5):
      if not isFingerUp(landmark, label, TIPIDS[i]):
        return False
    d = distance(landmark[TIPIDS[0]], landmark[TIPIDS[1]])
    if d > MARGIN_OF_ERROR:
      return False
  else:
    return False
  return True

# Detect a Loser Sign (L) Gesture
def detectLoserSign(landmark, label):
  if not isHandSideways(landmark, label):
    if not isFingerUp(landmark, label, TIPIDS[0]) or not isFingerUp(landmark, label, TIPIDS[1]):
      return False
    for i in range(2, 5):
      if isFingerUp(landmark, label, TIPIDS[i]):
        return False
  else:
    return False
  return True

# Detects gestures in a hand
def detectGestures(landmark, label):
  if detectThumbUp(landmark, label):
    return "Thumbs Up! :D"
  if detectThumbDown(landmark, label):
    return "Thumbs Down... :("
  if detectPeaceSign(landmark, label):
    return "Peace!"
  if detectRockNRollSign(landmark, label):
    return "Rock'n'Roll!"
  if detectSurfSign(landmark, label):
    return "Surf's up!"
  if detectOkSign(landmark, label):
    return "Everything is OK"
  if detectLoserSign(landmark, label):
    return "Loser >:D"
  return False


# Starts the WebCam Capture
capture = cv2.VideoCapture(0)
with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
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

    # finger_count of raised fingers
    finger_count = 0

    # If hands are detected
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

        # Detect fingers
        landmark = hand_landmarks.landmark
        finger_count += countFingers(landmark, label)

        # Detect Gestures
        if detectGestures(landmark, label):
          cv2.rectangle(frame, (int(0.2 * width), int(0.825 * height)),
                        (int(0.975 * width), int(0.975 * height)), WHITE, -1)
          cv2.putText(frame, detectGestures(landmark, label), (int(0.225 * width), int(0.925 * height)),
                      FONT, 1.5, BLUE, 5)

        # Detect Movement
        if not prev_thumb_pos:
          prev_thumb_pos  = landmark[TIPIDS[0]]
          prev_index_pos  = landmark[TIPIDS[1]]
          prev_middle_pos = landmark[TIPIDS[2]]
          prev_ring_pos   = landmark[TIPIDS[3]]
          prev_pinky_pos  = landmark[TIPIDS[4]]

        d0 = distance(prev_thumb_pos, landmark[TIPIDS[0]])
        d1 = distance(prev_index_pos, landmark[TIPIDS[1]])
        d2 = distance(prev_middle_pos, landmark[TIPIDS[2]])
        d3 = distance(prev_ring_pos, landmark[TIPIDS[3]])
        d4 = distance(prev_pinky_pos, landmark[TIPIDS[4]])

        if (d0 + d1 + d2 + d3 + d4) > MOVEMENT_MARGIN:
          moving = True
        else:
          moving = False

        prev_thumb_pos  = landmark[TIPIDS[0]]
        prev_index_pos  = landmark[TIPIDS[1]]
        prev_middle_pos = landmark[TIPIDS[2]]
        prev_ring_pos   = landmark[TIPIDS[3]]
        prev_pinky_pos  = landmark[TIPIDS[4]]

        if moving:
          cv2.rectangle(frame, (int(0.025 * width), int(0.025 * height)),
                        (int(0.45 * width), int(0.14 * height)), BLACK, -1)
          cv2.putText(frame, "Moving Hand...", (int(0.04 * width), int(0.1 * height)),
                      FONT, 1, WHITE, 2)

      # Display fingers counted
      text = str(finger_count).zfill(2)
      cv2.rectangle(frame, (int(0.025 * width), int(0.825 * height)),
                    (int(0.175 * width), int(0.975 * height)), WHITE, -1)
      cv2.putText(frame, text, (int(0.04 * width), int(0.95 * height)),
                  FONT, 2, RED, 10)
    # Show Frame
    cv2.imshow(TITLE, frame)

    # Until Esc Key is pressed
    if cv2.waitKey(5) & 0xFF == 27:
      break
capture.release()
