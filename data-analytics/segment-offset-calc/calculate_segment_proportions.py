import pandas as pd
import ntpath
import sys


def load_data(file_path):

    # import segment data
    data = pd.read_csv(file_path)

    return data


def save_data(data, filename):

    # save merged data
    data.to_csv(filename, index=False)


def calc_seg_props(data):

    # drop rows containing null data
    data.dropna(inplace=True)

    # data frame to represent output data - proportion of total journey that each segment represents...
    proportions = pd.DataFrame()

    # for each sub-route in the data set
    for sub_route in list(data["RouteID"].unique()):

        # these are the constant values we want... (ie. will exist for all sub-routes...)
        entries = {"RouteID": [], "UniqueTripID": [], "Weekday": [], "Month": [], "TimeGroup": [],
                   "PlannedDepTime": [], "ActualDepTime": [], "DepDelay": [], "PlannedArrTime": [],
                   "ActualArrTime": [], "ArrDelay": [], "PlannedDuration": [], "ActualDuration": [],
                   "DurationErr": [], "FirstStop": [], "FinalStop": []}

        # select only the data for that sub-route
        sub_route_data = data[(data["RouteID"] == sub_route)]

        # create column for each segment in this sub-route & add to the output dict
        segments_in_route = []
        for segment in list(sub_route_data["Segment"].unique()):
            entries[segment] = []
            segments_in_route.append(segment)

        # get the Stop ID's coresponding to the terminus stops of the sub-route
        first_stop = sub_route_data[(sub_route_data["ProgressNum"] == sub_route_data["ProgressNum"].min())]["StartStopID"].unique()[0]
        final_stop = sub_route_data[(sub_route_data["ProgressNum"] == sub_route_data["ProgressNum"].max())]["EndStopID"].unique()[0]

        # select only data by "UniqueTripID"s where a trip is full sub-route
        # (ie. has entries corresponding to the terminus stops)
        for trip in list(sub_route_data["UniqueTripID"].unique()):
            a = len(sub_route_data[((sub_route_data["UniqueTripID"] == trip) & (sub_route_data["StartStopID"] == first_stop))])
            b = len(sub_route_data[((sub_route_data["UniqueTripID"] == trip) & (sub_route_data["EndStopID"] == final_stop))])

            if (a > 0) and (b > 0):
                entries["UniqueTripID"].append(trip)

        # ditch rows representing "UniqueTripID"s which don't traverse entire sub-route
        sub_route_data = sub_route_data[(sub_route_data["UniqueTripID"].isin(entries["UniqueTripID"]))]

        # for each remaining "UniqueTripID"
        for trip in entries["UniqueTripID"]:

            # get the data entries for the first & final segment on the trip...
            start = sub_route_data[
                ((sub_route_data["UniqueTripID"] == trip) & (sub_route_data["StartStopID"] == first_stop))].iloc[0]
            end = sub_route_data[
                ((sub_route_data["UniqueTripID"] == trip) & (sub_route_data["EndStopID"] == final_stop))].iloc[0]

            entries["RouteID"].append(start["RouteID"])
            entries["Weekday"].append(start["Weekday"])
            entries["Month"].append(start["Month"])
            entries["TimeGroup"].append(start["TimeGroup"])

            entries["FirstStop"].append(first_stop)
            entries["FinalStop"].append(final_stop)

            entries["PlannedDepTime"].append(start["PlannedDepTime"])
            entries["ActualDepTime"].append(start["ActualDepTime"])
            entries["DepDelay"].append(start["DepDelay"])

            entries["PlannedArrTime"].append(end["PlannedArrTime"])
            entries["ActualArrTime"].append(end["ActualArrTime"])
            entries["ArrDelay"].append(end["ArrDelay"])

            entries["PlannedDuration"].append(entries["PlannedArrTime"][-1] - entries["PlannedDepTime"][-1])
            entries["ActualDuration"].append(entries["ActualArrTime"][-1] - entries["ActualDepTime"][-1])
            entries["DurationErr"].append(entries["ActualDuration"][-1] - entries["PlannedDuration"][-1])

            for segment in segments_in_route:

                try:

                    seg = sub_route_data[
                        ((sub_route_data["UniqueTripID"] == trip) & (sub_route_data["Segment"] == segment))]
                    if len(seg) == 1:
                        entries[segment].append((seg.iloc[0]["ActualDuration"] / entries["ActualDuration"][-1]))
                    else:
                        # append denote missing values
                        entries[segment].append(float("nan"))

                except Exception as e:
                    print(e)
                    # append denote missing values
                    entries[segment].append(float("nan"))

        # combine data
        proportions = proportions.append(pd.DataFrame(entries))

    return proportions


def group_seg_props(data):

    # data frame to represent output data - proportion of total journey that each segment represents...
    grouped = pd.DataFrame()

    # for each sub-route in the data set
    for sub_route in list(data["RouteID"].unique()):

        # select sub-route data
        sub_route_data = data[(data["RouteID"] == sub_route)]

        # group data by "Month", "Weekday" and "TimeGroup"
        for month in list(sub_route_data["Month"].unique()):
            for day in list(sub_route_data["Weekday"].unique()):
                for t_group in list(sub_route_data["TimeGroup"].unique()):

                    selection = sub_route_data[((sub_route_data["Month"] == month) &
                                                (sub_route_data["Weekday"] == day) &
                                                (sub_route_data["TimeGroup"] == t_group))]

                    # if there is data in this selection;
                    if len(selection) > 0:

                        # these are the constant values we want... (ie. will exist for all selections)
                        constants = ["RouteID", "Weekday", "Month", "TimeGroup", "FirstStop", "FinalStop"]

                        entry = {}

                        for col in selection.columns:
                            if col in constants:
                                entry[col] = [selection.iloc[0][col]]
                            else:
                                entry[col] = [selection[col].mean()]

                        grouped = grouped.append(pd.DataFrame(entry))

    return grouped


def main(infile, **kwargs):
    """define the execution loop of this script"""

    if "group"in kwargs:
        group = kwargs["group"]
    else:
        group = False

    if "to_csv" in kwargs:
        to_csv = kwargs["to_csv"]
    else:
        to_csv = False

    data = load_data(infile)

    proportions = calc_seg_props(data)

    if to_csv:
        outfile = "%s_proportions.csv" % (ntpath.basename(infile).split("_")[0])
        save_data(proportions, outfile)

    elif group is False:
        return proportions

    if group:
        grouped = group_seg_props(proportions)

        if to_csv:
            outfile = "%s_proportions_grouped.csv" % (ntpath.basename(infile).split("_")[0])
            save_data(grouped, outfile)

        else:
            return grouped


if __name__ == "__main__":

    raw_data = sys.argv[1]

    # check for key-word arguments from bash
    c = 2
    opt_args = {}
    while c < len(sys.argv):
        field = sys.argv[c].strip("-")
        value = sys.argv[c+1]
        opt_args[field] = value
        c += 2

    main(raw_data, **opt_args)
    print("done")
