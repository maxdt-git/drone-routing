*This activity has been created as part of the 42 curriculum by mde-nas.*

# Fly-in

## Description

Fly-in is a drone routing simulator. Given a map of connected zones (a
start hub, an end hub, and a set of intermediate hubs linked by
connections with movement costs and capacity limits), it computes routes
for a fleet of drones and simulates their turn-by-turn movement from the
start zone to the end zone, respecting zone/connection capacity and
zone-type movement rules, while trying to minimize the total number of
simulation turns.

## Instructions

```bash
make install   # create a virtualenv and install flake8/mypy
make run       # run the simulation on the default map (see CONFIG in the Makefile)
make debug     # run under pdb
make lint      # flake8 + mypy
make clean     # remove __pycache__ / .mypy_cache
```

To run on a specific map:

```bash
fly_venv/bin/python3 main.py maps/easy/01_linear_path.txt
```

## Algorithm & Implementation

- **`Graph`** parses the map into a `dict[str, Zone]` (`hubs`) and an
  adjacency list (`neighbors`), one entry per zone pointing to its
  neighbors as `(name, Connection, movement_cost)` tuples. Zones of type
  `blocked` are simply never linked, so pathfinding can never reach them.
- **`Pathfinding.paths`** is a Dijkstra implementation (a `heapq`-based
  priority queue, no graph library used, per the subject's constraints)
  that finds the lowest-cost route between two zones. Movement cost comes
  from the destination zone type (`normal`/`priority` = 1 turn,
  `restricted` = 2 turns). When two routes tie on cost, the one crossing
  more `priority` zones is preferred, as required by the subject.
- **`Pathfinding.find_multiple_path`** looks for several distinct
  low-cost routes: it takes the first (cheapest) path, then repeatedly
  tries excluding one connection of the already-found paths at a time
  (a simplified k-shortest-paths approach) and keeps the cheapest new
  route found, until no more distinct paths exist or `nb_paths` is
  reached. `Simulation` then distributes drones across these paths in
  round-robin.
- **`Drone`** tracks a single drone's position, its assigned path, and
  its progress along it. It also tracks multi-turn transits: a drone
  entering a `restricted` zone spends one turn "in flight" on the
  connection before actually landing, as required by the movement rules.
- **`Simulation`** is the turn engine. Each turn (`stack_list`), it lets
  every drone attempt its next move, but only if the destination
  zone/connection still has free capacity (`max_drones` /
  `max_link_capacity`, tracked live in `zone_occupancy` /
  `connection_occupancy`, reset and rebuilt every turn from ongoing
  transits via `reset_occupancy`). All moves of a turn are collected and
  joined into one output line.

## Visual Representation

`colors.py` maps each zone's `color` metadata to an ANSI escape code.
Every movement printed in the simulation output is wrapped in the color
of the zone it moves toward (or the destination zone's color, for a
departure onto a restricted connection), so the terminal output makes it
easy to visually follow which zones drones are moving through turn by
turn.

## Example

Input (`maps/easy/01_linear_path.txt`): 2 drones on a straight line
`start -> waypoint1 -> waypoint2 -> goal`.

Output:

```
D0-waypoint1
D0-waypoint2 D1-waypoint1
D0-goal D1-waypoint2
D1-goal
Total turns: 4
```

## Resources

- [Dijkstra's algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [Yen's k-shortest-paths algorithm](https://en.wikipedia.org/wiki/Yen%27s_algorithm) (inspiration for `find_multiple_path`)

**AI usage:** Claude was used throughout this project as a code-review
partner, not as a code generator — I wrote the implementation myself.
It was used to: explain the Dijkstra algorithm step by step before I
implemented it, and point out concrete logic bugs and help debug unexpected
simulation results.
