import sys
from dragon.workflows.batch import Batch
from dragon.native.process import ProcessTemplate
from dragon.infrastructure.facts import PMIBackend
from dragon.native.process_group import ProcessGroup

if __name__ == '__main__':
    tmpl = ProcessTemplate(target=sys.executable,
                           args=("course2/orchestrating_MPI/mpi4py_example.py"))

    pg = ProcessGroup(pmi=PMIBackend.PMIX)
    pg.add_process(nproc=3, template=tmpl)
    pg.init()
    pg.start()
    pg.join()
    pg.close()
    print("Smoke test successful", flush=True)