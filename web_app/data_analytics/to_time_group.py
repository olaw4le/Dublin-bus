def to_time_group(time):
    """assign a 'time_group' to the passed time"""

    # if time is greater than 24:00; assign to group 0
    if (time <= 0) or (time >= 86400):
        return 0

    # between 00:00 - 07:30 (24hr); time groups are by hour
    if time <= 27000:
        return (time - 1) // 3600

    # between 07:30 - 09:00 (24hr); time groups are by half-hour
    elif time <= 32400:
        return (to_time_group(27000)) + ((time - 27000) // 1800)

    # between 09:00 - 16:50 (24hr); time groups are by hour
    elif time <= 59400:
        return (to_time_group(32400)) + ((time - 32400) // 3600)

    # between 16:30 - 19:00 (24hr); time groups are by half-hour
    elif time <= 68400:
        return (to_time_group(59400)) + ((time - 59400) // 1800)

    # between 19:00 - 24:00 (24hr); time groups are by hour
    else:
        return (to_time_group(68400)) + ((time - 68400) // 3600)