from collections import deque
from typing import TypedDict


class Process(TypedDict):
    pid: str
    arrival: int
    brust: int
    priority: int


ResultEntry = tuple[str, int, int]

processes: list[Process] = [
    {"pid": "P1", "arrival": 0, "brust": 7, "priority": 2},
    {"pid": "P2", "arrival": 2, "brust": 4, "priority": 1},
    {"pid": "P3", "arrival": 4, "brust": 1, "priority": 3},
    {"pid": "P4", "arrival": 5, "brust": 4, "priority": 2},
]


def priority_scheduling(processes: list[Process]) -> list[ResultEntry]:
    current_time = 0
    completed: set[str] = set()
    result: list[ResultEntry] = []

    while len(completed) < len(processes):
        ready = [
            p for p in processes
            if p["arrival"] <= current_time and p["pid"] not in completed
        ]

        if not ready:
            next_time = min(p["arrival"] for p in processes if p["pid"] not in completed)
            result.append(("IDLE", current_time, next_time))
            current_time = next_time
            continue

        p = min(ready, key=lambda p: (p["priority"], p["arrival"], p["pid"]))
        start = current_time
        end = start + p["brust"]
        result.append((p["pid"], start, end))
        current_time = end
        completed.add(p["pid"])

    return result


def round_robin(processes: list[Process], quantum: int) -> list[ResultEntry]:
    if quantum <= 0:
        raise ValueError("Quantum must be greater than zero.")

    process_list = sorted(processes, key=lambda x: (x["arrival"], x["pid"]))
    remaining: dict[str, int] = {p["pid"]: p["brust"] for p in process_list}
    queue: deque[Process] = deque()
    result: list[ResultEntry] = []
    current_time = 0
    i = 0

    while i < len(process_list) or queue:
        if not queue:
            if current_time < process_list[i]["arrival"]:
                result.append(("IDLE", current_time, process_list[i]["arrival"]))
                current_time = process_list[i]["arrival"]

        while i < len(process_list) and process_list[i]["arrival"] <= current_time:
            queue.append(process_list[i])
            i += 1

        if not queue:
            continue

        p = queue.popleft()
        run_time = min(quantum, remaining[p["pid"]])
        start = current_time
        current_time += run_time
        result.append((p["pid"], start, current_time))
        remaining[p["pid"]] -= run_time

        while i < len(process_list) and process_list[i]["arrival"] <= current_time:
            queue.append(process_list[i])
            i += 1

        if remaining[p["pid"]] > 0:
            queue.append(p)

    return result


def show_result(title: str, result: list[ResultEntry]) -> None:
    print("\n" + title)
    print("Process\tStart\tEnd")
    for item in result:
        print(item[0], item[1], item[2])

    sequence = [item[0] for item in result if item[0] != "IDLE"]
    print("Sequence", " -> ".join(sequence))


print("INPUT DATA")
print("PID AT BT Priority")
for p in processes:
    print(f"{p['pid']}\t{p['arrival']}\t{p['brust']}\t{p['priority']}")

print("\nPriority Rule: Smaller Number = Higher Priority")
priority_result = priority_scheduling(processes)
show_result("NON-PREEMPTIVE PRIORITY", priority_result)

quantum = 2
print("\nRound Robin Quantum = ", quantum)
rr_result = round_robin(processes, quantum)
show_result("ROUND ROBIN", rr_result)