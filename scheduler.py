# The scheduler takes a list of requested passes as an input, resolves conflicts, and geneates
# a schedule for the ground stations

import argparse
import json
import random


def main():
    parser = argparse.ArgumentParser(description='Generate a schedule for a ground station network')
    parser.add_argument("reservations", help="requested ground station reservations")
    parser.add_argument("schedule", help="generated ground station schedule")
    parser.add_argument('-g','--groundstations', help='<Required> List of ground stations in network', required=True)
    parser.add_argument('-l','--length', help='<Required> Schedule length in minutes', type=int, required=True)
    parser.add_argument('-a', '--algorithm', help='<Required> Choose the algorithm you would like:\nFor Priority List: plist \nFor Lottery: lottery \nFor Token Algorithm: token \nFor Past 24 hrs Algorithm: past24', required=True)
    parser.add_argument('-pl', '--prioritylist', help="the priority list of the satalites")
    args = parser.parse_args()

    sim_len = args.length
    gs_list = [gs for gs in args.groundstations.split(',')]

    gs_sched = {}
    for gs in gs_list:
        gs_sched[gs] = []
        for t in range(sim_len):
            gs_sched[gs].append({"time": t, "res": []})

    with open(args.reservations) as f:
        data = json.load(f)

    load_reservations(gs_sched, data, sim_len)
    choose_algorithm(args, gs_sched, sim_len)

    print("Starting sim with stations {} of length {} minutes".format(gs_list, sim_len))

    with open(args.schedule, 'w') as f:
        json.dump(gs_sched, f, indent=4)


def choose_algorithm(args, gs_sched, sim_len):

    if(args.algorithm == "plist"):
        if(args.prioritylist == None):
            raise Exception("No priority list specified, Enter a priority list: -pl sat1, sat2, sat3...")
        else:
            resolve_conflicts(gs_sched, sim_len, priority_alg, args.prioritylist.split(','))

    elif(args.algorithm == "lottery"):
        resolve_conflicts(gs_sched, sim_len, lottery_alg)

    elif(args.algorithm == "token"):
        if(args.prioritylist == None):
            raise Exception("No priority list specified, Enter a priority list: -pl sat1, sat2, sat3...")
        else:
            resolve_conflicts(gs_sched, sim_len, token_alg, args.prioritylist.split(','))

    elif(args.algorithm == "past24"):
        resolve_conflicts(gs_sched, sim_len, past_24_alg)

    else:
        raise Exception("Unknown Algorithm {}".format(args.algorithm))



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

def resolve_conflicts(gs_sched, sim_len, alg, pl_list=None):
    in_conflict_block = False
    token_map = get_token_map(pl_list)
    for gs in gs_sched:
        for t in range(sim_len):
            timeslice = gs_sched[gs][t]

            # If there is no conflict, just schedule the ground station
            if len(timeslice["res"]) == 0:
                timeslice["sched"] = None
                in_conflict_block = False
            elif len(timeslice["res"]) == 1:
                timeslice["sched"] = timeslice["res"][0]
                in_conflict_block = False
            else:
                if(in_conflict_block == False):
                    timeslice["sched"] = alg(timeslice["res"], pl_list, token_map, gs_sched[gs], t)
                else:
                    timeslice["sched"] = gs_sched[gs][t - 1]["sched"]
                in_conflict_block = True


def priority_alg(sats, pl_list, token_map, gs_sched, t):

    min = pl_list.index(sats[0])
    res = sats[0]

    for sat in sats:
        priority = pl_list.index(sat)
        if(priority < min):
            min = priority
            res = sat

    return res


def lottery_alg(sats, pl_list, token_map, gs_sched, t):

    return random.choice(sats)


def get_token_map(pl_list):

    token_map = {}

    if(pl_list == None):
        return None
    else:
        pl_list.reverse()
        for i in range(len(pl_list)):
            token_map[pl_list[i]] = i
        return token_map


def token_alg(sats, pl_list, token_map, gs_sched, t):

    max_token = -1
    res = ""

    # find sat with max token and decrement its token
    for sat in sats:
        if(token_map[sat] > max_token):
            res = sat
            max_token = token_map[sat]

    if(max_token > 0):
        token_map[res] -= 1

    # increase all other sats tokens
    for sat in token_map:
        if(sat != res):
            token_map[sat] += 1

    return res


def past_24_alg(sats, pl_list, token_map, gs_sched, t):

    sat_usage = {}
    min_sat = None
    limit = min(t, 1440)

    # initalize map
    for sat in sats:
        sat_usage[sat] = 0

    # find sat usage from past 24 hours
    for i in range(1, limit):
        last_sat = gs_sched[t - i]["sched"]
        if(last_sat in sat_usage):
            sat_usage[gs_sched[t - i]["sched"]] += 1

    # return min sat usage
    min_sat = min(sat_usage.items(), key=lambda x: x[1])

    return min_sat[0]



if __name__ == "__main__":
    main()
