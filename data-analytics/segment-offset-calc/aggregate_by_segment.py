import pandas as pd
import sys
import ntpath


def aggregate_rows(data, **kwargs):

    # length of time (in seconds) intervals each segment is grouped by: defaults to 30 minutes
    if "interval" in kwargs:
        interval = kwargs["interval"]
    else:
        interval = 1800

    # assign "TimeSlots" to each segment - 30 minute intervals
    # base on "PlannedArrTime"
    intervals = []
    for index, row in data.iterrows():
        intervals.append(row["PlannedArrTime"] // interval)

    data["TimeSlot"] = intervals

    aggregate = pd.DataFrame()

    segments = []
    weekdays = []
    time_slots = []
    line_ids = []

    planned_durations_mean = []     # mean, median, sd, min, max
    planned_durations_std = []
    planned_durations_min = []
    planned_durations_max = []

    actual_durations_mean = []      # mean, median, sd, min, max
    actual_durations_std = []
    actual_durations_min = []
    actual_durations_max = []

    dep_delays_mean = []            # mean, median, sd, min, max
    dep_delays_std = []
    dep_delays_min = []
    dep_delays_max = []

    arr_delays_mean = []             # mean, median, sd, min, max
    arr_delays_std = []
    arr_delays_min = []
    arr_delays_max = []

    duration_errors_mean = []        # mean, median, sd, min, max
    duration_errors_std = []
    duration_errors_min = []
    duration_errors_max = []

    # calculate average times by "Segment" + "DayOfService" + "TimeSlot"
    j = len(data)
    k = 0

    for day in data["Weekday"].unique():

        day_data = data[(data["Weekday"] == day)]

        for interval in day_data["TimeSlot"].unique():

            interval_data = day_data[(data["TimeSlot"] == interval)]

            for segment in interval_data["Segment"].unique():

                segment_data = interval_data[(data["Segment"] == segment)]

                segments.append(segment)
                weekdays.append(day)
                time_slots.append(interval)
                line_ids.append(segment_data["LineID"].unique()[0])

                planned_durations_mean.append(segment_data["PlannedDuration"].mean())
                planned_durations_std.append(segment_data["PlannedDuration"].std())
                planned_durations_min.append(segment_data["PlannedDuration"].min())
                planned_durations_max.append(segment_data["PlannedDuration"].max())

                actual_durations_mean.append(segment_data["ActualDuration"].mean())
                actual_durations_std.append(segment_data["ActualDuration"].std())
                actual_durations_min.append(segment_data["ActualDuration"].min())
                actual_durations_max.append(segment_data["ActualDuration"].max())

                dep_delays_mean.append(segment_data["DepDelay"].mean())
                dep_delays_std.append(segment_data["DepDelay"].std())
                dep_delays_min.append(segment_data["DepDelay"].min())
                dep_delays_max.append(segment_data["DepDelay"].max())

                arr_delays_mean.append(segment_data["ArrDelay"].mean())
                arr_delays_std.append(segment_data["ArrDelay"].std())
                arr_delays_min.append(segment_data["ArrDelay"].min())
                arr_delays_max.append(segment_data["ArrDelay"].max())

                duration_errors_mean.append(segment_data["DurationErr"].mean())
                duration_errors_std.append(segment_data["DurationErr"].std())
                duration_errors_min.append(segment_data["DurationErr"].min())
                duration_errors_max.append(segment_data["DurationErr"].max())

                k += 1
                if j / k < 20:
                    k = 0
                    print("=", end="")

    aggregate["Segment"] = segments
    aggregate["Weekday"] = weekdays
    aggregate["TimeSlot"] = time_slots
    aggregate["LineID"] = line_ids

    aggregate["PlannedDuration-Mean"] = planned_durations_mean
    aggregate["PlannedDuration-Std"] = planned_durations_std
    aggregate["PlannedDuration-Min"] = planned_durations_min
    aggregate["PlannedDuration-Max"] = planned_durations_max

    aggregate["ActualDuration-Mean"] = actual_durations_mean
    aggregate["ActualDuration-Std"] = actual_durations_std
    aggregate["ActualDuration-Min"] = actual_durations_min
    aggregate["ActualDuration-Max"] = actual_durations_max

    aggregate["DepDelay-Mean"] = dep_delays_mean
    aggregate["DepDelay-Std"] = dep_delays_std
    aggregate["DepDelay-Min"] = dep_delays_min
    aggregate["DepDelay-Max"] = dep_delays_max

    aggregate["ArrDelay-Mean"] = arr_delays_mean
    aggregate["ArrDelay-Std"] = arr_delays_std
    aggregate["ArrDelay-Min"] = arr_delays_min
    aggregate["ArrDelay-Max"] = arr_delays_max

    aggregate["DurationErr-Mean"] = duration_errors_mean
    aggregate["DurationErr-Std"] = duration_errors_std
    aggregate["DurationErr-Min"] = duration_errors_min
    aggregate["DurationErr-Max"] = duration_errors_max
    print()

    return aggregate


def aggregate_by_segment(file, **kwargs):

    # deal with kwargs
    if "write_to_file" in kwargs:
        write_to_file = kwargs["write_to_file"]
    else:
        write_to_file = "false"

    if "out_dir" in kwargs:
        out_dir = kwargs["out_dir"]
    else:
        out_dir = ""

    if ("by_months" in kwargs) and (kwargs["by_months"] == "true"):
        by_months = True
    else:
        by_months = False

    data = pd.read_csv(file)

    # drop rows with missing values (this is safe to do as these rows represent
    # buses being introduced/removed part-way through a sub-route)
    data.dropna(axis=0, inplace=True)

    segments = pd.DataFrame()

    # if aggregating by months
    if by_months:

        # for unique value of month in dataset
        for month in list(data["Month"].unique()):

            # perform aggregation of data for this month only & append to 'segments' data frame
            month_aggregation = aggregate_rows(data[(data["Month"] == month)], **kwargs)
            month_aggregation["Month"] = month                      # add a 'Month' column for reference
            segments = segments.append(month_aggregation)

    # otherwise perform aggregation of data over entire data-set and append to 'segments' data-frame
    else:
        segments = segments.append(aggregate_rows(data, **kwargs))

    segments = add_start_id(segments)
    segments = add_end_id(segments)

    if write_to_file == "false":
        return segments
    else:

        # get / create the name for the output file
        if "outfile" in kwargs:
            outfile = kwargs["outfile"]
        else:
            if by_months is True:
                outfile = "%s_segments_avg_by_month.csv" % (ntpath.basename(file).split("_")[0])
            else:
                outfile = "%s_segments_avg.csv" % (ntpath.basename(file).split("_")[0])

        # save merged data
        save_path = "%s%s" % (out_dir, outfile)
        segments.to_csv(save_path, index=False)


def add_start_id(data):
    """ a function to re-introduce the 'StartStopID' field that was erroneously omitted in the previous step"""

    # check if column called "StartStopID" already exists
    if "StartStopID" in list(data.columns):

        # If so, print non-fatal error message and return original data set
        print("Column of name 'StartStopID' already exists in the data frame")
        return data

    else:

        # iterate through the data frame and extrapolate the start stop id from the 'Segment' field
        stop_ids = []

        for index, row in data.iterrows():
            # splitting the 'Segment' value by '-' gives the start & endpoint stop ids...
            stop_ids.append(row["Segment"].split("-")[0])

        data["StartStopID"] = stop_ids

        return data


def add_end_id(data):
    """ a function to re-introduce the 'StartStopID' field that was erroneously omitted in the previous step"""

    # check if column called "StartStopID" already exists
    if "EndStopID" in list(data.columns):

        # If so, print non-fatal error message and return original data set
        print("Column of name 'EndStopID' already exists in the data frame")
        return data

    else:

        # iterate through the data frame and extrapolate the end stop id from the 'Segment' field
        stop_ids = []

        for index, row in data.iterrows():
            # splitting the 'Segment' value by '-' gives the start & endpoint stop ids...
            stop_ids.append(row["Segment"].split("-")[1])

        data["EndStopID"] = stop_ids

        return data


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

    aggregate_by_segment(raw_data, **opt_args)
