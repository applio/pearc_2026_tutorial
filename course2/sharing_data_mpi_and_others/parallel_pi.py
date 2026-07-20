import os
import sys
from pathlib import Path
import random

from dragon.native.process_group import ProcessGroup
from dragon.native.process import ProcessTemplate
from dragon.data import DDict
from dragon.utils import XPickler

def worker():
    # worker is invoked `python parallel_pi.py dd_ser_value iterations samples_per_iteration`
    # with values for each of the values after the program name
    dd_ser = sys.argv[2]
    ddict = DDict.attach(dd_ser)
    iterations = int(sys.argv[3])
    samples_per_iteration = int(sys.argv[4])
    proc_id = ddict.fetch_add("worker_id")

    print(f"Worker {proc_id} says: Hello!", flush=True)
    for i in range(iterations):
        # The following waits until this value is available for this checkpoint
        # because of wait_for_keys on the ddict.
        print(f"Worker {proc_id} waiting for pi from orchestrator.", flush=True)
        pi = ddict.bget("pi")

        inside_circle = 0
        for _ in range(samples_per_iteration):
            x_coord = random.random()
            y_coord = random.random()
            if x_coord * x_coord + y_coord * y_coord <= 1.0:
                inside_circle += 1

        pi = (pi + (4.0 * inside_circle / samples_per_iteration))/2

        print(f"Proc {proc_id} providing its update for pi={pi}", flush=True)
        ddict[f"worker{proc_id}"] = pi
        ddict.checkpoint()

def python():
    ddict = DDict(
        1,
        1,
        128 * 1024 * 1024,
        wait_for_keys=True,
        working_set_size=4,
    )

    samples_per_iteration = 1000
    iterations = 7

    pg = ProcessGroup()  # or pmi=PMIBackend.PMIX

    num_procs = 10
    script_path = Path(__file__).resolve()
    proc_template = ProcessTemplate(target=sys.executable,
                args=(str(script_path), "worker", ddict.serialize(), iterations, samples_per_iteration),
                cwd=os.getcwd())

    pg.add_process(nproc=num_procs, template=proc_template)

    print("Writing initial pi value before iteration 0.", flush=True)
    ddict.bput("pi", 0.0)

    pg.init()
    pg.start()

    for i in range(iterations):
        pi = 0
        for proc_id in range(num_procs):
            pi += ddict[f"worker{proc_id}"]

        ddict.checkpoint()

        pi = pi / num_procs

        print(f"Writing updated pi={pi} value after iteration {i}.", flush=True)
        ddict.bput("pi", pi)

    pg.join()
    pg.close()
    print(f"Writing final version of pi={pi}", flush=True)
    ddict.destroy()

def cpp():
    ddict = DDict(
        1,
        1,
        128 * 1024 * 1024,
        wait_for_keys=True,
        working_set_size=4,
        trace=True
    )

    # These two lines are different when using C++ but could be used for Python as well.
    xp = XPickler()
    xd = ddict.pickler(xp, xp)

    samples_per_iteration = 1000
    iterations = 7

    pg = ProcessGroup()  # or pmi=PMIBackend.PMIX

    num_procs = 10
    test_dir = Path(__file__).resolve().parent
    exe = "worker"

    # Arguments start the binary directly when running C++ code
    proc_template = ProcessTemplate(target=str(test_dir / exe),
                args=(xd.serialize(), iterations, samples_per_iteration),
                cwd=os.getcwd())

    pg.add_process(nproc=num_procs, template=proc_template)

    print("Writing initial pi value before iteration 0.", flush=True)
    xd["pi"] = 0.0

    pg.init()
    pg.start()

    for i in range(iterations):
        pi = 0
        for proc_id in range(num_procs):
            pi += xd[f"worker{proc_id}"]

        xd.checkpoint()

        pi = pi / num_procs

        print(f"Writing updated pi={pi} value after iteration {i}.", flush=True)
        xd["pi"] = pi

    pg.join()
    pg.close()
    print(f"Writing final version of pi={pi}", flush=True)
    xd.destroy()


if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == "worker":
        worker()
    else:
        if sys.argv[1] == "python":
            python()
        else:
            cpp()


