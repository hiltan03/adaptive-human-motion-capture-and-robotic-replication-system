def is_hand_raised(landmarks):
    shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y
    elbow_y = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y
    wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y
    
    # If wrist is above the shoulder, the hand is raised
    if wrist_y < shoulder_y and wrist_y < elbow_y:
        return True
    return False
