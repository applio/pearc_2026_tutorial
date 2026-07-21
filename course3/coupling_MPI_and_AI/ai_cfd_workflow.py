import sys
from dragon.workflows.batch import Batch
from dragon.native.process import ProcessTemplate
from dragon.infrastructure.facts import PMIBackend

def queue_job(batch, nranks):

    rank_tmpls = [(nranks, ProcessTemplate(target=sys.executable,
                                           args=("../../course2/orchestrating_MPI/mpi4py_example.py",)))]
    job = batch.job(process_templates=rank_tmpls, pmi=PMIBackend.PMIX)
    print(f"Got a job {job}", flush=True)
    return job.uid, job


def main():

    batch = Batch()

    mpijobs = []
    for _ in range(1):
        uid, job = queue_job(batch, 2)
        mpijobs.append(job)

    for job in mpijobs:
        try:
            ecodes = job.get()
            print(f"Got ecodes: {ecodes}", flush=True)
        except Exception as e:
            print(f"Got exception from MPI job: {e}", flush=True)

    #completed_job = tbl[batch.poll()]
    batch.join()
    batch.destroy()

if __name__ == '__main__':
    main()