import cv2
import numpy as np


# ============================================================
# FELDOLGOZÁSI FELBONTÁS
# ============================================================

PROCESS_WIDTH = 820
PROCESS_HEIGHT = 616


# ============================================================
# FEKETE FALAK
# ============================================================

BLACK_THRESHOLD = 80

SCAN_ROWS = [
    int(PROCESS_HEIGHT * 0.50),
    int(PROCESS_HEIGHT * 0.60),
    int(PROCESS_HEIGHT * 0.70),
    int(PROCESS_HEIGHT * 0.80),
    int(PROCESS_HEIGHT * 0.88)
]

MIN_CORRIDOR_WIDTH = 100


# ============================================================
# KÉK / NARANCSSÁRGA IRÁNYJELZŐ VONALAK
# ============================================================

LOWER_BLUE = np.array([95, 80, 50])
UPPER_BLUE = np.array([140, 255, 255])

LOWER_ORANGE = np.array([5, 100, 80])
UPPER_ORANGE = np.array([25, 255, 255])

COLOR_LINE_MIN_AREA = 700


# ============================================================
# PIROS / ZÖLD AKADÁLYOK
# ============================================================

LOWER_GREEN = np.array([35, 70, 50])
UPPER_GREEN = np.array([85, 255, 255])

LOWER_RED1 = np.array([0, 70, 50])
UPPER_RED1 = np.array([10, 255, 255])

LOWER_RED2 = np.array([170, 70, 50])
UPPER_RED2 = np.array([179, 255, 255])

OBSTACLE_MIN_AREA = 500


# ============================================================
# MORFOLÓGIA
# ============================================================

kernel = np.ones(
    (5, 5),
    np.uint8
)


# ============================================================
# FAL KERESÉSE EGY SORBAN
# ============================================================

def find_walls(binary, y):

    row = binary[y]

    image_center = PROCESS_WIDTH // 2

    left_wall = None
    right_wall = None

    # Bal fal keresése
    for x in range(
        image_center,
        5,
        -1
    ):

        if row[x] == 0:

            left_wall = x
            break

    # Jobb fal keresése
    for x in range(
        image_center,
        PROCESS_WIDTH - 5
    ):

        if row[x] == 0:

            right_wall = x
            break

    return left_wall, right_wall


# ============================================================
# FOLYOSÓ / PÁLYA FELISMERÉSE
# ============================================================

def detect_corridor(frame):

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

    for y in SCAN_ROWS:

        left_wall, right_wall = find_walls(
            binary,
            y
        )

        if (
            left_wall is None
            or right_wall is None
        ):
            continue

        corridor_width = (
            right_wall - left_wall
        )

        if (
            corridor_width
            < MIN_CORRIDOR_WIDTH
        ):
            continue

        center_x = (
            left_wall + right_wall
        ) // 2

        points.append({
            "y": y,
            "left": left_wall,
            "right": right_wall,
            "center": center_x,
            "width": corridor_width
        })

    result = {
        "binary": binary,
        "points": points,
        "valid": False,
        "center": None,
        "lateral_error": 0,
        "heading_error": 0
    }

    if len(points) < 2:

        return result

    image_center = (
        PROCESS_WIDTH // 2
    )

    # Az alsó két mérés alapján
    # becsüljük a robot oldalhelyzetét.
    near_points = points[-2:]

    near_center = int(
        np.mean(
            [
                p["center"]
                for p in near_points
            ]
        )
    )

    lateral_error = (
        near_center
        - image_center
    )

    # ========================================================
    # PÁLYA IRÁNYA
    # ========================================================

    far_center = (
        points[0]["center"]
    )

    near_center_heading = (
        points[-1]["center"]
    )

    # Pozitív -> a pálya jobbra tart
    # Negatív -> a pálya balra tart
    heading_error = (
        far_center
        - near_center_heading
    )

    result["valid"] = True
    result["center"] = near_center
    result["lateral_error"] = (
        lateral_error
    )
    result["heading_error"] = (
        heading_error
    )

    return result


# ============================================================
# KONTÚROK -> OBJEKTUM ADATOK
# ============================================================

def contours_to_objects(
    contours,
    color,
    min_area
):

    objects = []

    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area < min_area:

            continue

        x, y, w, h = cv2.boundingRect(
            contour
        )

        objects.append({
            "color": color,
            "x": x,
            "y": y,
            "w": w,
            "h": h,

            "center_x": (
                x + w // 2
            ),

            "center_y": (
                y + h // 2
            ),

            "bottom_y": (
                y + h
            ),

            "area": area
        })

    return objects


# ============================================================
# KÉK / NARANCSSÁRGA VONALAK
# ============================================================

def detect_direction_lines(frame):

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2HSV
    )

    blue_mask = cv2.inRange(
        hsv,
        LOWER_BLUE,
        UPPER_BLUE
    )

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

    blue_mask = cv2.morphologyEx(
        blue_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    orange_mask = cv2.morphologyEx(
        orange_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    orange_mask = cv2.morphologyEx(
        orange_mask,
        cv2.MORPH_CLOSE,
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

    blue_objects = (
        contours_to_objects(
            blue_contours,
            "BLUE",
            COLOR_LINE_MIN_AREA
        )
    )

    orange_objects = (
        contours_to_objects(
            orange_contours,
            "ORANGE",
            COLOR_LINE_MIN_AREA
        )
    )

    blue_y = None
    orange_y = None

    if blue_objects:

        blue_y = max(
            obj["bottom_y"]
            for obj in blue_objects
        )

    if orange_objects:

        orange_y = max(
            obj["bottom_y"]
            for obj in orange_objects
        )

    return {
        "blue_y": blue_y,
        "orange_y": orange_y,
        "blue_objects": blue_objects,
        "orange_objects": orange_objects
    }


# ============================================================
# PIROS / ZÖLD AKADÁLYOK
# ============================================================

def detect_obstacles(frame):

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_RGB2HSV
    )

    green_mask = cv2.inRange(
        hsv,
        LOWER_GREEN,
        UPPER_GREEN
    )

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

    objects = []

    objects.extend(
        contours_to_objects(
            green_contours,
            "GREEN",
            OBSTACLE_MIN_AREA
        )
    )

    objects.extend(
        contours_to_objects(
            red_contours,
            "RED",
            OBSTACLE_MIN_AREA
        )
    )

    if not objects:

        return {
            "objects": [],
            "closest": None
        }

    # A kép aljához legközelebb eső
    # objektumot tekintjük legközelebbinek.
    closest = max(
        objects,
        key=lambda obj: (
            obj["bottom_y"],
            obj["area"]
        )
    )

    return {
        "objects": objects,
        "closest": closest
    }