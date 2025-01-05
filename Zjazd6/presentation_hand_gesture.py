import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_gesture = mp.solutions.hands.Hands


def detect_hand_direction(hand_landmarks):
    thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    pinky_x = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x

#Sprawdzenie w którą stronę jest zwrócona ręka
    if thumb_x < pinky_x:
        return "LEFT"
    else:
        return "RIGHT"

def thumb_up():
    # Pobieramy punkty końcowe kciuka oraz innych palców
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]

    # Podstawy palców (przykładowo: podstawy palca wskazującego, środkowego itd.)
    index_base = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP]
    middle_base = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_base = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_MCP]
    pinky_base = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_MCP]

    # Sprawdzamy, czy kciuk jest wyraźnie wyższy niż pozostałe palce
    # oraz czy inne palce są schowane (końcówki palców blisko podstawy)
    if (thumb_tip.y < index_tip.y and
            thumb_tip.y < middle_tip.y and
            thumb_tip.y < ring_tip.y and
            thumb_tip.y < pinky_tip.y and

            # Sprawdzamy, czy końcówki palców są blisko podstawy (czy są zgięte)
            abs(index_tip.x - thumb_tip.x) < abs(index_base.x - thumb_tip.x) and
            abs(middle_tip.x - thumb_tip.x) < abs(middle_base.x - thumb_tip.x) and
            abs(ring_tip.x - thumb_tip.x) < abs(ring_base.x - thumb_tip.x) and
            abs(pinky_tip.x - thumb_tip.x) < abs(pinky_base.x - thumb_tip.x)
        ):
        return True



cap = cv2.VideoCapture(0)
with (mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands):
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

                #zwraca która ręka i w którą stronę jest zwrócona
                direction = detect_hand_direction(hand_landmarks)
                hand_type = results.multi_handedness[0].classification[0].label

                #Kamerka ma lustrzane odbicie
                if hand_type == "Right":
                    hand_type = "Left"
                else:
                    hand_type = "Right"

                if(thumb_up()):
                    gesture = "Thumb up"
                    pyautogui.press('space')
                    print("Spacja wciśnięta!")
                else:
                    gesture = direction
                    if direction == "RIGHT":
                        pyautogui.press('left')
                        print("STRZALKA W LEWO")
                    else:
                        pyautogui.press('right')
                        print("STRZALKA W PRAWO")


                print(f"{hand_type}: {direction}, Gest: {gesture}")

                cv2.putText(image, f"{hand_type}: {direction}, {gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
