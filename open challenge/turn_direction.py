from picamera2 import Picamera2

import cv2
import numpy as np
import time
from collections import deque


# ============================================================
# KAMERA
# ============================================================

CAMERA_WIDTH = 3280
CAMERA_HEIGHT = 2464

PROCESS_WIDTH = 820
PROCESS_HEIGHT = 616


picam2 = Picamera2()

config = (
    picam2.create_preview_configuration(
        main={
            "size": (
                CAMERA_WIDTH,
                CAMERA_HEIGHT
            ),
            "format": "RGB888"
        }
    )
)

picam2.configure(config)

picam2.start()

time.sleep(2)


# ============================================================
# SZÍNHATÁROK
# ============================================================

LOWER_BLUE = np.array(
    [95, 80, 50]
)

UPPER_BLUE = np.array(
    [140, 255, 255]
)


LOWER_ORANGE = np.array(
    [5, 100, 80]
)

UPPER_ORANGE = np.array(
    [25, 255, 255]
)


# ============================================================
# PARAMÉTEREK
# ============================================================

MIN_AREA = 700

DECISION_Y = int(
    PROCESS_HEIGHT * 0.70
)

Y_TOLERANCE = 10


kernel = np.ones(
    (5, 5),
    np.uint8
)


history = deque(
    maxlen=7
)


# ============================================================
# LEGKÖZELEBBI SZÍNES OBJEKTUM
# ============================================================

def get_closest_object(
    contours
):

    objects = []

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area < MIN_AREA:

            continue


        x, y, w, h = (
            cv2.boundingRect(
                contour
            )
        )


        objects.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "bottom_y": y + h
        })


    if not objects:

        return None


    return max(
        objects,
        key=lambda obj: (
            obj["bottom_y"]
        )
    )


# ============================================================
# FŐ CIKLUS
# ============================================================

try:

    while True:

        frame_full = (
            picam2.capture_array()
        )


        frame = cv2.resize(
            frame_full,
            (
                PROCESS_WIDTH,
                PROCESS_HEIGHT
            ),
            interpolation=cv2.INTER_AREA
        )


        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2HSV
        )


        # ====================================================
        # KÉK
        # ====================================================

        blue_mask = cv2.inRange(
            hsv,
            LOWER_BLUE,
            UPPER_BLUE
        )


        # ====================================================
        # NARANCSSÁRGA
        # ====================================================

        orange_mask = cv2.inRange(
            hsv,
            LOWER_ORANGE,
            UPPER_ORANGE
        )


        blue_mask = cv2.morphologyEx(
            blue_mask,
            cv2.MORPH_OPEN,
            kernel
        )

        orange_mask = cv2.morphologyEx(
            orange_mask,
            cv2.MORPH_OPEN,
            kernel
        )


        blue_contours, _ = (
            cv2.findContours(
                blue_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
        )


        orange_contours, _ = (
            cv2.findContours(
                orange_mask,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
        )


        blue = get_closest_object(
            blue_contours
        )

        orange = get_closest_object(
            orange_contours
        )


        direction = None


        blue_close = (
            blue is not None
            and blue["bottom_y"]
            > DECISION_Y
        )


        orange_close = (
            orange is not None
            and orange["bottom_y"]
            > DECISION_Y
        )


        # ====================================================
        # DÖNTÉS
        # ====================================================

        if (
            blue is not None
            and orange is not None
            and (
                blue_close
                or orange_close
            )
        ):

            difference = (
                orange["bottom_y"]
                - blue["bottom_y"]
            )


            if (
                difference
                > Y_TOLERANCE
            ):

                direction = "CW"

            elif (
                difference
                < -Y_TOLERANCE
            ):

                direction = "CCW"


        elif orange_close:

            direction = "CW"


        elif blue_close:

            direction = "CCW"


        if direction is not None:

            history.append(
                direction
            )


        # ====================================================
        # STABIL IRÁNY
        # ====================================================

        stable = "UNKNOWN"


        if len(history) > 0:

            cw_count = (
                history.count("CW")
            )

            ccw_count = (
                history.count("CCW")
            )


            if cw_count > ccw_count:

                stable = "CW"

            elif ccw_count > cw_count:

                stable = "CCW"


        # ====================================================
        # KIRAJZOLÁS
        # ====================================================

        cv2.line(
            frame,
            (0, DECISION_Y),
            (
                PROCESS_WIDTH,
                DECISION_Y
            ),
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            f"DIRECTION: {direction}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            f"STABLE: {stable}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        display = cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2BGR
        )


        cv2.imshow(
            "Direction Detection",
            display
        )


        if (
            cv2.waitKey(1)
            & 0xFF
            == ord("q")
        ):

            break


except KeyboardInterrupt:

    pass


finally:

    picam2.stop()

    cv2.destroyAllWindows()