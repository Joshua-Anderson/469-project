#!/usr/bin/env python3

# The scheduler takes a list of requested passes as an input, resolves conflicts, and geneates
# a schedule for the ground stations

import argparse
import json
from random import randint

time_between_orbit_sides = 60*12 # twelve hours
time_between_passes = 60 # one hour
pass_length = 10

def main():
    parser = argparse.ArgumentParser(description='Generate a reservation list for a series of satellites')
    parser.add_argument("reservations", help="file to store requested ground station reservations")
    parser.add_argument('-m','--missions', help='List of missions and minute offset, comma seperated. Ex: CP7:0,CP12:90', required=True)
    parser.add_argument('-g','--groundstations', help='List of ground stations and minute offset, comma seperated. Ex: hertz:0,purdue:180', required=True)
    parser.add_argument('-l','--length', help='Total simulation length in minutes', type=int, required=True)
    args = parser.parse_args()

    sim_len = args.length

    missions = []
    print("Missions:")
    for m in args.missions.split(','):
        parts = m.split(':')
        print("\t {} - {}".format(parts[0], parts[1]))
        missions.append({"name": parts[0], "offset": int(parts[1])})

    groundstations = []
    print("Ground Stations:")
    for gs in args.groundstations.split(','):
        parts = gs.split(':')
        print("\t {} - {}".format(parts[0], parts[1]))
        groundstations.append({"name": parts[0], "offset": int(parts[1])})

    # Generate Polar-ish passes for each satellite.
    # To simplify the reservation generation, I'm assuming each mission is in a polar orbit
    # and has two passes in each side of the orbit
    # So a mission will have one 10 mintue pass, a one hour delay, another 10 minute pass, and repeat 12 hours later.
    # To make this more realistic, this program will inject some randomness into nearly every one of these numbers

    out = []
    for m in missions:
        for g in groundstations:
            t = m["offset"] + g["offset"]
            passes = []
            pass_num = 0
            while t < sim_len:
                pass_stop = t + pass_length + randint(0, pass_length/2)
                if pass_stop > sim_len:
                    passes.append([t, sim_len])
                    break
                passes.append([t, pass_stop])

                if pass_num % 2 == 0:
                    t += time_between_passes + randint(0, time_between_passes/10)
                else:
                    t += time_between_orbit_sides + randint(0, time_between_orbit_sides/12)

                pass_num += 1

            out.append({"mission": m["name"], "station": g["name"], "time": passes})

    with open(args.reservations, 'w') as f:
        json.dump(out, f, indent=4)







if __name__ == "__main__":
    main()
