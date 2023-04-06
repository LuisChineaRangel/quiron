#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 6 2023

@author: iluzioDev

This script implements the constants used in Quiron
"""
import cv2

# Title of the Window with the Hand Recognition
TITLE = 'Handy Hands'

# Colors used
BLACK = (0, 0, 0)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
WHITE = (255, 255, 255)

# Fonts used
FONT = cv2.FONT_HERSHEY_COMPLEX

# List of the identifiers of the tips of the fingers
TIPS = [4, 8, 12, 16, 20]

# Margin of Error used in checking if two fingers are touching each other
MOE = 0.05

# Margin of Hand movement
MARGIN = 0.025
