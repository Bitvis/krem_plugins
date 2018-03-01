import argparse
import os
import loglib

def readArgs():
    parser = argparse.ArgumentParser(description=
                                    "Display task log",
                                    prog='krem log')
    # Add arguments here
    group = parser.add_argument_group()

    group.add_argument("-j", "--job", nargs=1, help="Display task log from target job", required=True)
    group.add_argument("-r", "--run-nr", nargs=1, help="Display task log entries from given run number only. Format: x_x. Example: 21_1.")
    group.add_argument("-l", "--last", nargs=1, help="Display n-th last task log")

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = readArgs()
    run_nr = None
    last = None

    if args.run_nr:
        run_nr = args.run_nr[0]

    if args.last:
        last = args.last[0]

    loglib.display_task_log(args.job[0], run_nr, last)
