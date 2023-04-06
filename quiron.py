#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 2022

@author: iluzioDev

This script implements Hand Recognition using Mediapipe and OpenCV.
Includes features like:
  - Hand Recognition
  - Hand Movement Detection
  - Hand Gesture Recognition
  - Finger Counting
"""
import cv2
import mediapipe

import modules.constants as constants
import modules.gestures as gestures

# Flags to detect Hand movement
moves = prev_thumb = prev_index = prev_middle = prev_ring = prev_pinky = False

def count_fingers(landmark, label):
  """
  Counts the number of fingers up in a hand
  
  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)
    
  Returns:
    int: Number of fingers up
  """
  count = 0
  for i in range(5):
    if gestures.raised(landmark, label, constants.TIPS[i]):
      count += 1
  return count

def detect_gestures(landmark, label):
  """
  Detects the gesture of a hand

  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)
  
  Returns:
    str or bool: The gesture if it is detected, False otherwise
  """
  if gestures.thumb_up(landmark, label):
    return "Thumbs Up! :D"
  if gestures.thumb_down(landmark, label):
    return "Thumbs Down... :("
  if gestures.peace(landmark, label):
    return "Peace!"
  if gestures.rock_n_roll(landmark, label):
    return "Rock'n'Roll!"
  if gestures.surf(landmark, label):
    return "Surf's up!"
  if gestures.ok(landmark, label):
    return "Everything is OK"
  if gestures.loser(landmark, label):
    return "Loser >:D"
  return False

def moving(landmark):
  """
  Detects if the hand is moving or not calculating the distance in a margin between the positions
  of 2 instances through time of the hand

  Args:
    landmark: Landmark of one hand
  
  Returns:
    bool: True if the hand is moving, False otherwise
  """
  global moves, prev_thumb, prev_index, prev_middle, prev_ring, prev_pinky
  if not prev_thumb:
    prev_thumb = landmark[constants.TIPS[0]]
    prev_index = landmark[constants.TIPS[1]]
    prev_middle = landmark[constants.TIPS[2]]
    prev_ring = landmark[constants.TIPS[3]]
    prev_pinky = landmark[constants.TIPS[4]]

  d0 = gestures.distance(prev_thumb, landmark[constants.TIPS[0]])
  d1 = gestures.distance(prev_index, landmark[constants.TIPS[1]])
  d2 = gestures.distance(prev_middle, landmark[constants.TIPS[2]])
  d3 = gestures.distance(prev_ring, landmark[constants.TIPS[3]])
  d4 = gestures.distance(prev_pinky, landmark[constants.TIPS[4]])

  if (d0 + d1 + d2 + d3 + d4) > constants.MARGIN:
    moves = True
  else:
    moves = False

  prev_thumb = landmark[constants.TIPS[0]]
  prev_index = landmark[constants.TIPS[1]]
  prev_middle = landmark[constants.TIPS[2]]
  prev_ring = landmark[constants.TIPS[3]]
  prev_pinky = landmark[constants.TIPS[4]]

  return moves

def main():
  """
  Main function of the program. Starts the WebCam Capture and uses the features implemented
  
  Returns:
    None
  """
  mp_drawing = mediapipe.solutions.drawing_utils
  mp_drawing_styles = mediapipe.solutions.drawing_styles
  mp_hands = mediapipe.solutions.hands

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

      # finger_count of gestures.raised fingers
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
          finger_count += count_fingers(landmark, label)

          # Detect Gestures
          if detect_gestures(landmark, label):
            cv2.rectangle(frame, (int(0.2 * width), int(0.825 * height)),
                          (int(0.975 * width), int(0.975 * height)), constants.WHITE, -1)
            cv2.putText(frame, detect_gestures(landmark, label), (int(0.225 * width), int(0.925 * height)),
                        constants.FONT, 1.5, constants.BLUE, 5)

          # Detect Movement
          if moving(landmark):
            cv2.rectangle(frame, (int(0.025 * width), int(0.025 * height)),
                          (int(0.45 * width), int(0.14 * height)), constants.BLACK, -1)
            cv2.putText(frame, "Moving Hand...", (int(0.04 * width), int(0.1 * height)),
                        constants.FONT, 1, constants.WHITE, 2)

        # Display fingers counted
        text = str(finger_count).zfill(2)
        cv2.rectangle(frame, (int(0.025 * width), int(0.825 * height)),
                      (int(0.175 * width), int(0.975 * height)), constants.WHITE, -1)
        cv2.putText(frame, text, (int(0.04 * width), int(0.95 * height)),
                    constants.FONT, 2, constants.RED, 10)
      # Show Frame
      cv2.imshow(constants.TITLE, frame)

      # Until Esc Key is pressed
      if cv2.waitKey(5) & 0xFF == 27:
        break
  capture.release()

if __name__ == "__main__":
  main()
