# CPE 469 Research Project - Distributed CubeSat Ground Station Scheduling

The research project is investigating the impact of different scheduling algorithms on CubeSat ground station performance.

There are three python programs we used to create a workflow that simulated ground station scheduling:

  - `reservation_generation.py`: Generates random ground station reservations simulating a CubeSat in polar orbit.
  - `scheduler.py`: Takes the ground station reservations, uses a scheduling algorithm to resolve the conflicts, and writes a master schedule.
  - `analysis.py`: Performs statistical analysis on the generated schedule to evaluate algorithm effectiveness. Ex: Ground station time per mission, percent mission won in a conflict, and so on.

## Generating Ground Station Reservations

The `reservation_generation.py` supports generating a ground station schedule for CubeSats in Polar orbit. This is approximated by two back to back passes, then a twelve hour delay to the next set of back to back passes.

Parameters:
  - Missions: Satellites to generate a schedule for, followed by the offset to their first pass. `CP7:50,CP12:90` includes two satellite in the reservations, one which is offset 50 minutes and one which is offset 90 minutes.
  - Ground Stations: The Ground Stations used to operate these missions and their offset from 0. `hertz:0,purdue:180` includes two stations, one of which is offset 180 minutes.
  - Length: Amount of time in minutes to run simlation for.

Example Run: `python3 reservation_generator.py -m CP7:50,CP12:90 -g hertz:0,purdue:180 -l 18000`
