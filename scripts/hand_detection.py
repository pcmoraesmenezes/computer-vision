import cv2
import mediapipe as mp
import os


mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands()

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

NOTEPAD_IS_OPEN = False
CHROME_IS_OPEN = False
CALCULATOR_IS_OPEN = False

def find_hand_coords(img, switch_side=False):
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_img)

    all_hands = []
    if results.multi_hand_landmarks:
        for hand_side, hand_landmarks in zip(results.multi_handedness, results.multi_hand_landmarks):
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            hand_metadata = {}
            coords = []

            for marker in hand_landmarks.landmark:
                coord_x, coord_y, coord_z = int(marker.x * 1280), int(marker.y * 720), int(marker.z * 1280)

                coords.append((coord_x, coord_y, coord_z))

                cv2.putText(img, f"x: {coord_x}, y: {coord_y}, z: {coord_z}", (coord_x, coord_y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                cv2.circle(img, (coord_x, coord_y), 5, (0, 255, 0), cv2.FILLED)

            hand_metadata["coords"] = coords
            all_hands.append(hand_metadata)

            if switch_side:
                if hand_side.classification[0].label == "Left":
                    hand_info = "Right"
                else:
                    hand_info = "Left"
            else:
                hand_info = hand_side.classification[0].label

    return img, all_hands


def raise_finger(hand_data):
    finger = []

    for finger_point in [8,12,16,20]:
        if hand_data['coords'][finger_point][1] < hand_data['coords'][finger_point - 2][1]:
            finger.append(True)
        else:
            finger.append(False)
            
    return finger


while True:
    success, img = cam.read()
    
    img = cv2.flip(img, 1)
    
    img, hand_data = find_hand_coords(img) 

    if len(hand_data) == 1:
        finger_status = raise_finger(hand_data[0])

        if finger_status == [True, False, False, False] and NOTEPAD_IS_OPEN == False:
            NOTEPAD_IS_OPEN = True
            os.startfile(r"C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2501.31.0_x64__8wekyb3d8bbwe\Notepad\Notepad.exe")

        if finger_status == [True, True, False, False] and CHROME_IS_OPEN == False:
            CHROME_IS_OPEN = True
            os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")

        if finger_status == [True, True, True, False] and CALCULATOR_IS_OPEN == False:
            CALCULATOR_IS_OPEN = True
            os.startfile(r"C:\Program Files\WindowsApps\Microsoft.WindowsCalculator_11.2502.2.0_x64__8wekyb3d8bbwe\CalculatorApp.exe")

        if finger_status == [False, False, False, False]:
            NOTEPAD_IS_OPEN = False
            # CHROME_IS_OPEN = False
            CALCULATOR_IS_OPEN = False
            os.system("taskkill /f /im notepad.exe")
            # os.system("taskkill /f /im chrome.exe")
            os.system("taskkill /f /im Calculator.exe")

        if finger_status == [True, False, False, True]:
            break
    
    cv2.imshow("Image", img)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()