# WRO Future Engineers 2026 – VTS Team

Autonomous vehicle developed by the VTS team for the **World Robot Olympiad (WRO) Future Engineers 2026** category.

The vehicle is designed as a compact rear-wheel-drive, front-wheel-steered autonomous car. Its main controller is a **Raspberry Pi 4 Model B (8 GB)**, while visual perception is provided by a **Raspberry Pi Camera Module 3 Wide**. The control software is written in **Python**, with **OpenCV** used for real-time image processing and track perception.

---

## Table of Contents

1. [Team Information](#1-team-information)
2. [Project Overview](#2-project-overview)
3. [Design Goals](#3-design-goals)
4. [Mechanical Design](#4-mechanical-design)
5. [Drive and Steering System](#5-drive-and-steering-system)
6. [Electronics and Hardware](#6-electronics-and-hardware)
7. [Power System](#7-power-system)
8. [Vision System](#8-vision-system)
9. [Software Architecture](#9-software-architecture)
10. [Open Challenge Strategy](#10-open-challenge-strategy)
11. [Obstacle Challenge Strategy](#11-obstacle-challenge-strategy)
12. [Testing and Development](#12-testing-and-development)
13. [Repository Structure](#13-repository-structure)
14. [Vehicle Photos](#14-vehicle-photos)
15. [Schematics and Mechanical Files](#15-schematics-and-mechanical-files)
16. [Videos](#16-videos)
17. [Future Improvements](#17-future-improvements)

---

## 1. Team Information
![VTS csapatkép](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/t-photos/Szemf%C3%A9nyveszt%C5%91k%20Team%20Picture.jpg)
**Institution:** VTS / Subotica Tech – College of Applied Sciences  
**Competition:** WRO Future Engineers 2026

### Team members

- **Berec Edvárd**
- **Dukai Botond**
- **Kaszás Krisztián**

### Team captain / mentor

- **Pletikoszity Árpád**

We are a motivated and goal-oriented team with a strong interest in robotics, autonomous systems, programming, and practical engineering. Our aim is not only to build a vehicle capable of completing the WRO Future Engineers challenges, but also to understand the interaction between mechanical design, electronics, computer vision, and autonomous control.

---

## 2. Project Overview
Our project is a fully autonomous four-wheeled vehicle developed for the WRO Future Engineers competition.

The design follows a conventional automotive layout:

- rear-wheel drive,
- front-wheel steering,
- a single geared DC motor for propulsion,
- a servo motor for steering,
- camera-based environmental perception,
- Raspberry Pi-based high-level control.

The vehicle uses a **Raspberry Pi 4 Model B with 8 GB RAM** as its main processing unit. A **Raspberry Pi Camera Module 3 Wide** provides a wide field of view for detecting the track, boundaries, coloured traffic signs, and other relevant visual features.

The complete control software is being developed in **Python**, while **OpenCV** is used for image acquisition and image-processing tasks.

![Concept visualization of the autonomous vehicle](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/v-photos/Visualization1.jpg)

*Concept visualization; the physical build may differ.*

---

## 3. Design Goals

The main design goals are:

- reliable autonomous driving on the official WRO Future Engineers field;
- simple and robust mechanical construction;
- precise front-wheel steering;
- stable low-speed propulsion;
- wide-angle visual perception;
- modular electronics that can be tested independently;
- software that can be modified and calibrated quickly during development;
- easy access to all major components for maintenance and debugging.

A major design principle is to keep the drivetrain and steering mechanically simple while assigning perception and decision-making tasks to the Raspberry Pi.

---

## 4. Mechanical Design

The main chassis is manufactured from **2 mm steel sheet**.

Steel was selected to provide:

- high mechanical rigidity;
- stable mounting of the motor, steering system, Raspberry Pi, and camera;
- resistance to deformation during repeated testing;
- a low and mechanically stable base for the vehicle.

The robot uses **LEGO wheels** and LEGO-compatible axles in the drivetrain. This approach allows rapid modification of the wheel and transmission system while retaining a rigid metal chassis for the main structure.

### Vehicle configuration

- **Chassis material:** 2 mm steel sheet
- **Drive:** rear-wheel drive
- **Steering:** front-wheel steering
- **Wheels:** LEGO wheels
- **Wheel diameter:** 56 mm
- **Rear axle connection:** LEGO-compatible axle system

> **TODO:** Add final vehicle dimensions and total mass after assembly.

Concept views of the proposed vehicle:

![Concept visualization, side view](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/v-photos/Visualization2.jpg)

![Concept visualization, opposite side view](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/v-photos/Visualization3.jpg)

*These are concept visualizations, not photographs of the completed robot.*

---

## 5. Drive and Steering System

### 5.1 Propulsion

Propulsion is provided by a **GA12-N20 geared DC motor**.

Current drivetrain parameters:

- motor output speed: **60 rpm**;
- additional transmission ratio: **1:3 reduction**;
- calculated rear-wheel speed: approximately **20 rpm**;
- wheel diameter: **56 mm**.

The motor drives the rear wheels through a LEGO-compatible axle transmission.

With a 56 mm wheel diameter and an approximate wheel speed of 20 rpm, the theoretical linear vehicle speed is approximately:

**0.059 m/s (0.21 km/h)**

before considering mechanical losses and wheel slip.

The additional reduction was selected to increase available wheel torque and to provide smooth, controllable low-speed movement during the early development phase.

> **TODO:** After track testing, confirm whether the 1:3 reduction remains in the final competition configuration.

### 5.2 Motor Driver

The DC motor is controlled using a **TB6612 dual motor driver**.

The driver enables:

- bidirectional DC motor control;
- PWM-based speed control;
- direct control from Raspberry Pi GPIO logic;
- compact integration into the vehicle electronics.

Only one propulsion motor is currently required, leaving the second driver channel available if the drivetrain is modified later.

### 5.3 Steering

Front-wheel steering is actuated by an **MG996R servo motor**.

The servo is controlled by a dedicated **PCA9685 PWM servo controller** rather than by software-generated PWM directly from the Raspberry Pi.

This solution was chosen to provide:

- stable servo pulses;
- repeatable steering angles;
- reduced timing load on the Raspberry Pi;
- convenient software calibration of steering endpoints and centre position.

The front wheels are mechanically linked to the servo and rotate together to steer the vehicle.

> **TODO:** Add the final steering angle range and mechanical steering geometry after calibration.

---

## 6. Electronics and Hardware

### 6.1 Main Controller – Raspberry Pi 4 Model B 8 GB

The main controller is a **Raspberry Pi 4 Model B with 8 GB RAM**.

It was selected because it provides sufficient processing capability for:

- real-time camera acquisition;
- OpenCV-based image processing;
- autonomous decision logic;
- GPIO motor control;
- I²C communication with the PCA9685;
- development and debugging directly in Python.

The Raspberry Pi serves as the central unit connecting perception, decision-making, steering, and propulsion.

### 6.2 Raspberry Pi Camera Module 3 Wide

The vehicle uses a **Raspberry Pi Camera Module 3 Wide**.

The wide-angle version was selected because the robot needs to observe:

- track boundaries;
- upcoming corners;
- red and green traffic signs;
- objects located to the left and right of the vehicle's centreline.

### 6.3 PCA9685 Servo Controller

The **PCA9685** provides hardware PWM signals for the steering servo.

Main function in the robot:

`Raspberry Pi → I²C → PCA9685 → MG996R servo`

This keeps steering pulse generation independent of Linux timing variation on the Raspberry Pi.

### 6.4 MG996R Servo Motor

The **MG996R** is used as the front steering actuator.

Its main role is to:

- turn the front wheels;
- maintain a calibrated centre position;
- execute steering corrections calculated by the navigation software.

### 6.5 TB6612 Dual Motor Driver

The **TB6612** is used as the interface between the Raspberry Pi and the GA12-N20 drive motor.

Main signal path:

`Raspberry Pi → TB6612 → GA12-N20 → rear axle → rear wheels`

### 6.6 GA12-N20 Geared DC Motor

The **GA12-N20** motor provides vehicle propulsion.

Current specification used in the project:

- rated operating configuration: 6 V class;
- gearbox output speed: 60 rpm;
- additional mechanical reduction: 1:3.

---

## 7. Power System

The vehicle is powered by a **10,000 mAh power bank**.

### Power bank output

- **Voltage:** 5 V
- **Maximum output current:** 3 A
- **Capacity:** 10,000 mAh

The power bank was selected because it is:

- rechargeable;
- compact;
- easily replaceable;
- safe and convenient during repeated development sessions;
- suitable for powering Raspberry Pi-based systems.

### Power distribution

The planned power architecture includes:

- Raspberry Pi 4 powered from the 5 V supply;
- servo power distributed separately from the Raspberry Pi logic where required;
- common electrical ground between the Raspberry Pi, PCA9685, TB6612, and actuator power circuits.

> **Important:** The final power architecture must be verified under maximum servo and motor load. The MG996R can create large transient current demands, and the 5 V / 3 A source must be tested for voltage drop and Raspberry Pi undervoltage.

> **TODO:** Add the final DC-DC converter / separate servo supply arrangement if one is used in the competition version.

---

## 8. Vision System

### 8.1 Camera Position

The Raspberry Pi Camera Module 3 Wide is mounted approximately **150–200 mm above the chassis** and tilted approximately **30° forward**.

This position was selected to provide a wide view of the track and wall boundaries, the coloured direction lines, approaching red and green obstacles, and the area immediately in front of the vehicle.

### 8.2 OpenCV Processing

Image processing is performed in **Python using OpenCV**.

The vision system detects four main types of visual information:

- dark/black track boundaries and walls;
- orange direction line;
- blue direction line;
- red and green obstacles.

The processing pipeline is:

1. capture a frame from the Camera Module 3 Wide;
2. crop or resize the image if required;
3. convert the frame to the colour space required by the detector;
4. create colour masks;
5. apply filtering and morphological operations;
6. detect contours;
7. calculate contour area and the lowest image coordinate (`bottom_y`);
8. pass the resulting detections to the navigation module.

For red and green objects, the closest relevant obstacle is selected primarily from the object that extends lowest in the image. Contour area is used as an additional criterion.

---

## 9. Software Architecture

The software is written in **Python** and divided into separate modules for perception, decision-making, and actuator control.

![Concept diagram of the autonomous navigation process](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/other/Autonomous%20Navigation%20Process%20BD.jpg)

*Development concept; component labels and control logic will be checked against the final build.*

The current main files are:

```text
src/
├── robot_main.py
├── vision.py
├── navigation.py
├── drive_control.py
├── color_detection.py
├── turn_direction.py
└── wall_follow.py
```

### `robot_main.py`

Main application file. It initializes the camera and control modules, starts the vehicle, captures camera frames, requests detections from `vision.py`, passes perception data to `navigation.py`, and sends steering and propulsion commands through `drive_control.py`.

### `vision.py`

Responsible for the main OpenCV processing tasks:

- wall/track detection;
- orange line detection;
- blue line detection;
- red obstacle detection;
- green obstacle detection;
- contour filtering;
- object position and `bottom_y` calculation.

### `navigation.py`

Contains the autonomous decision logic.

The current navigation states are:

```text
SEARCH_DIRECTION
NORMAL_DRIVING
AVOID_OBSTACLE
RETURN_TO_PATH
```

The module determines the driving direction, normal track-following behaviour, when an obstacle is sufficiently close, the required passing side, when obstacle avoidance is complete, and when the robot should return to its normal trajectory.

### `drive_control.py`

Controls the vehicle actuators:

- PCA9685 → MG996R steering servo;
- TB6612 → GA12-N20 propulsion motor.

### Test and development scripts

- `color_detection.py` – colour-recognition development and verification;
- `turn_direction.py` – orange/blue direction-decision testing;
- `wall_follow.py` – basic track/wall-following testing.

---

## 10. Open Challenge Strategy

The robot is designed to **start moving forward immediately**. It does not wait at the starting position to determine the direction of travel.

While moving, the camera continuously searches for the coloured direction lines. The robot makes the clockwise/counter-clockwise decision only when a detected line becomes sufficiently close in the image.

The current decision threshold is:

```text
DECISION_Y = 430
```

A direction line is considered close enough for a reliable decision when:

```text
bottom_y > 430
```

The direction logic is:

- **orange line detected first/closer → clockwise (CW);**
- **blue line detected first/closer → counter-clockwise (CCW).**

Once the direction is determined, it is stored and remains locked for the run.

After direction selection, the robot continues in `NORMAL_DRIVING` mode. The camera and wall/track detection are used continuously to decide when steering correction is required.

The robot does not follow a memorized fixed route. Decisions are made from visual information detected during the run.

### Open Challenge control sequence

```text
START
  ↓
Move forward
  ↓
Search for orange / blue line
  ↓
Is a line close enough? (bottom_y > 430)
  ├── No → continue forward and observe
  └── Yes
       ↓
Orange → CW
Blue   → CCW
       ↓
Lock direction
       ↓
NORMAL_DRIVING
       ↓
Continuous wall/track detection and steering correction
```

---

## 11. Obstacle Challenge Strategy

The Obstacle Challenge uses the same basic movement and direction-detection logic as the Open Challenge, with additional red/green obstacle recognition.

The robot continuously detects both red and green objects while driving.

The implemented passing rule is:

```python
PASS_SIDE = {
    "RED": "RIGHT",
    "GREEN": "LEFT"
}
```

Therefore:

- a **red obstacle is passed on the right**;
- a **green obstacle is passed on the left**.

### 11.1 Selecting the Relevant Obstacle

If several coloured objects are visible, the robot selects the closest obstacle using image geometry. The current selection prioritizes:

1. greatest `bottom_y`;
2. contour area.

In simplified form:

```text
closest obstacle = max(bottom_y, area)
```

### 11.2 Obstacle Distance Decision

An obstacle becomes active for avoidance when:

```text
bottom_y > 400
```

At that point, the navigation state changes from:

```text
NORMAL_DRIVING
```

to:

```text
AVOID_OBSTACLE
```

The obstacle colour determines the passing side.

After the robot has passed the object, the system waits until the obstacle is no longer detected for **8 consecutive frames** before considering the manoeuvre complete.

The navigation then enters:

```text
RETURN_TO_PATH
```

and finally returns to:

```text
NORMAL_DRIVING
```

### Obstacle Challenge control sequence

```text
NORMAL_DRIVING
      ↓
Detect red / green objects
      ↓
Select closest object
(max bottom_y, then area)
      ↓
Is bottom_y > 400?
      ├── No → continue normal driving
      └── Yes
             ↓
       AVOID_OBSTACLE
             ↓
   Red   → pass RIGHT
   Green → pass LEFT
             ↓
Obstacle absent for 8 frames
             ↓
       RETURN_TO_PATH
             ↓
       NORMAL_DRIVING
```

The robot does **not** perform the parking task. The current development is focused on reliable autonomous driving, direction recognition, and red/green obstacle avoidance.

---

## 12. Testing and Development

Development is performed incrementally so that perception, steering, and propulsion can be validated independently.

![Motor and driver components during development](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/v-photos/in%20the%20details%20of%20the%20process.jpg)

The current test sequence is:

1. Raspberry Pi and power-system verification;
2. PCA9685 communication test;
3. MG996R steering centre and endpoint calibration;
4. TB6612 motor-driver test;
5. GA12-N20 drivetrain test;
6. low-speed straight-line driving;
7. Camera Module 3 Wide acquisition test;
8. orange/blue line detection;
9. clockwise/counter-clockwise decision test;
10. wall/track-following test;
11. red/green obstacle detection;
12. closest-obstacle selection test;
13. obstacle passing on the required side;
14. return-to-path test;
15. integrated full-field testing.

### Current software thresholds

| Parameter | Current value | Function |
|---|---:|---|
| Direction decision threshold | `DECISION_Y = 430` | Orange/blue line must be sufficiently close |
| Obstacle activation threshold | `bottom_y > 400` | Starts obstacle avoidance |
| Obstacle clear confirmation | 8 frames | Confirms that the obstacle has been passed |

These values are calibration parameters and may be adjusted during field testing if the final camera mounting position changes.

### Development log

| Date | Test / Problem | Modification | Result |
|---|---|---|---|
| TODO | Steering calibration | TODO | TODO |
| TODO | Direction-line detection | TODO | TODO |
| TODO | Wall following | TODO | TODO |
| TODO | Red/green detection | TODO | TODO |
| TODO | Obstacle avoidance | TODO | TODO |

---

## 13. Repository Structure

The repository is organized so that source code, engineering documentation, images, and videos can be accessed separately.

```text
/
├── README.md
├── src/
│   ├── robot_main.py
│   ├── vision.py
│   ├── navigation.py
│   ├── drive_control.py
│   ├── color_detection.py
│   ├── turn_direction.py
│   └── wall_follow.py
├── schemes/
│   ├── wiring diagram
│   └── electronics documentation
├── models/
│   ├── chassis drawings
│   ├── mechanical parts
│   └── camera mount files
├── v-photos/
│   ├── front
│   ├── rear
│   ├── left
│   ├── right
│   ├── top
│   └── bottom
├── t-photos/
│   └── team photos
├── video/
│   ├── open-challenge.md
│   └── obstacle-challenge.md
└── other/
    └── additional documentation
```

The source-code structure reflects the actual development workflow: perception is implemented in `vision.py`, decision-making in `navigation.py`, actuator control in `drive_control.py`, and the complete system is integrated by `robot_main.py`.


## 14. Vehicle Photos

The final repository will contain clear photographs of the completed vehicle from the required directions:

- front;
- rear;
- left;
- right;
- top;
- bottom.

Additional images will document:

- drivetrain;
- steering mechanism;
- electronics layout;
- camera mounting;
- chassis construction.

Prototype during assembly:

![Robot prototype during assembly](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/v-photos/Robot.jpg)

> **TODO:** Insert final photos after the vehicle is assembled.

---

## 15. Schematics and Mechanical Files

The `schemes` folder will contain the electrical documentation of the robot.

The final wiring diagram should show at minimum:

- Raspberry Pi 4;
- Camera Module 3 Wide;
- PCA9685;
- MG996R;
- TB6612;
- GA12-N20 motor;
- power bank;
- power and ground connections.

The mechanical documentation will include available drawings of:

- steel chassis;
- motor mount;
- steering mechanism;
- axle/transmission arrangement;
- camera mount.

Preliminary electronics diagram (to be revised to match the final camera and power configuration):

![Preliminary electronics diagram](https://raw.githubusercontent.com/botson17/WRO-2026-Future-Engineers/main/other/Electronic.jpg)

> **TODO:** Upload wiring diagram and final mechanical drawings.

---

## 16. Videos

The `video` folder will contain links to demonstration videos.

### Open Challenge

`TODO: Insert video link`

### Obstacle Challenge

`TODO: Insert video link`

The videos will demonstrate autonomous vehicle operation without external control.

---

## 17. Future Improvements

The current vehicle is being developed as a practical, modular autonomous platform.

Possible future improvements include:

- optimization of drivetrain ratio after full-field testing;
- improved steering geometry;
- closed-loop vehicle-speed feedback;
- additional distance sensing if required;
- improved camera mount;
- automatic camera exposure/colour calibration;
- more robust traffic-sign detection;
- state-machine-based challenge control;
- optimized power distribution;
- mechanical weight reduction.

---

## Current Hardware Summary

| Component | Selected solution |
|---|---|
| Main controller | Raspberry Pi 4 Model B, 8 GB |
| Camera | Raspberry Pi Camera Module 3 Wide |
| Programming language | Python |
| Image processing | OpenCV |
| Power source | 10,000 mAh power bank |
| Power output | 5 V / 3 A |
| Steering controller | PCA9685 |
| Steering actuator | MG996R servo |
| Drive motor controller | TB6612 dual motor driver |
| Drive motor | GA12-N20 geared DC motor |
| Motor output speed | 60 rpm |
| Final reduction | 1:3 |
| Approx. wheel speed | 20 rpm |
| Wheel diameter | 56 mm |
| Wheels | LEGO |
| Drivetrain | Rear-wheel drive |
| Steering | Front-wheel steering |
| Chassis | 2 mm steel sheet |
| Camera height | Approx. 150–200 mm |
| Camera angle | Approx. 30° forward |

---

## Status

**Development in progress.**

The README will be updated continuously as the vehicle, software, wiring, and competition strategy are finalized.
