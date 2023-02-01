SCHEDULER = {
    "checkin": {
        "func": "checkin",
        "args": [
            None,
            None
        ],
        "month": "*",
        "day": "*",
        "hour": "08",
        "minute": "03",
        "second": "00",
        "day_of_week": "mon-fri"
    },
    "checkout": {
        "func": "checkout",
        "args": [
            None,
            None
        ],
        "month": "*",
        "day": "*",
        "hour": "20",
        "minute": "03",
        "second": "00",
        "day_of_week": "mon-fri"
    },
    "check-and-alert": {
        "func": "check_and_alert",
        "args": [],
        "month": "*",
        "day": "*",
        "hour": "08-22",
        "minute": "*/10",
        "second": "00",
        "day_of_week": "mon-fri"
    }
}
