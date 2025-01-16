# Hand Gesture Control for PowerPoint Presentation

## Problem Description:
This program enables controlling a PowerPoint presentation through hand gestures. The gestures are recognized using a webcam, and the corresponding keyboard shortcuts are simulated to control the presentation.

### Key Gestures:
- **Thumb up** — Press the spacebar (play or pause a video).
- **Thumb down** — Press the Escape key (stop the presentation).
- **Left hand** — Press the left arrow key (go to the previous slide).
- **Right hand** — Press the right arrow key (go to the next slide).

The program works in the background, analyzing the webcam feed, and sends corresponding commands to the system (simulating key presses) based on the recognized gestures.

---

## How to Use

### Required Libraries:
To run the program, you need to install the following Python libraries:

1. `opencv-python` — For webcam handling and displaying images.
2. `mediapipe` — For hand gesture recognition.
3. `pyautogui` — For simulating keyboard presses (e.g., spacebar, arrow keys, Escape).

You can install these libraries using the following command:

```bash
pip install opencv-python mediapipe pyautogui
```
## Instructions:

### 1. Run the Program
Execute the Python script (`.py` file). The program will start the webcam and begin detecting hand gestures.

### 2. Grant Camera and Keyboard Access
Upon running the program, your system will ask for permission to access your camera. Grant access to allow gesture recognition. Additionally, the program requires keyboard access to simulate key presses.

### 3. Start PowerPoint
Make sure you have a PowerPoint presentation open and ready. The program will send keyboard commands to control the presentation (move slides forward/backward or play/pause).

### 4. Gestures to Control the Presentation:
- **Thumb Up** — Play or Pause the presentation (simulates pressing the spacebar).
- **Thumb Down** — Stop the presentation (simulates pressing Escape).
- **Left Hand Gesture** — Move to the previous slide (simulates pressing the left arrow key).
- **Right Hand Gesture** — Move to the next slide (simulates pressing the right arrow key).

### 5. How the Program Works
The program continuously analyzes the webcam feed and takes actions based on the recognized gestures. Ensure your hand is positioned correctly for accurate gesture detection. 

- If the thumb is pointing up, it will trigger a play/pause action.
- If the thumb is pointing down, it will stop the presentation.
- If the hand is positioned to the left or right, it will navigate to the previous or next slide, respectively.

### 6. Additional Notes:
- The program works in the background and communicates with PowerPoint or any other presentation software that supports keyboard commands.
- Adjust lighting and hand positions to ensure accurate gesture detection.
- There are short delays between recognizing each gesture to avoid repeated actions.

---

## Troubleshooting:

- **Camera not detected:** Ensure the camera is properly connected, and the program has permission to access it.
- **No gesture recognition:** Try to keep your hand in the frame, and ensure the gesture is clear and distinct (e.g., thumb fully extended).
- **Keyboard not responding:** Make sure PowerPoint or another presentation application is active and focused on the screen.

---

**Authors:** Marta Szpilka and Jakub Więcek
