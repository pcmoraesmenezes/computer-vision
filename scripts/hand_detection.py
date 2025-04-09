import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands()

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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

while True:
    success, img = cam.read()
    
    img = cv2.flip(img, 1)
    
    img, hand_data = find_hand_coords(img)  # Correctly unpack the tuple
    
    cv2.imshow("Image", img)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()