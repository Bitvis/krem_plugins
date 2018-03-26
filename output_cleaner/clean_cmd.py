import argparse
import output_cleaner

def readArgs():
    parser = argparse.ArgumentParser(description=
                                    "Clean Krem output directory.",
                                    prog='krem clean')
    # Add arguments here
    group_1 = parser.add_mutually_exclusive_group(required=True)
    group_1.add_argument("-j", "--jobs", nargs='+', help="Target jobs to clean")
    group_1.add_argument("--all", action="store_true", help="Clean all jobs")

    group_2 = parser.add_argument_group()
    group_2.add_argument("-f", "--force", action='store_true', help="Ignore unexpected content in clean target")
    group_2.add_argument("-k", "--keep", nargs=1, type=int, help="Keep the n latest output instances")

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = readArgs()

    result = 0

    if args.all:
        result = output_cleaner.clean_all(args.force, args.keep)
    else:
        output_cleaner.clean(args.jobs, args.force, args.keep)
        result = 0

    exit(result)
    