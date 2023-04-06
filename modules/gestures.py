#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 6 2023

@author: iluzioDev

This script implements the gestures and functions used in the Hand Recognition
"""
import numpy

import modules.constants as constants

def distance(p1, p2):
  """
  Calculates the distance between two points on a 2D plane.

  Args:
    p1: Coordinate of the first point
    p2: Coordinate of the second point

  Returns:
    float: Distance between the two points
  """
  return numpy.sqrt(((p2.x - p1.x)**2) + ((p2.y - p1.y)**2))

def sideways(landmark, label):
  """
  Checks if the hand is sideways (Horizontal Aligned)

  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)

  Returns:
    bool: True if hand is sideways, False otherwise
  """
  wrist = landmark[0]
  thumb_cmc = landmark[1]
  pinky_mcp = landmark[17]

  if thumb_cmc.y > wrist.y or thumb_cmc.y < pinky_mcp.y:
    return True
  return False

def raised(landmark, label, tip):
  """
  Checks if a finger is up or not
  
  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)
    tip: ID of the tip of the finger
  
  Returns:
    bool: True if finger is up, False otherwise
  """
  # Vertical Aligned Hand Case
  if not sideways(landmark, label):
    # In thumb case, it must be checked if hand is backward or forward
    if tip == constants.TIPS[0]:
      if landmark[tip].x < landmark[constants.TIPS[4]].x:
        if (label == "Left" and landmark[tip].x < landmark[tip - 1].x) or (label == "Right" and landmark[tip].x < landmark[tip - 1].x):
          return True
      if landmark[tip].x > landmark[constants.TIPS[4]].x:
        if (label == "Right" and landmark[tip].x > landmark[tip - 1].x) or (label == "Left" and landmark[tip].x > landmark[tip - 1].x):
          return True
      return False
    # For rest of fingers, make the comparison between tip and pip
    return landmark[tip].y < landmark[tip - 2].y
  
  # Horizontal Aligned Hand Case
  # In thumb case, it must be checked if hand is backward or forward
  if tip == constants.TIPS[0]:
    thumb_cmc = landmark[constants.TIPS[0]]
    pinky_mcp = landmark[17]
    if thumb_cmc.y < pinky_mcp.y:
      return landmark[tip].y < landmark[tip - 1].y
    return landmark[tip].y > landmark[tip - 1].y
  # For rest of fingers, make the comparison between tip and pip
  return (label == "Left" and landmark[tip].x > landmark[tip - 2].x) or (label == "Right" and landmark[tip].x < landmark[tip - 2].x)


def thumb_up(landmark, label):
  """
  Checks if the thumb is up
  
  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)
    
  Returns:
    bool: True if thumb is up, False otherwise
  """
  if not sideways(landmark, label):
    return False
  if not raised(landmark, label, constants.TIPS[0]) or (landmark[constants.TIPS[0]].y > landmark[constants.TIPS[0] - 1].y):
    return False
  for i in range(1, 5):
    if raised(landmark, label, constants.TIPS[i]):
      return False
  return True

def thumb_down(landmark, label):
  """
  Checks if the thumb is down
  
  Args: 
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)
  
  Returns:
    bool: True if thumb is down, False otherwise
  """
  if not sideways(landmark, label):
    return False
  if not raised(landmark, label, constants.TIPS[0]) or (landmark[constants.TIPS[0]].y < landmark[constants.TIPS[0] - 1].y):
    return False
  for i in range(1, 5):
    if raised(landmark, label, constants.TIPS[i]):
      return False
  return True

def peace(landmark, label):
  """
  Checks if the hand is doing a Peace Sign
  
  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)
    
  Returns:
    bool: True if hand is doing a Peace Sign, False otherwise
  """
  if sideways(landmark, label):
    return False
  if not raised(landmark, label, constants.TIPS[1]) or not raised(landmark, label, constants.TIPS[2]):
    return False
  for i in range(5):
    if i == 1 or i == 2:
      continue
    if raised(landmark, label, constants.TIPS[i]):
      return False
  return True

def rock_n_roll(landmark, label):
  """
  Checks if the hand is doing a Rock N Roll Sign
  
  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)

  Returns:
    bool: True if hand is doing a Rock N Roll Sign, False otherwise
  """
  if not sideways(landmark, label):
    if not raised(landmark, label, constants.TIPS[0]) or not raised(landmark, label, constants.TIPS[1]) or not raised(landmark, label, constants.TIPS[4]):
      return False
    for i in range(2, 4):
      if raised(landmark, label, constants.TIPS[i]):
        return False
  else:
    return False
  return True

def surf(landmark, label):
  """
  Checks if the hand is doing a Surf Sign

  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)

  Returns:
    bool: True if hand is doing a Surf Sign, False otherwise
  """
  if not sideways(landmark, label):
    return False
  if not raised(landmark, label, constants.TIPS[0]) or not raised(landmark, label, constants.TIPS[4]) or (landmark[constants.TIPS[0]].y > landmark[constants.TIPS[0] - 1].y):
    return False
  for i in range(1, 4):
    if raised(landmark, label, constants.TIPS[i]):
      return False
  return True

def ok(landmark, label):
  """
  Checks if the hand is doing an OK Sign
  
  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)

  Returns:
    bool: True if hand is doing an OK Sign, False otherwise
  """
  if sideways(landmark, label):
    return False
  for i in range(2, 5):
    if not raised(landmark, label, constants.TIPS[i]):
      return False
  d = distance(landmark[constants.TIPS[0]], landmark[constants.TIPS[1]])
  if d > constants.MOE:
    return False
  return True

def loser(landmark, label):
  """
  Checks if the hand is doing a Loser Sign

  Args:
    landmark: Landmark of one hand
    label: Label of the hand (Left or Right)

  Returns:
    bool: True if hand is doing a Loser Sign, False otherwise
  """
  if sideways(landmark, label):
    return False
  if not raised(landmark, label, constants.TIPS[0]) or not raised(landmark, label, constants.TIPS[1]):
    return False
  for i in range(2, 5):
    if raised(landmark, label, constants.TIPS[i]):
      return False
  return True
