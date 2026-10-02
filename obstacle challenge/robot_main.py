from picamera2 import Picamera2

import cv2
import time

from vision import (
    PROCESS_WIDTH,
    PROCESS_HEIGHT,
    detect_corridor,
    detect_direction_lines,
    detect_obstacles
)

from navigation import (
    Navigator,
    SEARCH_DIRECTION,
    DECISION_Y
)

from drive_control import RobotDrive


# ============================================================
# HARDVER VEZÉRLÉS
# ============================================================

# Teszteléskor:
ROBOT_CONTROL = False

# Ha készen áll a robot:
# ROBOT_CONTROL = True


# ============================================================
# KAMERA
# Camera V2.1 NoIR - IMX219
# ============================================================

CAMERA_WIDTH = 3280
CAMERA_HEIGHT = 2464


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

picam2.configure(
    config
)

picam2.start()

time.sleep(2)


# ============================================================
# NAVIGÁCIÓ
# ============================================================

navigator = Navigator()


# ============================================================
# ROBOT HARDVER
# ============================================================

robot = None

if ROBOT_CONTROL:

    robot = RobotDrive()


# ============================================================
# FPS
# ============================================================

previous_time = time.time()

fps = 0


# ============================================================
# FŐ CIKLUS
# ============================================================

try:

    while True:

        # ====================================================
        # KAMERA
        # ====================================================

        frame_full = (
            picam2.capture_array()
        )


        # Teljes látómező megmarad.
        # Csak a feldolgozási felbontást
        # csökkentjük.
        frame = cv2.resize(
            frame_full,
            (
                PROCESS_WIDTH,
                PROCESS_HEIGHT
            ),
            interpolation=cv2.INTER_AREA
        )


        # ====================================================
        # FEKETE FALAK / FOLYOSÓ
        # ====================================================

        corridor = detect_corridor(
            frame
        )


        # ====================================================
        # CW / CCW IRÁNYFELISMERÉS
        # ====================================================

        direction_data = None

        if (
            navigator.state
            == SEARCH_DIRECTION
        ):

            direction_data = (
                detect_direction_lines(
                    frame
                )
            )


            navigator.update_direction(
                direction_data["blue_y"],
                direction_data["orange_y"]
            )


            # Döntési zóna
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


        # ====================================================
        # PIROS / ZÖLD AKADÁLYOK
        # ====================================================

        obstacle_data = (
            detect_obstacles(
                frame
            )
        )


        closest_obstacle = (
            obstacle_data[
                "closest"
            ]
        )


        # ====================================================
        # NAVIGÁCIÓ
        # ====================================================

        control = navigator.update(
            corridor,
            closest_obstacle
        )


        steering = (
            control["steering"]
        )

        speed = (
            control["speed"]
        )

        status = (
            control["status"]
        )


        # ====================================================
        # HARDVERVEZÉRLÉS
        # ====================================================

        if ROBOT_CONTROL:

            robot.set_steering_angle(
                steering
            )


            if speed > 0:

                robot.forward(
                    speed
                )

            else:

                robot.stop()


        # ====================================================
        # FALAK KIRAJZOLÁSA
        # ====================================================

        for point in (
            corridor["points"]
        ):

            # Bal fal
            cv2.circle(
                frame,
                (
                    point["left"],
                    point["y"]
                ),
                5,
                (255, 0, 0),
                -1
            )


            # Jobb fal
            cv2.circle(
                frame,
                (
                    point["right"],
                    point["y"]
                ),
                5,
                (255, 0, 0),
                -1
            )


            # Folyosó közepe
            cv2.circle(
                frame,
                (
                    point["center"],
                    point["y"]
                ),
                5,
                (0, 255, 0),
                -1
            )


        # ====================================================
        # AKADÁLYOK KIRAJZOLÁSA
        # ====================================================

        for obj in (
            obstacle_data["objects"]
        ):

            if (
                obj["color"]
                == "RED"
            ):

                box_color = (
                    255,
                    0,
                    0
                )

            else:

                box_color = (
                    0,
                    255,
                    0
                )


            cv2.rectangle(
                frame,
                (
                    obj["x"],
                    obj["y"]
                ),
                (
                    obj["x"]
                    + obj["w"],

                    obj["y"]
                    + obj["h"]
                ),
                box_color,
                2
            )


            cv2.putText(
                frame,
                obj["color"],
                (
                    obj["x"],
                    max(
                        obj["y"] - 10,
                        20
                    )
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                box_color,
                2
            )


        # ====================================================
        # LEGKÖZELEBBI AKADÁLY
        # ====================================================

        if (
            closest_obstacle
            is not None
        ):

            cv2.circle(
                frame,
                (
                    closest_obstacle[
                        "center_x"
                    ],

                    closest_obstacle[
                        "center_y"
                    ]
                ),
                10,
                (255, 255, 255),
                3
            )


        # ====================================================
        # KAMERA KÖZÉPVONALA
        # ====================================================

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

        if delta > 0:

            fps = 1 / delta

        previous_time = (
            current_time
        )


        # ====================================================
        # INFORMÁCIÓ
        # ====================================================

        cv2.putText(
            frame,
            f"STATE: {navigator.state}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            (
                "DIRECTION: "
                f"{navigator.direction}"
            ),
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            f"STATUS: {status}",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            (
                "STEER: "
                f"{steering:.1f}"
            ),
            (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        cv2.putText(
            frame,
            (
                "SPEED: "
                f"{speed * 100:.0f}%"
            ),
            (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        if corridor["valid"]:

            cv2.putText(
                frame,
                (
                    "LATERAL: "
                    f"{corridor['lateral_error']}"
                ),
                (20, 210),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )


            cv2.putText(
                frame,
                (
                    "HEADING: "
                    f"{corridor['heading_error']}"
                ),
                (20, 245),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )


        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 280),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


        # ====================================================
        # KÉP MEGJELENÍTÉSE
        # ====================================================

        display = cv2.cvtColor(
            frame,
            cv2.COLOR_RGB2BGR
        )


        cv2.imshow(
            "WRO Robot",
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

    if (
        ROBOT_CONTROL
        and robot is not None
    ):

        robot.shutdown()


    picam2.stop()

    cv2.destroyAllWindows()