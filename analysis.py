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

# Create a gantt chart of ground station utilization
def chart_utilization(data, filename):
    chart_data = []
    sim_start = datetime.datetime(2000, 1, 1, 0, 0)

    for gs, schedule in data.items():
        for ts in schedule:
            if ts["sched"] is None:
                continue

            start, finish = time_slice_to_date(sim_start, ts["time"])

            point = {}
            point["Task"] = gs
            point["Start"] = start
            point["Finish"] = finish
            point["Resource"] = ts["sched"]
            chart_data.append(point)

            if len(ts["res"]) > 1:
                c_point = {}
                c_point["Task"] = gs + "-conflict"
                c_point["Start"] = start
                c_point["Finish"] = finish
                c_point["Resource"] = "conflict"
                chart_data.append(c_point)

            for m in ts["res"]:
                m_point = {}
                m_point["Task"] = gs + "-" + m
                m_point["Start"] = start
                m_point["Finish"] = finish
                m_point["Resource"] = m
                chart_data.append(m_point)

    fig = ff.create_gantt(chart_data, index_col='Resource', group_tasks=True,
        show_colorbar=True, title='Ground Station Schedules')
    plotly.offline.plot(fig, filename=filename)


# Convert raw time slice offset to an absolute time interval
def time_slice_to_date(start, offset):
    return str(start + datetime.timedelta(minutes = offset)), str(start + datetime.timedelta(minutes = offset + 1))

def percent(a, b):
    return round((float(a)/float(b)) * 100)

if __name__ == "__main__":
    main()
