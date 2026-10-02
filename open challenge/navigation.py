# ============================================================
# ÁLLAPOTOK
# ============================================================

SEARCH_DIRECTION = "SEARCH_DIRECTION"
NORMAL_DRIVING = "NORMAL_DRIVING"
AVOID_OBSTACLE = "AVOID_OBSTACLE"
RETURN_TO_PATH = "RETURN_TO_PATH"


# ============================================================
# KORMÁNY
# ============================================================

CENTER_ANGLE = 90

MIN_STEERING_ANGLE = 60
MAX_STEERING_ANGLE = 120


# ============================================================
# PÁLYAKÖVETÉS
# ============================================================

KP_POSITION = 0.08
KP_HEADING = 0.10


# ============================================================
# AKADÁLYKERÜLÉS
# ============================================================

KP_AVOID = 0.10


# ============================================================
# SEBESSÉGEK
# ============================================================

FAST_SPEED = 0.45
NORMAL_SPEED = 0.35
TURN_SPEED = 0.27
AVOID_SPEED = 0.25


# ============================================================
# KÉK / NARANCSSÁRGA IRÁNYFELISMERÉS
# ============================================================

DECISION_Y = 430

Y_TOLERANCE = 10


# ============================================================
# AKADÁLY PARAMÉTEREK
# ============================================================

OBSTACLE_TRIGGER_Y = 400

OBSTACLE_CLEAR_FRAMES = 8

SAFETY_MARGIN = 90


# ============================================================
# AKADÁLYKERÜLÉSI OLDAL
# ============================================================

# Ezt a konkrét versenyszabályhoz
# igazítsuk véglegesen.

PASS_SIDE = {
    "RED": "RIGHT",
    "GREEN": "LEFT"
}


# ============================================================
# NAVIGÁTOR
# ============================================================

class Navigator:

    def __init__(self):

        self.state = (
            SEARCH_DIRECTION
        )

        self.direction = None

        self.no_obstacle_counter = 0

        self.current_obstacle_color = (
            None
        )

        self.image_width = 820

        self.image_center = (
            self.image_width // 2
        )


    # ========================================================
    # CW / CCW IRÁNY FELISMERÉSE
    # ========================================================

    def update_direction(
        self,
        blue_y,
        orange_y
    ):

        # Ha már egyszer eldöntöttük,
        # nem változtatjuk meg.
        if self.direction is not None:

            return


        blue_close = (
            blue_y is not None
            and blue_y > DECISION_Y
        )

        orange_close = (
            orange_y is not None
            and orange_y > DECISION_Y
        )


        # Egyik vonal sincs még közel.
        if (
            not blue_close
            and not orange_close
        ):

            return


        # Mindkettő látszik.
        if (
            blue_y is not None
            and orange_y is not None
        ):

            difference = (
                orange_y
                - blue_y
            )

            # Narancssárga van közelebb.
            if (
                difference
                > Y_TOLERANCE
            ):

                self.direction = "CW"

            # Kék van közelebb.
            elif (
                difference
                < -Y_TOLERANCE
            ):

                self.direction = "CCW"


        # Csak a narancssárga van közel.
        elif orange_close:

            self.direction = "CW"


        # Csak a kék van közel.
        elif blue_close:

            self.direction = "CCW"


        if self.direction is not None:

            self.state = (
                NORMAL_DRIVING
            )

            print(
                "MENETIRANY:",
                self.direction
            )


    # ========================================================
    # FAL / FOLYOSÓ KÖVETÉS
    # ========================================================

    def wall_follow(
        self,
        corridor
    ):

        if not corridor["valid"]:

            return {
                "steering": CENTER_ANGLE,
                "speed": 0,
                "status": "NO PATH"
            }


        lateral_error = (
            corridor[
                "lateral_error"
            ]
        )

        heading_error = (
            corridor[
                "heading_error"
            ]
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


        total_error = (
            abs(lateral_error)
            + abs(heading_error)
        )


        if total_error < 30:

            speed = FAST_SPEED

        elif total_error < 90:

            speed = NORMAL_SPEED

        else:

            speed = TURN_SPEED


        return {
            "steering": steering,
            "speed": speed,
            "status": "WALL FOLLOW"
        }


    # ========================================================
    # AKADÁLY KÖZELSÉG
    # ========================================================

    def obstacle_is_close(
        self,
        obstacle
    ):

        if obstacle is None:

            return False

        return (
            obstacle["bottom_y"]
            > OBSTACLE_TRIGGER_Y
        )


    # ========================================================
    # AKADÁLYKERÜLÉS
    # ========================================================

    def avoid_obstacle(
        self,
        obstacle
    ):

        color = (
            obstacle["color"]
        )

        side = (
            PASS_SIDE[color]
        )


        # ----------------------------------------------------
        # KERÜLÉSI CÉLPONT
        # ----------------------------------------------------

        if side == "RIGHT":

            target_x = (
                obstacle["x"]
                + obstacle["w"]
                + SAFETY_MARGIN
            )

        else:

            target_x = (
                obstacle["x"]
                - SAFETY_MARGIN
            )


        target_x = max(
            0,
            min(
                self.image_width - 1,
                target_x
            )
        )


        error = (
            target_x
            - self.image_center
        )


        steering = (
            CENTER_ANGLE
            + KP_AVOID
            * error
        )


        steering = max(
            MIN_STEERING_ANGLE,
            min(
                MAX_STEERING_ANGLE,
                steering
            )
        )


        return {
            "steering": steering,
            "speed": AVOID_SPEED,
            "status": (
                f"AVOID {color} "
                f"PASS {side}"
            )
        }


    # ========================================================
    # FŐ NAVIGÁCIÓS DÖNTÉS
    # ========================================================

    def update(
        self,
        corridor,
        closest_obstacle
    ):

        # ----------------------------------------------------
        # KÖZELI AKADÁLY MINDENT FELÜLÍR
        # ----------------------------------------------------

        if self.obstacle_is_close(
            closest_obstacle
        ):

            self.state = (
                AVOID_OBSTACLE
            )

            self.current_obstacle_color = (
                closest_obstacle[
                    "color"
                ]
            )

            self.no_obstacle_counter = 0

            return self.avoid_obstacle(
                closest_obstacle
            )


        # ----------------------------------------------------
        # AKADÁLY ELTŰNT
        # ----------------------------------------------------

        if (
            self.state
            == AVOID_OBSTACLE
        ):

            self.no_obstacle_counter += 1

            if (
                self.no_obstacle_counter
                < OBSTACLE_CLEAR_FRAMES
            ):

                return {
                    "steering": CENTER_ANGLE,
                    "speed": AVOID_SPEED,
                    "status":
                        "CLEARING OBSTACLE"
                }


            self.state = (
                RETURN_TO_PATH
            )


        # ----------------------------------------------------
        # VISSZATÉRÉS A FOLYOSÓ KÖZEPÉRE
        # ----------------------------------------------------

        if (
            self.state
            == RETURN_TO_PATH
        ):

            result = self.wall_follow(
                corridor
            )

            result["status"] = (
                "RETURN TO PATH"
            )

            if (
                corridor["valid"]
                and abs(
                    corridor[
                        "lateral_error"
                    ]
                ) < 30
            ):

                self.state = (
                    NORMAL_DRIVING
                )

            return result


        # ----------------------------------------------------
        # NORMÁL HALADÁS
        # ----------------------------------------------------

        return self.wall_follow(
            corridor
        )