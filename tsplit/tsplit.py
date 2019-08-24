#!/usr/bin/env python3

import argparse
import libxml2
import logging

logger = logging.getLogger('tsplit')

def import_durations(file_paths, split_by="file"):
    """
    inport_junit takes a junit xml file and returns a dict of tests and their durations

    Args:
        file_path (string): Path to junit file to parse.

    Returns:
        durations (dict): Test names and durations split by classname (usually test files)

    Example:
        
    """
    durations = dict()
    for xml_file in file_paths:
        try:
            # xml = JUnitXml.fromfile(xml_file)
            xml = libxml2.parseFile(xml_file)
            logger.debug(xml)
        except:
            logger.error(f"Unable to parse {xml_file}")
            continue

        ctxt = xml.xpathNewContext()
        res = ctxt.xpathEval("//testcase")
        for tc in res:
            logger.debug(f"Test: {tc}")
            try:
                if split_by == "file":
                    split = tc.prop("file")
                else:
                    split = tc.prop("classname")
                time = float(tc.prop("time"))
            except:
                logger.error(f"Unable to extract unique identifier for {tc}")

            if split in durations:
                durations[split] += time
            else:
                durations[split] = time

    return durations

def check_smallest(groups):
    sg = 0
    for i in range(0, len(groups)):
        if groups[i]['total_duration'] < groups[sg]['total_duration']:
            sg = i

    return sg

def sort_durations(durations, num):
    # Reverse Sort
    s = sorted(durations.items(), key=lambda kv: kv[1], reverse=True)

    # Track which group is the smallest
    smallest_group = 0
    groups = []

    # Create num groups
    for i in range(num):
        groups.append({'total_duration': 0, 'tests': []})

    for t, d in s:
        groups[smallest_group]['total_duration'] += d
        groups[smallest_group]['tests'].append(t)

        smallest_group = check_smallest(groups)

    return groups


def print_groups(groups):
    for idx, group in enumerate(groups):
        logger.debug(f"Group {idx+1}: {group['tests']}\t\t{group['total_duration']}")
        print(f"Group {idx+1}:\t\t{group['total_duration']}")


def output_files(groups, prefix="group"):
    for idx, group in enumerate(groups):
        with open(f"{prefix}{idx+1}", "w") as f:
            f.write(" ".join(group['tests']))


def output_env_vars(groups, prefix="GROUP_"):
    import os

    for idx, group in enumerate(groups):
        os.environ[f"{prefix}{idx}"] = " ".join(group['tests'])


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--groups', '-g', type=int, default=4, help='Number of groups to split the tests into.')
    parser.add_argument('--output', '-o', default=None, type=str, help='Output text files with the lists.')
    parser.add_argument('--env', '-e', default=None, type=str, help='Output environment variables for lists.')
    parser.add_argument('file_paths', metavar='files', type=str, nargs='+',
                    help='Files to parse.')
    args = parser.parse_args()

    d = import_durations(args.file_paths)
    g = sort_durations(d, args.groups)
    print_groups(g)
    if args.output:
        output_files(g, prefix=args.output)

    if args.env:
        output_env_vars(g, prefix=args.env)

if __name__ == "__main__":
    main()
