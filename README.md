# WRO 2026 Future Engineers — Self-Driving Car

Engineering repository for our entry in the WRO 2026 Future Engineers category. This repository records the vehicle we build, the reasons for our choices, the source code, and the results of testing. **Current status: early design and documentation setup.** The design ideas below are not claims that a finished vehicle has been built or tested.

## Challenge

The vehicle must drive autonomously in two challenges. In the Open Challenge it completes three laps with changing inner wall positions. In the Obstacle Challenge it follows the required side of red and green traffic signs, completes three laps, and performs parallel parking. We will document the implemented behavior and measured results as the project develops.

## Current vehicle concept

| Subsystem | Current plan | Status |
| --- | --- | --- |
| Chassis | Custom, flat 3D-printed plate; the chassis itself is not made from LEGO | Planned |
| Drive | LEGO-based mechanical drive | Planned; motor, axle and gearing not finalized |
| Steering | Front-wheel steering driven through LEGO gears | Planned; geometry and actuator not finalized |
| Perception | Two color sensors and one camera | Planned; mounting and roles not finalized |
| Additional sensing | A further sensor may be added after testing | Undecided |
| Controller and power | Selection, wiring and battery budget | Undecided |
| Software | Autonomous navigation for both challenges | Not uploaded yet |

The initial steering concept uses gears at the front to turn the wheels. We need to measure steering angle, backlash, wheel clearance and repeatability before fixing the printed chassis geometry. The chassis should allow the team to replace or reposition sensor mounts and adjust the steering mechanism during development. The team will add drawings, photos and actual measurements to [mechanical design](docs/mechanical-design.md).

The two color sensors and camera are a proposal, not an established sensor fusion system. We still need to decide which observations each device provides, measure performance on the competition field, and document calibration and failure cases. See [power and sensors](docs/power-and-sensors.md).

## Rule constraints to verify during construction

The 2026 international rules limit the vehicle to **300 × 200 mm footprint, 300 mm height and 1.5 kg**. It must have four wheels, one driving axle and one steering actuator; differential steering with independent motors on the sides is not allowed. The driven wheels must be mechanically connected. Sensors and cameras are permitted, but wireless communication must be disabled during competition rounds. The vehicle must start using the specified power switch and separate start button procedure. We will check the finished build against the full rules and official Q&A, including any event-specific updates.

## Repository map

- [Engineering journal](docs/engineering-journal.md): dated decisions, alternatives, setbacks and iterations.
- [Mechanical design](docs/mechanical-design.md): chassis, dimensions, steering, drivetrain, CAD and assembly.
- [Power and sensors](docs/power-and-sensors.md): controller, battery, wiring, camera and sensor calibration.
- [Software and strategy](docs/software-and-strategy.md): module map, algorithms, obstacle handling, deployment.
- [Testing](docs/testing.md): repeatable test procedures and measured outcomes.
- [Evidence](media/README.md): vehicle photographs and links to autonomous driving videos.
- `hardware/`: add original CAD, printable files and wiring diagrams when available.
- `software/`: add the team's original source code and setup instructions when available.

## Reproducing the vehicle

This section is **pending the actual build**. The team will provide a component list with exact models, CAD and print settings, assembly instructions, wiring diagram, controller and firmware versions, software dependencies, build/upload commands, calibration procedure and a reproducible track test. We will not publish guessed commands or unverified circuit details.

## Engineering process

Each important design decision belongs in the journal with its date, problem, alternatives, selected approach and evidence. Test entries should name the hardware/software revision, track setup, trials, measured result and the change planned next. Commit messages should describe actual work. We will include setbacks as well as successful runs so another team can understand how the vehicle evolved.

## Documentation still needed

- Final photos: front, rear, both sides, top and bottom, plus a team photo.
- One YouTube driving demonstration for each challenge, with at least 30 seconds of autonomous driving in each.
- Original vehicle source code, complete CAD, parts list, wiring diagram and calibration values.
- A detailed English README of at least 5,000 characters describing the **finished** system and how to build and upload its code. This starter README does not yet satisfy that final documentation requirement.
- Hard copy for the international event and confirmation of the organizer's submission deadline.

The 2026 rules also specify a dated commit history and public availability after submission. See section 7 and Appendix C of the official document for the exact requirements; a newly initialized repository cannot substitute for earlier work or backdate development.

## Official sources

- [WRO 2026 Future Engineers rules](https://wro-association.org/wp-content/uploads/WRO-2026-Future-Engineers-Self-Driving-Cars-General-Rules.pdf)
- [WRO 2026 documentation rubric](https://wro-association.org/wp-content/uploads/WRO-2026-Future-Engineers-Documentation-Rubric.pdf)
- [WRO 2026 season and Q&A links](https://wro-association.org/competition/2026-season/)
- [WRO 2026 Open Championship Europe](https://wro2026croatia.eu/competition/)

The team remains responsible for its original construction, programming, measurements and engineering explanations.
