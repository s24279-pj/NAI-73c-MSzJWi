#####################################
#                                   #
#   Marta Szpilka, Jakub Więcek     #
#                                   #
#####################################

import cv2
import mediapipe as mp
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_gesture = mp.solutions.hands.Hands


def detect_hand_direction(hand_landmarks):
    """
    Określa poziomy kierunek dłoni (lewo lub prawo) na podstawie pozycji kciuka i środkowego palca.

    Argumenty:
        hand_landmarks: Punkty charakterystyczne dłoni wykryte przez MediaPipe.

    Zwraca:
        str: "LEFT" (lewo), "RIGHT" (prawo) lub "UNKNOWN" (nieznany) w zależności od orientacji dłoni.
    """
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Jeżeli dłoń jest w poziomie (jeśli różnica w osi X jest większa niż w osi Y)
    if abs(thumb_tip.x - middle_tip.x) > abs(thumb_tip.y - middle_tip.y) - 0.1:
        if thumb_tip.x < middle_tip.x:
            return "LEFT"  # Kciuk po lewej stronie, ręka skierowana w lewo
        else:
            return "RIGHT"  # Kciuk po prawej stronie, ręka skierowana w prawo
    else:
        return "UNKNOWN"  # Ręka nie jest w poziomie


def is_thumb_up(hand_landmarks):
    """
    Sprawdza, czy wykryto gest "kciuk w górę".

    Argumenty:
        hand_landmarks: Punkty charakterystyczne dłoni wykryte przez MediaPipe.

    Zwraca:
        bool: True, jeśli wykryto gest "kciuk w górę", w przeciwnym razie False.
    """

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

def is_thumb_down(hand_landmarks):
    """
    Sprawdza, czy wykryto gest "kciuk w dół".

    Argumenty:
        hand_landmarks: Punkty charakterystyczne dłoni wykryte przez MediaPipe.

    Zwraca:
        bool: True, jeśli wykryto gest "kciuk w dół", w przeciwnym razie False.
    """

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
    if (thumb_tip.y > index_tip.y and
            thumb_tip.y > middle_tip.y and
            thumb_tip.y > ring_tip.y and
            thumb_tip.y > pinky_tip.y and

            # Sprawdzamy, czy końcówki palców są blisko podstawy (czy są zgięte)
            abs(index_tip.x - thumb_tip.x) < abs(index_base.x - thumb_tip.x) and
            abs(middle_tip.x - thumb_tip.x) < abs(middle_base.x - thumb_tip.x) and
            abs(ring_tip.x - thumb_tip.x) < abs(ring_base.x - thumb_tip.x) and
            abs(pinky_tip.x - thumb_tip.x) < abs(pinky_base.x - thumb_tip.x)
    ):
        return True


cap = cv2.VideoCapture(0)
with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
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

                # Określenie kierunku dłoni
                direction = detect_hand_direction(hand_landmarks)
                hand_type = handedness.classification[0].label

                # Korekta dla lustrzanego odbicia
                if hand_type == "Right":
                    hand_type = "Left"
                else:
                    hand_type = "Right"

                # Rozpoznawanie gestów
                if is_thumb_up(hand_landmarks):
                    gesture = "Thumb up"
                    pyautogui.press('space')
                    print("Spacja wciśnięta!")
                    time.sleep(1)  # Opóźnienie 1 sekundy po naciśnięciu spacji
                elif is_thumb_down(hand_landmarks):
                        gesture = "Thumb down"
                        pyautogui.press('ESC')
                        print("KCIUK W DÓŁ")
                        time.sleep(1)
                else:
                    if direction == "LEFT":
                        gesture = "Left"
                        pyautogui.press('left')
                        print("STRZAŁKA W LEWO")
                        time.sleep(1)  # Opóźnienie 1 sekunde po naciśnięciu strzałki w lewo
                    elif direction == "RIGHT":
                        gesture = "Right"
                        pyautogui.press('right')
                        print("STRZAŁKA W PRAWO")
                        time.sleep(1)  # Opóźnienie 1 sekunde po naciśnięciu strzałki w prawo
                    else:
                        gesture = "UNKNOWN"

                # Wyświetlanie informacji
                print(f"{hand_type}: {direction}, Gest: {gesture}")
                cv2.putText(image, f"{hand_type}: {direction}, {gesture}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
