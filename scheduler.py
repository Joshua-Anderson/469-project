# The scheduler takes a list of requested passes as an input, resolves conflicts, and geneates
# a schedule for the ground stations

import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Generate a schedule for a ground station network')
    parser.add_argument("reservations", help="requested ground station reservations")
    parser.add_argument("schedule", help="generated ground station schedule")
    parser.add_argument('-g','--groundstations', help='<Required> List of ground stations in network', required=True)
    parser.add_argument('-l','--length', help='<Required> Schedule length in minutes', type=int, required=True)
    args = parser.parse_args()

    sim_len = args.length
    gs_list = [gs for gs in args.groundstations.split(',')]

    print("Starting sim with stations {} of length {} minutes".format(gs_list, sim_len))

    gs_sched = {}
    for gs in gs_list:
        gs_sched[gs] = []
        for t in range(sim_len):
            gs_sched[gs].append({"time": t, "res": []})

    with open(args.reservations) as f:
        data = json.load(f)

    load_reservations(gs_sched, data, sim_len)
    resolve_conflicts(gs_sched, sim_len)

    with open(args.schedule, 'w') as f:
        json.dump(gs_sched, f, indent=4)

def load_reservations(gs_sched, new_res, sim_len):
    # Add ground station reservations to schedule
    for res in new_res:
        mission = res["mission"]
        station = res["station"]
        if not station in gs_sched:
            continue
        station_sched = gs_sched[station]
        for time_range in res["time"]:
            # Add reservation for every minute reserved by file
            for t in range(time_range[0], time_range[1]):
                timeslice = station_sched[t]
                timeslice["res"].append(mission)
                timeslice["time"] = t

def resolve_conflicts(gs_sched, sim_len):
    for gs in gs_sched:
        for t in range(sim_len):
            timeslice = gs_sched[gs][t]

            # If there is no conflict, just schedule the ground station
            if len(timeslice["res"]) == 0:
                timeslice["sched"] = None
                continue
            if len(timeslice["res"]) == 1:
                timeslice["sched"] = timeslice["res"][0]
                continue

            timeslice["sched"] = "TODO"

if __name__ == "__main__":
    main()
