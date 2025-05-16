# Polytechnique Montréal - INF8175 : Abalone's agent

Here is an intelligent agent for the board game Abalone (rules [here](https://www.youtube.com/watch?v=UUCe1ilichA)). I'm using an alpha-beta implementation enhanced with a set of weighted heuristics. Despite this rather simple implementation, I managed to achieve the third place in the intern competition of the course.

There is 2 agents available :
* random_player.py : a random player.
* my_player : my implementation of an inteligent agent.

You can find a clear description of what was expected and how to run in the Assignement PDF and a succint report of my implementation in the Report PDF (both in french).

## How to run

To run a local game with GUI :
```console
$ python main_abalone.py -t local (agent-1).py (agent-2).py
```

To run a local game human versus human :
```console
$ python main_abalone.py -t human_vs_human
```

To run a local game human versus agent :
```console
$ python main_abalone.py -t human_vs_computer (agent).py
```

