import cv2
import mediapipe as mp
import numpy as np
from HandTrackingModule import HandDetector

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# intialize files
with open("scale.txt", "w") as file:
    file.write("")

with open("pan.txt", "w") as file:
    file.write("0 0")

with open("rotate.txt", "w") as file:
    file.write("0")

# constants
scale_factor = 0
min_length = 18.439088914585774
max_length = 200.5356303021603
min_scale = 10143
max_scale = 71189
x_blend = 15
z_blend = 8
min_s_blend = 0.002
max_s_blend = 0.04
rd = 1


# Open the webcam
cap = cv2.VideoCapture(0)

# Create a HandDetector instance
detector = HandDetector(maxHands=2, detectionCon=0.9)

with mp_hands.Hands(
    model_complexity=0, min_detection_confidence=0.9, min_tracking_confidence=0.9
) as hands:
    while True:
        ret, frame = cap.read()
        # Flip the frame horizontally for a later selfie-view display
        # Detect hands in the frame
        frame = cv2.flip(frame, 1)
        hands, frame = detector.findHands(frame, draw=True)
        # Check if at least one hand is detected
        if hands:  # single
            if len(hands) == 1:
                hand1 = hands[0]  # Get the first hand detected
                lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
                bbox1 = hand1[
                    "bbox"
                ]  # Bounding box around the first hand (x,y,w,h coordinates)
                handType1 = hand1["type"]
                fingerup1 = detector.fingersUp(hand1)  # TODO: scale, rotate
                area = bbox1[2] * bbox1[3]
                center1 = hand1["center"]
                x, z = center1[0], center1[1]
                xc = lmList1[8][0]

                fingerup1 = detector.fingersUp(hand1)
                fist = detector.fist(hand1)

                if handType1 == "Left":  # rotate and scale
                    if fingerup1 == [1, 1, 0, 0, 0]:  # rotate
                        length, _, frame = detector.findDistance(
                            lmList1[4][0:2], lmList1[8][0:2], frame
                        )
                        rotate = np.interp(length, [min_length, max_length], [-rd, rd])
                        with open("rotate.txt", "w") as file:
                            file.write(str(float(rotate)))

                        cv2.putText(
                            frame,
                            f"Rotate Factor: {float(rotate)}",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            2,
                        )

                        cv2.putText(
                            frame,
                            f"X , Z: {float(x)},{float(z)}",
                            (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            2,
                        )
                    elif fingerup1 != [1, 1, 0, 0, 0]:  # scale
                        with open("rotate.txt", "w") as file:
                            file.write(str(float(0)))
                        scale_factor = np.interp(
                            area, [min_scale, max_scale], [min_s_blend, max_s_blend]
                        )
                        scale_factor = "{:.5f}".format(scale_factor)
                        with open("scale.txt", "w") as file:
                            file.write(str(float(scale_factor)))

                        cv2.putText(
                            frame,
                            f"Scale Factor: {float(scale_factor)}",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 0, 0),
                            2,
                        )
                else:
                    if fist and fingerup1 != [0, 1, 0, 0, 0]:  # pan
                        with open("rotate.txt", "w") as file:
                            file.write("0")
                        x = np.interp(x, [69, 527], [-x_blend, x_blend])
                        z = np.interp(z, [69, 412], [z_blend, -z_blend])
                        x = "{:.5f}".format(x)
                        z = "{:.5f}".format(z)
                        with open("pan.txt", "w") as file:
                            file.write(str(float(x)))
                            file.write(str(" "))
                            file.write(str(float(z)))

                        cv2.putText(
                            frame,
                            f"X , Z: {float(x)},{float(z)}",
                            (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 0, 255),
                            2,
                        )

                    elif fingerup1 == [0, 1, 0, 0, 0]:  # stop rotate
                        with open("rotate.txt", "w") as file:
                            file.write("0")
                        cv2.putText(
                            frame,
                            "POP",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (180, 200, 70),
                            2,
                        )

                    elif fingerup1 == [0, 1, 1, 1, 1]:  # rotate
                        rotate = np.interp(xc, [56, 537], [-rd, rd])
                        with open("rotate.txt", "w") as file:
                            file.write(str(float(rotate)))

                        cv2.putText(
                            frame,
                            f"Rotate Factor: {float(rotate)}",
                            (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 0),
                            2,
                        )
            else:
                hand1 = hands[0]  # Get the new hand detected
                handType1 = hand1["type"]
                if handType1 == "Right":
                    i = 0
                    j = 1
                else:
                    i = 1
                    j = 0
                hand1 = hands[i]  # Get the new hand detected
                lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
                handType1 = hand1["type"]
                center1 = hand1["center"]
                fingerup1 = detector.fingersUp(hand1)
                area = bbox1[2] * bbox1[3]
                fingerup1 = detector.fingersUp(hand1)

                hand2 = hands[j]
                fingerup2 = detector.fingersUp(hand2)  # TODO: scale+pan, rotate+pan
                lmList2 = hand2["lmList"]
                handType2 = hand2["type"]
                x, z = center1[0], center1[1]
                bbox1 = hand2["bbox"]
                fist = detector.fist(hand1)

                if handType1 == "Right" and fist:
                    with open("rotate.txt", "w") as file:
                        file.write(str(float(0)))
                    x = np.interp(x, [63, 404], [-x_blend, x_blend])
                    z = np.interp(z, [64, 434], [z_blend, -z_blend])  # pan
                    x = "{:.5f}".format(x)
                    z = "{:.5f}".format(z)

                    with open("pan.txt", "w") as file:
                        file.write(str(float(x)))
                        file.write(str(" "))
                        file.write(str(float(z)))

                    cv2.putText(
                        frame,
                        f"X , Z: {float(x)},{float(z)}",
                        (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2,
                    )

                if (
                    handType1 == "Right"
                    and fingerup1 == [1, 1, 0, 0, 0]
                    and fingerup2 != [1, 1, 0, 0, 0]
                ):
                    length, _, img = detector.findDistance(
                        lmList1[4][0:2], lmList1[8][0:2], frame
                    )
                    rotate = np.interp(length, [min_length, max_length], [-rd, rd])
                    with open("rotate.txt", "w") as file:
                        file.write(str(float(rotate)))  # rotate from pan

                    cv2.putText(
                        frame,
                        f"Rotate Factor: {float(rotate)}",
                        (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                    )

                if fingerup2 == [1, 1, 0, 0, 0]:  # rotate
                    length, _, img = detector.findDistance(
                        lmList2[4][0:2], lmList2[8][0:2], frame
                    )
                    rotate = np.interp(length, [min_length, max_length], [-rd, rd])
                    with open("rotate.txt", "w") as file:
                        file.write(str(float(rotate)))  # normal rotate

                    cv2.putText(
                        frame,
                        f"Rotate Factor: {float(rotate)}",
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2,
                    )

                else:
                    scale_factor = np.interp(
                        area, [min_scale, max_scale], [min_s_blend, max_s_blend]
                    )
                    with open("scale.txt", "w") as file:
                        file.write(str(float(scale_factor)))

                    cv2.putText(
                        frame,
                        f"Scale Factor: {float(scale_factor)}",
                        (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 0, 0),
                        2,
                    )

        cv2.imshow("GOD", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
