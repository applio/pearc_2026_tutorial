# Programming High-Performance AI-coupled HPC Workflows

## Tutorial Goals
The primary goal of this tutorial is that attendees gain a deeper understanding of how to design high-performance AI-coupled
HPC workflows through direct experience with DragonHPC [6], a distributed runtime that supports a variety of orchestration
and communication patterns typical of such workflows. To achieve this primary goal, the tutorial is organized into three courses
each covering a significant contributing concept. In the first two courses, attendees will become familiar with the standard
Python multiprocessing API, how DragonHPC’s extension enables multi-node computation needed for data processing and AI
workloads at-scale, and techniques to optimize data exchange within the workflow (including DragonHPC’s features that simplify
remote data placement for users). In the last course, attendees will learn how to construct an AI+HPC coupled workflow using
DragonHPC.

## Outcomes
Attendees will be provided exercises and solutions, primarily in the form of Jupyter notebooks. These notebooks are designed to
give attendees a variety of code patterns commonly found in AI+HPC workflows that can be easily incorporated into their own
use cases. By learning how to take advantage of the features of DragonHPC, attendees will have a toolbox of techniques that
can be explored on their laptop or common HPC platforms and be able to scale their workloads to leadership scale systems with
little-to-no code changes.

## Agenda
| Time Slot | Minutes | Course | Topic/Exercise Presenter(s) |
| --- | --- | --- | --- |
| 0:00 - 0:15 | 15 | Tutorial introduction | P. Mendygral |
| 0:15 - 0:45 | 30 | Presentation: AI+HPC workflows and DragonHPC | C. Simpson |
| 0:45 - 1:00 | 15 | 1 | Preparations for exercises | P. Mendygral<br>T. Maiden |
| 1:00 - 1:30 | 30 | 1 | Python multiprocessing across multiple nodes | P. Mendygral<br>D. Potts |

1:30 - 2:00 30 1 Managing Python objects, tensors, and contiguous C. Simpson
data with the in-memory distributed dictionary K. Lee
(DDict API)
2:00 - 2:15 15 Coffee Break
2:15 - 2:45 30 2 Using Python multiprocessing with GPUs, and P. Mendygral
PyTorch for multi-node LLM inference
2:45 - 3:00 15 2 Checkpoint with attendees/Q&A All presenters
3:00 - 3:15 15 2 Orchestrating MPI applications with the P. Mendygral
ProcessGroup API
3:15 - 3:45 30 2 Sharing data between MPI and other processes K. Lee
using the DDict API C. Simpson
3:45 - 4:15 30 3 Coupling MPI applications with PyTorch-based P. Mendygral
inference and training C. Simpson
4:15 - 4:30 15 3 Checkpoint with attendees/Q&A All presenters
4:30 - 4:45 15 Coffee Break
4:45 - 5:50 65 Review/discussion/Q&A/hackathon All presenters
5:50 - 6:00 10 Wrap-up and next steps P. Mendygral

## Primary tool website
* [DragonHPC Homepage](http://dragonhpc.org)

## Primary tool documentation
* [DragonHPC](https://dragonhpc.github.io/dragon/doc/_build/html/index.html)

## Sample tutorials
* [Data processing introduction for DragonHPC](https://dragonhpc.github.io/dragon/doc/_build/html/uses/data_processing.html)
* [AI in the loop example for DragonHPC](https://dragonhpc.github.io/dragon/doc/_build/html/cbook/ai-in-the-loop.html)

## Technical Organizers and Contributers (more to add yet)
* Pete Mendygral, HPE
* Kent Lee, HPE
* Eric Cozzi, HPE
* Christine Simpson, Argonne National Laboratory
* Davin Potts, Appliomics
* Tom Maiden, PSC
* TJ Olesky, PSC
