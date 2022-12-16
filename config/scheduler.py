SCHEDULER = {
    "checkin": {
        "func": "checkin",
        "args": [
            None,
            None
        ],
        "hour": "09",
        "minute": "00",
        "second": "00",
        "day_of_week": "mon-sat"
    },
    "checkout": {
        "func": "checkout",
        "args": [
            None,
            None
        ],
        "hour": "20",
        "minute": "00",
        "second": "00",
        "day_of_week": "mon-sat"
    },
    "check-and-alert": {
        "func": "check_and_alert",
        "args": [],
        "hour": "08-22",
        "minute": "*/10",
        "second": "00",
        "day_of_week": "mon-sat"
    }
}
