import argparse
import os
import job_validator

def readArgs():
    parser = argparse.ArgumentParser(description=
                                    "Runs validation of given job",
                                    prog='krem validate')
    # Add arguments here
    group = parser.add_argument_group()
    group.add_argument("-j", "--job", nargs=1, help="Target job to validate, required=True")
    
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = readArgs()

    if args.job is not None:
        validator = job_validator.Validator(args.job[0])
        validator.run()
    
