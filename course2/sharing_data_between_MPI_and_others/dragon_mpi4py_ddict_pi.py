import os
import random
import sys
from pathlib import Path

import multiprocessing as mp

import dragon
from dragon.data.ddict import DDict
from dragon.infrastructure.facts import PMIBackend
from dragon.native.process import MSG_PIPE, Process, ProcessTemplate
from dragon.native.process_group import ProcessGroup

try:
    mp.set_start_method("dragon")
except RuntimeError:
    pass


def monte_carlo_batch_pi(rng, samples_per_iteration):
    inside_circle = 0
    for _ in range(samples_per_iteration):
        x_coord = rng.random()
        y_coord = rng.random()
        if x_coord * x_coord + y_coord * y_coord <= 1.0:
            inside_circle += 1
    return 4.0 * inside_circle / samples_per_iteration


def run_rank_worker():
    from mpi4py import MPI

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    serialized_ddict = os.environ["DRAGON_DDICT_SER"]
    iterations = int(os.environ["DRAGON_PI_ITERATIONS"])
    samples_per_iteration = int(os.environ["DRAGON_PI_SAMPLES_PER_ITERATION"])
    ddict = DDict.attach(serialized_ddict)

    try:
        initial_pi = ddict["pi"]
        local_pi = initial_pi
        prior_weight = 1

        rng = random.Random(1729 + rank)
        for batch_index in range(iterations):
            batch_pi = monte_carlo_batch_pi(rng, samples_per_iteration)
            local_pi = (
                ((prior_weight + batch_index) * local_pi) + batch_pi
            ) / (prior_weight + batch_index + 1)

        ddict[f"rank_{rank}_pi_checkpoint"] = local_pi
        ddict.pput(f"rank_{rank}_pi", local_pi)
        ddict.pput(
            f"rank_{rank}_meta",
            {
                "initial_pi": initial_pi,
                "iterations": iterations,
                "samples_per_iteration": samples_per_iteration,
            },
        )
        ddict.checkpoint()
        print(f"rank {rank} finished with pi={local_pi:.8f}")
    finally:
        ddict.detach()



def launch_pi_job(total_ranks=4, iterations=100, samples_per_iteration=10000):
    ddict = DDict(
        1,
        1,
        128 * 1024 * 1024,
        wait_for_keys=True,
        working_set_size=4,
    )
    ddict["pi"] = 0.0
    serialized_ddict = ddict.serialize()

    process_group = None

    try:
        env = os.environ.copy()
        env["DRAGON_DDICT_SER"] = serialized_ddict
        env["DRAGON_PI_ITERATIONS"] = str(iterations)
        env["DRAGON_PI_SAMPLES_PER_ITERATION"] = str(samples_per_iteration)

        script_path = Path(__file__).resolve()
        process_group = ProcessGroup(restart=False, pmi=PMIBackend.PMIX)
        process_group.add_process(
            nproc=total_ranks,
            template=ProcessTemplate(
                target=sys.executable,
                args=(str(script_path), "--worker"),
                env=env,
                cwd=os.getcwd()
            ),
        )

        process_group.init()
        process_group.start()

        for i in range(iterations):
            rank_values = [float(ddict[f"rank_{rank}_pi"]) for rank in range(total_ranks)]
            average_pi = sum(rank_values) / len(rank_values)

            ddict.checkpoint()
            ddict["pi"] = average_pi

            print("Per-rank pi estimates:")
            for rank, rank_value in enumerate(rank_values):
                print(f"  rank_{rank}: {rank_value:.8f}")
            print(f"Averaged pi: {average_pi:.8f}")
            print(f"Checkpoint-updated pi key: {ddict['pi']:.8f}")

        process_group.join()
        process_group.close()

    finally:
        if process_group is not None:
            try:
                process_group.close()
            except Exception:
                pass

        ddict.detach()
        ddict.destroy()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--worker":
        run_rank_worker()
        return

    launch_pi_job()


if __name__ == "__main__":
    main()