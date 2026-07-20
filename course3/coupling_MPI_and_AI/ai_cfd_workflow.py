import sys
from dragon.workflows.batch import Batch
from dragon.native.process import ProcessTemplate

def main():
    mpitmpl = ProcessTemplate(target=sys.executable, args=("../../course2/orchestrating_MPI/mpi4py_example.py",))
    batch = Batch()
    batch.job()

if __name__ == '__main__':
    main()