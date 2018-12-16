# CPE 469 Research Project - Distributed CubeSat Ground Station Scheduling

The research project is investigating the impact of different scheduling algorithms on CubeSat ground station performance.

There are three python programs we used to create a workflow that simulated ground station scheduling:

  - `reservation_generation.py`: Generates random ground station reservations simulating a CubeSat in polar orbit.
  - `scheduler.py`: Takes the ground station reservations, uses a scheduling algorithm to resolve the conflicts, and writes a master schedule.
  - `analysis.py`: Performs statistical analysis on the generated schedule to evaluate algorithm effectiveness. Ex: Ground station time per mission, percent mission won in a conflict, and so on.

## Generating Ground Station Reservations

The `reservation_generation.py` file generates a json file that shows when each satellite would like to be scheduled at a given ground station, without respect to conflicts. This is approximated by two back to back passes, then a twelve hour delay to the next set of back to back passes.

Parameters:
  - Missions: Satellites to generate a schedule for, followed by the offset to their first pass. `CP7:50,CP12:90` includes two satellite in the reservations, one which is offset 50 minutes and one which is offset 90 minutes.
  - Ground Stations: The Ground Stations used to operate these missions and their offset from 0. `hertz:0,purdue:180` includes two stations, one of which is offset 180 minutes.
  - Length: Amount of time in minutes to run simulation for.

Example Run: `python3 reservation_generator.py -m CP7:50,CP12:90 -g hertz:0,purdue:180 -l 18000 reservation.json`

## Generating Satellite Schedules

The `scheduler.py` file generates a master schedule for all the satellites at each ground station taking into account conflicts. The master schedule is generated in the form of a json file. Each school will have its own master schedule.

Parameters:
    - Ground Stations: A list of ground stations that a given school has.
    - Length: How many minutes long to generate a schedule for.
    - Algorithm: The algorithm that is going to be used to resolve conflicts.
    - Priority List: (optional) The priority list of satellites, required for some algorithms.
    - Reservations: The reservation file to be used to make a schedule.
    - Schedules: The resulting json file that contains the master schedule.

Example Run: `python3 scheduler.py -g hertz -l 30 -a plist -pl CP7,CP12 testreservations.json schedules.json`


## Generating Analysis Graphs

The `analysis.py` file is used to create an html file that has a graph containing statistics on how much each satellite is used at a given ground station and how conflicts are settled.

Parameters:
    - Schedule: The json file that contains the master schedule generated from scheduler.py
    - Chart: The name of the chart file that will be generated.

Example Run: `python3 analysis.py scheduler.json chart.html`
