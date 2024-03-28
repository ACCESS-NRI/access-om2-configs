import time
import subprocess as sp


def wait_for_qsub(run_id):
    """
    Wait for the qsub job to terminate.
    """

    while True:
        time.sleep(1*60)
        try:
            qsub_out = sp.check_output(['qstat', run_id], stderr=sp.STDOUT)
        except sp.CalledProcessError as err:
            qsub_out = err.output

        qsub_out = qsub_out.decode()

        if 'Job has finished' in qsub_out:
            break


def get_git_branch_name(path):
    """Get the git branch name of the given git directory"""
    try:
        cmd = 'git rev-parse --abbrev-ref HEAD'
        result = sp.check_output(cmd, shell=True,
                                         cwd=path).strip()
        # Decode byte string to string
        branch_name = result.decode('utf-8')
        return branch_name
    except sp.CalledProcessError:
        return None
