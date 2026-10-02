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
# PARAMÉTEREK
# ============================================================

BLACK_THRESHOLD = 80

MIN_CORRIDOR_WIDTH = 100


SCAN_ROWS = [
    int(PROCESS_HEIGHT * 0.50),
    int(PROCESS_HEIGHT * 0.60),
    int(PROCESS_HEIGHT * 0.70),
    int(PROCESS_HEIGHT * 0.80),
    int(PROCESS_HEIGHT * 0.88)
]


CENTER_ANGLE = 90

MIN_STEERING_ANGLE = 60
MAX_STEERING_ANGLE = 120


KP_POSITION = 0.08
KP_HEADING = 0.10


CENTER_TOLERANCE = 10


# ============================================================
# FAL KERESÉSE
# ============================================================

def find_walls(
    binary,
    y
):

    row = binary[y]

    center = (
        PROCESS_WIDTH // 2
    )

    left_wall = None
    right_wall = None


    for x in range(
        center,
        5,
        -1
    ):

        if row[x] == 0:

            left_wall = x
            break


    for x in range(
        center,
        PROCESS_WIDTH - 5
    ):

        if row[x] == 0:

            right_wall = x
            break


    return (
        left_wall,
        right_wall
    )


# ============================================================
# FŐ CIKLUS
# ============================================================

kernel = np.ones(
    (5, 5),
    np.uint8
)


previous_time = (
    time.time()
)


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


        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2GRAY
        )


        _, binary = cv2.threshold(
            gray,
            BLACK_THRESHOLD,
            255,
            cv2.THRESH_BINARY
        )


        binary = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            kernel
        )


        binary = cv2.morphologyEx(
            binary,
            cv2.MORPH_CLOSE,
            kernel
        )


        points = []


        # ====================================================
        # FALAK
        # ====================================================

        for y in SCAN_ROWS:

            left, right = (
                find_walls(
                    binary,
                    y
                )
            )


            if (
                left is None
                or right is None
            ):

                continue


            width = (
                right - left
            )


            if (
                width
                < MIN_CORRIDOR_WIDTH
            ):

                continue


            center = (
                left + right
            ) // 2


            points.append({
                "x": center,
                "y": y,
                "left": left,
                "right": right
            })


            cv2.circle(
                frame,
                (left, y),
                5,
                (255, 0, 0),
                -1
            )


            cv2.circle(
                frame,
                (right, y),
                5,
                (255, 0, 0),
                -1
            )


            cv2.circle(
                frame,
                (center, y),
                5,
                (0, 255, 0),
                -1
            )


        # ====================================================
        # IRÁNY ÉS HELYZET
        # ====================================================

        lateral_error = 0
        heading_error = 0

        steering = CENTER_ANGLE

        path_status = "NO PATH"


        if len(points) >= 2:

            image_center = (
                PROCESS_WIDTH // 2
            )


            near_center = int(
                np.mean(
                    [
                        points[-1]["x"],
                        points[-2]["x"]
                    ]
                )
            )


            lateral_error = (
                near_center
                - image_center
            )


            far_center = (
                points[0]["x"]
            )


            heading_error = (
                far_center
                - points[-1]["x"]
            )


            steering = (
                CENTER_ANGLE
                + KP_POSITION
                * lateral_error
                + KP_HEADING
                * heading_error
            )


            steering = max(
                MIN_STEERING_ANGLE,
                min(
                    MAX_STEERING_ANGLE,
                    steering
                )
            )


            if (
                heading_error > 30
            ):

                path_status = (
                    "RIGHT TURN"
                )

            elif (
                heading_error < -30
            ):

                path_status = (
                    "LEFT TURN"
                )

            else:

                path_status = (
                    "STRAIGHT"
                )


        # ====================================================
        # FPS
        # ====================================================

        current_time = (
            time.time()
        )

        delta = (
            current_time
            - previous_time
        )

        fps = (
            1 / delta
            if delta > 0
            else 0
        )

        previous_time = (
            current_time
        )


        # ====================================================
        # KIJELZÉS
        # ====================================================

        cv2.putText(
            frame,
            (
                "PATH: "
                f"{path_status}"
            ),
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            (
                "LATERAL: "
                f"{lateral_error}"
            ),
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            (
                "HEADING: "
                f"{heading_error}"
            ),
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            (
                "STEERING: "
                f"{steering:.1f}"
            ),
            (20, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )


        cv2.line(
            frame,
            (
                PROCESS_WIDTH // 2,
                0
            ),
            (
                PROCESS_WIDTH // 2,
                PROCESS_HEIGHT
            ),
            (255, 255, 0),
            2
        )


        display = cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2BGR
        )


        cv2.imshow(
            "Wall Follow Test",
            display
        )


        cv2.imshow(
            "Binary",
            binary
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