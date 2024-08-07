import cv2
import numpy as np
import json

def nothing(x):
    pass

# Create a window for trackbars
cv2.namedWindow('Calibration')

# Create trackbars for HSV range
cv2.createTrackbar('LH', 'Calibration', 20, 180, nothing)
cv2.createTrackbar('LS', 'Calibration', 100, 255, nothing)
cv2.createTrackbar('LV', 'Calibration', 100, 255, nothing)
cv2.createTrackbar('UH', 'Calibration', 30, 180, nothing)
cv2.createTrackbar('US', 'Calibration', 255, 255, nothing)
cv2.createTrackbar('UV', 'Calibration', 255, 255, nothing)

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos('LH', 'Calibration')
    l_s = cv2.getTrackbarPos('LS', 'Calibration')
    l_v = cv2.getTrackbarPos('LV', 'Calibration')
    u_h = cv2.getTrackbarPos('UH', 'Calibration')
    u_s = cv2.getTrackbarPos('US', 'Calibration')
    u_v = cv2.getTrackbarPos('UV', 'Calibration')

    lower_hsv = np.array([l_h, l_s, l_v])
    upper_hsv = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Apply morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('Original', frame)
    cv2.imshow('Mask', mask)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        # Save the HSV ranges to a file
        hsv_ranges = {
            'lower_hue': l_h,
            'lower_saturation': l_s,
            'lower_value': l_v,
            'upper_hue': u_h,
            'upper_saturation': u_s,
            'upper_value': u_v
        }

        with open('hsv_ranges.json', 'w') as f:
            json.dump(hsv_ranges, f)

        print("HSV values saved to 'hsv_ranges.json'")

cap.release()
cv2.destroyAllWindows()




