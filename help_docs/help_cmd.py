import argparse
import os
import help_docs

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
        help_docs.display_job_doc(args.job[0])
    elif args.task is not None:
        help_docs.display_task_doc(args.task[0])        
    elif args.manual:
        help_docs.display_manual()
    elif args.readme:
        help_docs.display_readme()
    elif args.file:
        hdlihelp_docsb.display_file(args.file[0])
