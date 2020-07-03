import pandas as pd
import ntpath
import sys


def create_segments(file, **kwargs):
    """takes a .csv route file (e.g 'EightyEight_Master.csv') with the data entries organised
    by 'nodes' / 'bus-stops' and restructures data into entries describing 'links' / 'route
    segments'; either returns a pandas Dataframe object or writes the merged data to a new .csv file
    (set **kwarg write_to_file='true' )"""

    if "write_to_file" in kwargs:
        write_to_file = kwargs["write_to_file"]
    else:
        write_to_file = "false"

    # import data for the bus route
    data = pd.read_csv(file)

    # create a data frame to hold all unique journey segments
    segments = pd.DataFrame()

    # populate the "segments" data frame by sub-route
    for route in data["ROUTEID"].unique():

        # check that each "PROGRNUMBER" corresponds to a single "STOPPOINTID"
        sub_route = data[(data["ROUTEID"] == route)]

        # map "PROGRNUMBER" to "STOPPOINTID"; "PROGRNUMBER" varies by sub-route...
        stop_order = {}
        min_num = sys.maxsize           # track start "PROGRNUMBER"
        max_num = 0                     # track end "PROGRNUMBER"

        for num in sub_route["PROGRNUMBER"].unique():
            stop_id = sub_route[(sub_route["PROGRNUMBER"] == num)]
            stop_order[num] = stop_id["STOPPOINTID"].unique()[0]
            if num < min_num:
                min_num = num
            if num > max_num:
                max_num = num

        # sort the values of "PROGRNUMBER" in ascending order - this is to mitigate against missing/skipped values
        nums = list(stop_order.keys())
        nums.sort()

        # iterate through sub-route data & transform into entry in "segments" data frame
        values = {}                                         # store the transformed data temporarily
        for index, row in sub_route.iterrows():

            seq = row["PROGRNUMBER"]  # the"PROGRNUMBER" corresponding to this stop

            # if not the first stop - fill in data for the previous segment
            if seq != min_num:

                # get "PROGRNUMBER" corresponding to the previous stop; this isn't always (seq - 1)!
                pre = nums[nums.index(seq) - 1]

                this_stop = stop_order[seq]
                prev_stop = stop_order[pre]

                row_id = "%d-%d-%d" % (row["UNIQUE_TRIP"], prev_stop, this_stop)

                # create a dict for this segment if not one already
                if row_id not in values:
                    values[row_id] = {}

                values[row_id]["Segment"] = "%d-%d" % (prev_stop, this_stop)
                values[row_id]["StartStopID"] = prev_stop
                values[row_id]["EndStopID"] = this_stop
                values[row_id]["PlannedArrTime"] = row["PLANNEDTIME_ARR"]
                values[row_id]["ActualArrTime"] = row["ACTUALTIME_ARR"]
                values[row_id]["ArrDelay"] = row["DELAYARR"]

                values[row_id]["DayOfService"] = row["DAYOFSERVICE"]
                values[row_id]["TripID"] = row["TRIPID"]
                values[row_id]["LineID"] = row["LINEID"]
                values[row_id]["RouteID"] = row["ROUTEID"]
                values[row_id]["UniqueTripID"] = row["UNIQUE_TRIP"]
                #values[row_id]["ProgressNum"] = row["PROGRNUMBER"]
                values[row_id]["Month"] = row["MONTH"]
                values[row_id]["Weekday"] = row["DAYOFWEEK"]
                values[row_id]["TimeGroup"] = row["TIME_GROUP"]

            # if not the last stop - fill in data for the next segment
            if seq != max_num:

                # get the "PROGRNUMBER" corresponding to the next stop; this isn't always (seq + 1)!
                nxt = nums[nums.index(seq) + 1]

                this_stop = stop_order[seq]
                next_stop = stop_order[nxt]

                row_id = "%d-%d-%d" % (row["UNIQUE_TRIP"], this_stop, next_stop)

                # create a dict for this segment if not one already
                if row_id not in values:
                    values[row_id] = {}

                values[row_id]["Segment"] = "%d-%d" % (this_stop, next_stop)
                values[row_id]["StartStopID"] = this_stop
                values[row_id]["EndStopID"] = next_stop
                values[row_id]["PlannedDepTime"] = row["PLANNEDTIME_DEP"]
                values[row_id]["ActualDepTime"] = row["ACTUALTIME_DEP"]
                values[row_id]["DepDelay"] = row["DELAYDEP"]

                values[row_id]["DayOfService"] = row["DAYOFSERVICE"]
                values[row_id]["TripID"] = row["TRIPID"]
                values[row_id]["LineID"] = row["LINEID"]
                values[row_id]["RouteID"] = row["ROUTEID"]
                values[row_id]["UniqueTripID"] = row["UNIQUE_TRIP"]
                values[row_id]["ProgressNum"] = row["PROGRNUMBER"]
                values[row_id]["Month"] = row["MONTH"]
                values[row_id]["Weekday"] = row["DAYOFWEEK"]
                values[row_id]["TimeGroup"] = row["TIME_GROUP"]

        segments = segments.append(list(values.values()), ignore_index=True)

    # generate new features...
    # iterate through each segment to calculate "PlannedDuration", "ActualDuration" and "DurationErr"
    values = {"PlannedDuration": [], "ActualDuration": [], "DurationErr": []}
    for index, row in segments.iterrows():
        x = row["PlannedArrTime"] - row["PlannedDepTime"]
        y = row["ActualArrTime"] - row["ActualDepTime"]
        values["PlannedDuration"].append(x)
        values["ActualDuration"].append(y)
        values["DurationErr"].append(y - x)

    for key in values:
        segments[key] = values[key]

    if write_to_file == "false":
        return segments
    else:

        # get / create the name for the output file
        if "outfile" in kwargs:
            outfile = kwargs["outfile"]
        else:
            outfile = "%s_route_segments.csv" % (ntpath.basename(file).split("_")[0])

        # save merged data
        segments.to_csv(outfile, index=False)


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

    create_segments(raw_data, **opt_args)
