import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Initialize Pose detection
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB for MediaPipe processing
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image)

        # Convert the image back to BGR for display
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark

            # Get key landmarks for the left arm
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

            # Calculate horizontal alignment (y-coordinates should be similar)
            shoulder_elbow_aligned = abs(left_shoulder.y - left_elbow.y) < 0.05
            elbow_wrist_aligned = abs(left_elbow.y - left_wrist.y) < 0.05

            # Ensure the wrist is farther left than the elbow
            wrist_left_of_elbow = left_wrist.x < left_elbow.x

            # Check if all conditions are met
            if shoulder_elbow_aligned and elbow_wrist_aligned and wrist_left_of_elbow:
                print("Left arm raised horizontally to the left detected!")
                cv2.putText(image, "Left Arm Raised!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw the pose landmarks
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # Display the frame
        cv2.imshow('Pose Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:  # Press ESC to exit
            break

cap.release()
cv2.destroyAllWindows()
