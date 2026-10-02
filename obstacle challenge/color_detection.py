from picamera2 import Picamera2

import cv2
import numpy as np
import time


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
# ZÓNÁK
# ============================================================

LEFT_LIMIT = (
    PROCESS_WIDTH // 3
)

RIGHT_LIMIT = (
    2 * PROCESS_WIDTH // 3
)


# ============================================================
# MINIMUM OBJEKTUMMÉRET
# ============================================================

MIN_AREA = 500


# ============================================================
# HSV - ZÖLD
# ============================================================

LOWER_GREEN = np.array(
    [35, 70, 50]
)

UPPER_GREEN = np.array(
    [85, 255, 255]
)


# ============================================================
# HSV - PIROS
# ============================================================

LOWER_RED1 = np.array(
    [0, 70, 50]
)

UPPER_RED1 = np.array(
    [10, 255, 255]
)

LOWER_RED2 = np.array(
    [170, 70, 50]
)

UPPER_RED2 = np.array(
    [179, 255, 255]
)


# ============================================================
# POZÍCIÓ
# ============================================================

def get_position(
    center_x
):

    if (
        center_x
        < LEFT_LIMIT
    ):

        return "BAL"

    elif (
        center_x
        < RIGHT_LIMIT
    ):

        return "KOZEP"

    else:

        return "JOBB"


# ============================================================
# MORFOLÓGIA
# ============================================================

kernel = np.ones(
    (5, 5),
    np.uint8
)


# ============================================================
# FPS
# ============================================================

previous_time = time.time()

fps = 0


# ============================================================
# FŐ CIKLUS
# ============================================================

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


    # ========================================================
    # ZÖLD
    # ========================================================

    green_mask = cv2.inRange(
        hsv,
        LOWER_GREEN,
        UPPER_GREEN
    )


    # ========================================================
    # PIROS
    # ========================================================

    red_mask1 = cv2.inRange(
        hsv,
        LOWER_RED1,
        UPPER_RED1
    )

    red_mask2 = cv2.inRange(
        hsv,
        LOWER_RED2,
        UPPER_RED2
    )

    red_mask = cv2.bitwise_or(
        red_mask1,
        red_mask2
    )


    # ========================================================
    # ZAJSZŰRÉS
    # ========================================================

    green_mask = cv2.morphologyEx(
        green_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    green_mask = cv2.morphologyEx(
        green_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    red_mask = cv2.morphologyEx(
        red_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    red_mask = cv2.morphologyEx(
        red_mask,
        cv2.MORPH_CLOSE,
        kernel
    )


    # ========================================================
    # KONTÚROK
    # ========================================================

    green_contours, _ = (
        cv2.findContours(
            green_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
    )

    red_contours, _ = (
        cv2.findContours(
            red_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
    )


    # ========================================================
    # ZÖLD OBJEKTUMOK
    # ========================================================

    for contour in (
        green_contours
    ):

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

        center_x = (
            x + w // 2
        )

        center_y = (
            y + h // 2
        )

        position = (
            get_position(
                center_x
            )
        )


        cv2.rectangle(
            frame,
            (x, y),
            (
                x + w,
                y + h
            ),
            (0, 255, 0),
            2
        )


        cv2.circle(
            frame,
            (
                center_x,
                center_y
            ),
            6,
            (0, 255, 0),
            -1
        )


        cv2.putText(
            frame,
            f"GREEN {position}",
            (
                x,
                max(
                    y - 10,
                    25
                )
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )


    # ========================================================
    # PIROS OBJEKTUMOK
    # ========================================================

    for contour in (
        red_contours
    ):

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

        center_x = (
            x + w // 2
        )

        center_y = (
            y + h // 2
        )

        position = (
            get_position(
                center_x
            )
        )


        cv2.rectangle(
            frame,
            (x, y),
            (
                x + w,
                y + h
            ),
            (255, 0, 0),
            2
        )


        cv2.circle(
            frame,
            (
                center_x,
                center_y
            ),
            6,
            (255, 0, 0),
            -1
        )


        cv2.putText(
            frame,
            f"RED {position}",
            (
                x,
                max(
                    y - 10,
                    25
                )
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )


    # ========================================================
    # ZÓNÁK
    # ========================================================

    cv2.line(
        frame,
        (
            LEFT_LIMIT,
            0
        ),
        (
            LEFT_LIMIT,
            PROCESS_HEIGHT
        ),
        (255, 255, 255),
        1
    )


    cv2.line(
        frame,
        (
            RIGHT_LIMIT,
            0
        ),
        (
            RIGHT_LIMIT,
            PROCESS_HEIGHT
        ),
        (255, 255, 255),
        1
    )


    # ========================================================
    # FPS
    # ========================================================

    current_time = (
        time.time()
    )

    delta = (
        current_time
        - previous_time
    )

    if delta > 0:

        fps = 1 / delta

    previous_time = (
        current_time
    )


    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )


    # ========================================================
    # MEGJELENÍTÉS
    # ========================================================

    display = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2BGR
    )

    cv2.imshow(
        "Red Green Detection",
        display
    )


    if (
        cv2.waitKey(1)
        & 0xFF
        == ord("q")
    ):

        break


picam2.stop()

cv2.destroyAllWindows()