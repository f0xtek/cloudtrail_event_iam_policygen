#!/usr/bin/env python3

import sys

import pandas

EXCEL_FILE = sys.argv[1]


def read_excel(filename):
    df = pandas.read_excel(filename)
    return df


def remove_redundant_data(dataframe):
    return dataframe.drop(
        [
            "User name",
            "AWS access key",
            "Event time",
            "AWS region",
            "Request ID",
            "Event ID",
            "Read-only",
            "Event type",
            "Recipient Account Id",
            "Event category",
            "Error code",
            "Source IP address",
            "User agent",
        ],
        axis=1,
    )


def create_policy_action(source, name):
    return f"{source}:{name}"


def generate_iam_policy_actions(event_sources, event_names):
    sources_names = zip(event_sources, event_names)
    return set([create_policy_action(item[0], item[1]) for item in sources_names])


def get_service_from_event_source(event_source):
    return event_source.split(".")[0]


def print_policy_actions(actions):
    for index, value in enumerate(actions):
        if index != len(actions) - 1:
            suffix = ","
        else:
            suffix = ""
        print(f"{value}{suffix}")


if __name__ == "__main__":
    data = read_excel(EXCEL_FILE)
    data = remove_redundant_data(data)
    data["Event source"] = [
        get_service_from_event_source(source) for source in data["Event source"]
    ]

    policy_actions = generate_iam_policy_actions(
        data["Event source"], data["Event name"]
    )
    print_policy_actions(policy_actions)
