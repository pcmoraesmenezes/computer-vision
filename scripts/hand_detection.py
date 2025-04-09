import cv2
import mediapipe as mp
import os
import time
from time import sleep
from pynput.keyboard import Controller


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (0, 255, 255) 

text = '>'

keyboard = Controller()

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands()

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

NOTEPAD_IS_OPEN = False
CHROME_IS_OPEN = False
CALCULATOR_IS_OPEN = False

KEYBORD = [
    [
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'
    ],
    [
        'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
    ],
    [
        'Z', 'X', 'C', 'V', 'B', 'N', 'M'
    ],

    [
         ',', '.', ' '
    ]
]


OFFSET = 50
key_pressed = False
last_key_position = None
key_press_start_time = 0
KEY_PRESS_DURATION = 1.0

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

            all_hands[-1]["hand"] = hand_info

    return img, all_hands


def raise_finger(hand_data):
    finger = []

    for finger_point in [8,12,16,20]:
        if hand_data['coords'][finger_point][1] < hand_data['coords'][finger_point - 2][1]:
            finger.append(True)
        else:
            finger.append(False)
            
    return finger


def show_button(img, position, key, len=50, color=WHITE):
    cv2.rectangle(img, position, (position[0]+len, position[1]+len), color, cv2.FILLED)
    cv2.rectangle(img, position, (position[0]+len, position[1]+len), BLUE, 2)

    cv2.putText(img, key, (position[0]+15, position[1]+30), cv2.FONT_HERSHEY_PLAIN, 1, BLACK, 2)

    return img


def show_progress_button(img, position, key, progress, len=50):
    cv2.rectangle(img, position, (position[0]+len, position[1]+len), WHITE, cv2.FILLED)
    cv2.rectangle(img, position, (position[0]+len, position[1]+len), BLUE, 2)
    
    progress = min(1.0, progress)  
    progress_height = int(len * progress)
    
    if progress > 0:
        progress_top = position[1] + len - progress_height
        cv2.rectangle(img, 
                     (position[0], progress_top), 
                     (position[0]+len, position[1]+len), 
                     YELLOW, cv2.FILLED)
        cv2.rectangle(img, position, (position[0]+len, position[1]+len), BLUE, 2)
    
    cv2.putText(img, key, (position[0]+15, position[1]+30), cv2.FONT_HERSHEY_PLAIN, 1, BLACK, 2)
    
    return img


while True:
    success, img = cam.read()
    
    img = cv2.flip(img, 1)
    
    img, hand_data = find_hand_coords(img) 

    if len(hand_data) == 1:

        finger_status = raise_finger(hand_data[0])

        if hand_data[0]['hand'] == "Left":

            x_aux, y_aux, z_aux = hand_data[0]['coords'][8]
            cv2.putText(img, f'Cam distance: {z_aux}', (850, 50), cv2.FONT_HERSHEY_PLAIN, 1, PURPLE, 2)

            current_key_over = None 
            current_key_char = None 
            
            for index_row, index_key in enumerate(KEYBORD):
                for index, key in enumerate(index_key):
                    if sum(finger_status) <= 1:
                        key = key.lower()
                    
                    key_position = (index, index_row)
                    button_position = (OFFSET + index * 80, OFFSET + index_row * 80)
                    
                    if (OFFSET+index*80 < x_aux < 100+index*80 and 
                        OFFSET+index_row*80 < y_aux < 100+index_row*80):
                        
                        current_key_over = key_position
                        current_key_char = key
                        
                        if z_aux < -85:
                            if last_key_position != key_position:
                                key_press_start_time = time.time()
                                last_key_position = key_position
                            
                            elapsed_time = time.time() - key_press_start_time
                            progress = elapsed_time / KEY_PRESS_DURATION
                            
                            img = show_progress_button(img, button_position, key, progress)
                            
                            if elapsed_time >= KEY_PRESS_DURATION and not key_pressed:
                                text += key
                                keyboard.press(key)
                                keyboard.release(key)
                                key_pressed = True
                                img = show_button(img, button_position, key, color=GREEN)
                        else:
                            img = show_button(img, button_position, key, color=PURPLE)
                            if last_key_position == key_position:
                                key_pressed = False
                    else:
                        img = show_button(img, button_position, key)
            
            if current_key_over is None:
                key_pressed = False
                last_key_position = None
                key_press_start_time = 0

            if finger_status == [False, False, False, True] and len(text) > 1:
                text = text[:-1]
                sleep(0.2)

            cv2.rectangle(img, (OFFSET, 450), (830, 500), WHITE, cv2.FILLED)
            cv2.rectangle(img, (OFFSET, 450), (830, 500), BLUE, 2)
            cv2.putText(img, text[-40:], (OFFSET, 480), cv2.FONT_HERSHEY_PLAIN, 1, BLACK, 2)
            cv2.circle(img, (x_aux, y_aux), 7, BLUE, cv2.FILLED)
            
            if current_key_over is not None and z_aux < -85 and not key_pressed:
                elapsed_time = time.time() - key_press_start_time
                remaining_time = max(0, KEY_PRESS_DURATION - elapsed_time)
                cv2.putText(img, f'Tempo: {remaining_time:.1f}s', (850, 80), 
                           cv2.FONT_HERSHEY_PLAIN, 1, PURPLE, 2)
        else:
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


with open("output.txt", "w") as file:
    file.write(text)
    file.write("\n")


cam.release()
cv2.destroyAllWindows()