import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='Analyze Ground Station Schedule')
    parser.add_argument("schedule", help="Ground Station Schedule ")
    args = parser.parse_args()

    # Ground Station Utilization Time
    # Ground Station Conflict Time
    # Mission Requested Time
    # Mission Scheduled Time
    # Mission Time in Conflict
    # Mission Percent Time Won Conflict

    with open(args.schedule) as f:
        data = json.load(f)

    gs_stats = {}
    mission_stats = {}

    for gs, schedule in data.items():
        gs_stats[gs] = {"sim_len": len(schedule), "utilized": 0, "conflict": 0}
        for ts in schedule:
            calc_gs_stats(gs_stats, gs, ts)
            calc_mission_stats(mission_stats, ts)

    print("Groundstation Analysis:")
    for gs, results in gs_stats.items():
        print("\t{}:".format(gs))

        sim_len = results["sim_len"]
        conflict = results["conflict"]
        utilized = results["utilized"]
        print("\t\tUtilized {}% ({}/{})"
            .format(percent(utilized, sim_len), utilized, sim_len))
        print("\t\tConflict {}% ({}/{})"
            .format(percent(conflict, sim_len), conflict, sim_len))

    print("Mission Analysis:")
    for mission, results in mission_stats.items():
        print("\t{}:".format(mission))

        requested = results["requested"]
        conflict = results["conflict"]
        scheduled = results["scheduled"]
        print("\t\tScheduled {}% ({}/{})"
            .format(percent(scheduled, requested), scheduled, requested))
        print("\t\tConflict {}% ({}/{})"
            .format(percent(conflict, requested), conflict, requested))

        lost_conflict = requested - scheduled
        won_conflict = conflict - lost_conflict
        print("\t\tWon Conflict {}% ({}/{})"
            .format(percent(won_conflict, conflict), won_conflict, conflict))

def calc_gs_stats(gs_stats,gs, ts):
    if len(ts["res"]) > 1:
        gs_stats[gs]["conflict"] += 1
    if ts["sched"] is not None:
        gs_stats[gs]["utilized"] += 1

def calc_mission_stats(mission_stats, ts):
    conflict = len(ts["res"]) > 1
    for mission in ts["res"]:
        if not mission in mission_stats:
            mission_stats[mission] = {"requested": 0, "scheduled": 0, "conflict": 0}
        mission_stats[mission]["requested"] += 1
        if conflict:
            mission_stats[mission]["conflict"] += 1
    if ts["sched"] is not None:
        mission_stats[ts["sched"]]["scheduled"] += 1




def percent(a, b):
    return round((float(a)/float(b)) * 100)

if __name__ == "__main__":
    main()
