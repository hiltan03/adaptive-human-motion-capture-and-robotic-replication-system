# Establish serial communication with Arduino (adjust the COM port)
arduino = serial.Serial('COM3', 9600)
import serial
import time
import cv2
import mediapipe as mp

# Initialize serial communication with Arduino (make sure the correct COM port is specified)
arduino = serial.Serial('COM3', 9600)  # Adjust 'COM3' to your correct port
time.sleep(2)  # Wait for the connection to establish

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

def is_hand_raised(landmarks):
    shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
    elbow_y = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y
    wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y
    # If wrist is above the shoulder, the hand is raised
    if wrist_y < shoulder_y and wrist_y < elbow_y:
        return True
    return False

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Flip the frame horizontally for a better user experience
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get the pose landmarks
    results = pose.process(rgb_frame)

    # Draw the landmarks on the image
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Check if the hand is raised
        if is_hand_raised(results.pose_landmarks.landmark):
            arduino.write(b'1')  # Send command '1' to Arduino (hand raised)
        else:
            arduino.write(b'0')  # Send command '0' to Arduino (hand not raised)

    # Display the frame
    cv2.imshow("Human Motion Detection", frame)

    # Break on ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# def send_command(command):
#     arduino.write(command.encode())  # Send command to Arduino
#     time.sleep(1)  # Wait for the servo to move

# # Check if the hand is raised (from the previous code)
# if is_hand_raised(results.pose_landmarks.landmark):
#     send_command('1')  # Send '1' to Arduino to move the servo
# else:
#     send_command('0')  # Send '0' to return the servo to its initial position
