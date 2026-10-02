from adafruit_servokit import ServoKit
from gpiozero import DigitalOutputDevice, PWMOutputDevice
import time


class RobotDrive:

    def __init__(self):

        # ====================================================
        # PCA9685 + MG996R SERVO
        # ====================================================

        self.pca = ServoKit(
            channels=16,
            address=0x40
        )

        # Servo a PCA9685 0. csatornáján
        self.servo = self.pca.servo[0]

        # MG996R impulzustartomány
        self.servo.set_pulse_width_range(
            700,
            2300
        )

        # ====================================================
        # KORMÁNYSZÖGEK
        # Később mechanikailag kalibrálandók
        # ====================================================

        self.CENTER_ANGLE = 90
        self.LEFT_ANGLE = 60
        self.RIGHT_ANGLE = 120

        # ====================================================
        # TB6612 MOTOR DRIVER
        # ====================================================

        # Raspberry Pi GPIO
        self.ain1 = DigitalOutputDevice(17)
        self.ain2 = DigitalOutputDevice(27)

        self.pwma = PWMOutputDevice(
            18,
            frequency=1000,
            initial_value=0
        )

        self.stby = DigitalOutputDevice(22)

        # TB6612 engedélyezése
        self.stby.on()

        self.speed = 0.0

        # Biztonságos kezdőállapot
        self.stop()
        self.steer_center()

        print("RobotDrive inicializalva.")


    # ========================================================
    # KORMÁNYZÁS
    # ========================================================

    def steer_center(self):

        self.servo.angle = self.CENTER_ANGLE

        print(
            f"KORMANY: KOZEP "
            f"({self.CENTER_ANGLE} fok)"
        )


    def steer_left(self):

        self.servo.angle = self.LEFT_ANGLE

        print(
            f"KORMANY: BAL "
            f"({self.LEFT_ANGLE} fok)"
        )


    def steer_right(self):

        self.servo.angle = self.RIGHT_ANGLE

        print(
            f"KORMANY: JOBB "
            f"({self.RIGHT_ANGLE} fok)"
        )


    def set_steering_angle(self, angle):

        angle = max(
            self.LEFT_ANGLE,
            min(
                self.RIGHT_ANGLE,
                angle
            )
        )

        self.servo.angle = angle


    # ========================================================
    # MOTOR
    # ========================================================

    def forward(self, speed=0.40):

        speed = max(
            0.0,
            min(
                1.0,
                speed
            )
        )

        self.ain1.on()
        self.ain2.off()

        self.pwma.value = speed

        self.speed = speed


    def backward(self, speed=0.30):

        speed = max(
            0.0,
            min(
                1.0,
                speed
            )
        )

        self.ain1.off()
        self.ain2.on()

        self.pwma.value = speed

        self.speed = speed


    def stop(self):

        self.pwma.value = 0

        self.ain1.off()
        self.ain2.off()

        self.speed = 0


    # ========================================================
    # EGYSZERŰ PARANCSOK
    # ========================================================

    def straight(self, speed=0.40):

        self.steer_center()
        self.forward(speed)


    def left(self, speed=0.30):

        self.steer_left()
        self.forward(speed)


    def right(self, speed=0.30):

        self.steer_right()
        self.forward(speed)


    def command(self, command, speed=0.40):

        command = command.upper()

        if command == "LEFT":

            self.steer_left()
            self.forward(speed)

        elif command == "RIGHT":

            self.steer_right()
            self.forward(speed)

        elif command == "STRAIGHT":

            self.steer_center()
            self.forward(speed)

        elif command == "STOP":

            self.stop()

        elif command == "BACK":

            self.steer_center()
            self.backward(speed)

        else:

            print(
                "Ismeretlen parancs:",
                command
            )


    # ========================================================
    # LEÁLLÍTÁS
    # ========================================================

    def shutdown(self):

        print("Robot leallitasa...")

        self.stop()
        self.steer_center()

        time.sleep(0.2)

        self.stby.off()

        self.ain1.close()
        self.ain2.close()
        self.pwma.close()
        self.stby.close()


# ============================================================
# HARDVER TESZT
# ============================================================

if __name__ == "__main__":

    robot = RobotDrive()

    try:

        robot.steer_center()
        time.sleep(2)

        robot.steer_left()
        time.sleep(2)

        robot.steer_right()
        time.sleep(2)

        robot.steer_center()
        time.sleep(2)

        robot.forward(0.25)
        time.sleep(2)

        robot.stop()

    except KeyboardInterrupt:
        pass

    finally:
        robot.shutdown()