#!/usr/bin/python

from google.cloud import errorreporting_v1beta1
from datetime import datetime
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=str, help="GCP project id. Default - autodoc-234411 ", default="autodoc-234411")
    parser.add_argument("--name", type=str, help="GCP log name")
    parser.add_argument("--period", type=str, help="Time period (one of PERIOD_1_HOUR, PERIOD_6_HOURS, PERIOD_1_DAY, PERIOD_1_WEEK, PERIOD_30_DAYS, PERIOD_UNSPECIFIED). Default - PERIOD_1_HOUR", default="PERIOD_1_HOUR")
    parser.add_argument("--group", type=str, help="Group ID")
    args = parser.parse_args()

    client = errorreporting_v1beta1.ErrorStatsServiceClient()
    project_name = "projects/" + args.project

    time_range = {"period": args.period}

    affected_services_list = []

    if args.name is None:
        print(bcolors.HEADER + "Services names:" + bcolors.ENDC)
        for element in client.list_group_stats(project_name, time_range):
            for affected_service in element.affected_services:
                if affected_service.service not in affected_services_list:
                    affected_services_list.append(affected_service.service)
                    print(affected_service.service)
        exit(0)
    else:
        if args.group is None:
            print(bcolors.HEADER + '{:20}{:7}{:135}{:25}{:20}{:10}'.format("Group ID", "Count", "Error", "First seen", "Last seen", "Responde Code") + bcolors.ENDC)
            for element in client.list_group_stats(project_name, time_range, None, {"service": args.name}):
                print('{:20}{:7}{:135}{:25}{:20}{:10}'.format(element.group.group_id,
                                                              str(element.count),
                                                              element.representative.message.encode('utf-8').split('\n', 1)[0][:128] + "..",
                                                              datetime.utcfromtimestamp(element.first_seen_time.seconds).strftime('%Y-%m-%d %H:%M:%S'),
                                                              pretty_date(int(element.last_seen_time.seconds)),
                                                              element.representative.context.http_request.response_status_code))
        else:
            for event in client.list_events(project_name, args.group, None, time_range):
                print("\n\n")
                print(bcolors.HEADER + "---- " + datetime.utcfromtimestamp(event.event_time.seconds).strftime('%Y-%m-%d %H:%M:%S') + " ----" + bcolors.ENDC)
                print(event.context.http_request.method + "   " + event.context.http_request.url + "   " + str(event.context.http_request.response_status_code) + "\n")
                print(event.message)


if __name__ == '__main__':
    main()
