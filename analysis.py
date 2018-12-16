#!/usr/bin/env python3

import json
import argparse
import plotly
import plotly.figure_factory as ff
import datetime


def main():
    parser = argparse.ArgumentParser(description='Analyze Ground Station Schedule')
    parser.add_argument("schedule", help="Ground Station Schedule")
    parser.add_argument("chart", help="Chart of the final Ground Station Schedule")
    args = parser.parse_args()

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

    chart_utilization(data, args.chart)

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

def merge_time_slice(datapoints, prev, start, finish, task, resource):
    # If the new time slice is a continuation of the previous one, add on to the previous one.
    if prev is not None and \
       prev["Resource"] == resource and \
       prev["Finish"] == start:
        prev["Finish"] = finish
        return prev

    # Otherwise, add the old point to the list and start a new datapoint
    if prev is not None:
        datapoints.append(prev)

    point = {}
    point["Start"] = start
    point["Finish"] = finish
    point["Resource"] = resource
    point["Task"] = task
    return point



# Create a gantt chart of ground station utilization
def chart_utilization(data, filename):
    chart_data = []
    sim_start = datetime.datetime(2000, 1, 1, 0, 0)

    for gs, schedule in data.items():
        last_point = None
        last_c_point = None
        last_m_points = {}

        # Add time slice to chart. Combine common data points (same mission and adjacent) to save memory
        for ts in schedule:
            if ts["sched"] is None:
                continue

            start, finish = time_slice_to_date(sim_start, ts["time"])

            last_point = merge_time_slice(chart_data, last_point, start, finish, gs, ts["sched"])

            if len(ts["res"]) > 1:
                last_c_point = merge_time_slice(chart_data, last_c_point, start, finish, gs + "-conflict", "conflict")

            for m in ts["res"]:
                last_m_points[m] = merge_time_slice(chart_data, last_m_points.get(m, None), start, finish, gs + "-" + m, m)

        # If there is a reservation in progress at the end of the time, end it
        if last_point is not None:
            chart_data.append(last_point)
        if last_c_point is not None:
            chart_data.append(last_c_point)
        for m_point in last_m_points:
            chart_data.append(last_m_points[m_point])

    print("Charting {} datapoints...".format(len(chart_data)))
    fig = ff.create_gantt(chart_data, index_col='Resource', group_tasks=True,
        show_colorbar=True, title='Ground Station Schedules')
    plotly.offline.plot(fig, filename=filename)


# Convert raw time slice offset to an absolute time interval
def time_slice_to_date(start, offset):
    return str(start + datetime.timedelta(minutes = offset)), str(start + datetime.timedelta(minutes = offset + 1))

def percent(a, b):
    if b == 0:
        return 100
    return round((float(a)/float(b)) * 100)

if __name__ == "__main__":
    main()
