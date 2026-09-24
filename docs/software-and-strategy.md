# Software architecture and driving strategy

**Status:** The team has not uploaded a program yet. The questions below define what the final documentation must explain; they do not describe implemented algorithms.

## Source and setup

When code is available, add the exact controller/firmware, programming language, toolchain versions, dependencies, build command, upload procedure and start procedure. Link every source module to the motor, steering or sensor hardware it controls. Put the team's original code under `software/` and document its entry point here.

## Control flow to document

- Waiting for the required start button, selecting direction and beginning autonomous motion.
- Reading and validating color sensors and camera frames.
- Estimating position relative to walls, lane and traffic signs.
- Steering and speed control, including tuning method and limits.
- Open Challenge lap counting and changing inner wall positions.
- Obstacle Challenge interpretation of red/green signs and side selection.
- Parking-space detection and parallel parking after the required laps.
- Handling unexpected readings, loss of track, timeout or mechanical faults.

Add a flowchart of the **implemented** state transitions, parameter table with units, and explanations of any PID, computer vision or sensor fusion methods the team actually uses. Explain the tests and metrics used for tuning rather than listing algorithm names without evidence.
