from datetime import datetime


def timestamp2datetime(timestamp, formatting='%Y-%m-%d %H:%M:%S'):
    time = datetime.fromtimestamp(timestamp)
    return time.strftime(formatting)
