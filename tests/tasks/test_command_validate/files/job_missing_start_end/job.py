


from krempack.core import kjob
from library.returncodes import *
from library.setup import setup_plugins

if __name__ == '__main__':
    job = kjob.Job(__file__, rc)
    setup_plugins(job.plugin_handler)

    #job.start()


    err = job.run_task_serial('task_foo', 'run_without_arguments')

    job.run_task_parallel('task_foo', 'run_with_named_arguments', arguments=[("arg1", ""), ("arg2", "run_in_parallel")])
    job.run_task_parallel('task_foo', 'run_with_named_arguments', arguments=[("arg1", "also"), ("arg2", "run_in_parallel")])
    task_results = job.wait_for_complete()


    all_task_results = job.get_task_results()


    #job.end()

    exit(rc.PASS)

