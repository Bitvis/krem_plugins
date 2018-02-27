import argparse
import os
import hdlib

def readArgs():
    parser = argparse.ArgumentParser(description=
                                    "Display task and job readme files",
                                    prog='krem help')
    # Add arguments here
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-j", "--job", nargs=1, help="Display markdown file from target job")
    group.add_argument("-t", "--task", nargs=1, help="Display markdown file from target task")
    group.add_argument("-m", "--manual", action='store_true', help="Display KREM manual")
    group.add_argument("-r", "--readme", action='store_true', help="Display KREM readme")
    group.add_argument("-f", "--file", nargs=1, help="Display given markdown file")
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = readArgs()

    if args.job is not None:
        hdlib.display_job_doc(args.job[0])
    elif args.task is not None:
        hdlib.display_task_doc(args.task[0])        
    elif args.manual:
        hdlib.display_manual()
    elif args.readme:
        hdlib.display_readme()
    elif args.file:
        hdlib.display_file(args.file[0])
