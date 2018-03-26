


from krempack.core import kjob
from library.returncodes import *
from library.setup import *

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)
    setup_plugins(job.plugin_handler)

    job.start()
    err = job.run_task_serial('task_foo', 'run_without_arguments')

    if err == rc.PASS:
        # run_with_single_argument require arguments, but we are not passing any to trigger validation fault
        err = job.run_task_serial('task_foo', 'run_with_single_argument')

    job.end()

    exit(rc.PASS)
    
