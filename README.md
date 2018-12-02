# CPE 469 Research Project - Distributed CubeSat Ground Station Scheduling

The research project is investigating the impact of different scheduling algorithms on CubeSat ground station performance.

There are three python programs we used to create a workflow that simulated ground station scheduling:

  - `reservation_generation.py`: Generates random ground station reservations simulating a CubeSat in polar orbit.
  - `scheduler.py`: Takes the ground station reservations, uses a scheduling algorithm to resolve the conflicts, and writes a master schedule.
  - `analysis.py`: Performs statistical analysis on the generated schedule to evaluate algorithm effectiveness. Ex: Ground station time per mission, percent mission won in a conflict, and so on.
