from typing import TypedDict

class Process(TypedDict):
    pid: str
    arrival: int
    burst: int

Interval = tuple[str, int, int]

processes: list[Process] = [
    {"pid":"p1","arrival":0,"burst":7},
    {"pid":"p2","arrival":2,"burst":4},
    {"pid":"p3","arrival":4,"burst":1},
    {"pid":"p4","arrival":5,"burst":4},
]

def fcfs(process_list: list[Process]) -> list[Interval]:
    current_time = 0
    intervals: list[Interval] = []

    ordered = sorted(
        process_list,
        key=lambda p: (p["arrival"],p["pid"])
    )

    for process in ordered:
        if current_time < process["arrival"]:
            intervals.append(("IDLE",current_time,process["arrival"]))
            current_time = process["arrival"]

        start = current_time
        end = start + process["burst"]
        intervals.append((process["pid"],start,end))
        current_time = end 

    return intervals 


def sjf(process_list: list[Process]) -> list[Interval]:
    remaining = process_list.copy()
    current_time = 0
    intervals: list[Interval] = []

    while remaining:
        ready = [p for p in remaining if p["arrival"] <= current_time]

        if not ready:
            next_arrival = min(p["arrival"] for p in remaining)
            intervals.append(("IDLE", current_time, next_arrival))
            current_time = next_arrival
            continue

        process = min(ready, key=lambda p: (p["burst"], p["arrival"], p["pid"]))

        start = current_time
        end = start + process["burst"]
        intervals.append((process["pid"], start, end))
        current_time = end
        remaining.remove(process)

    return intervals



def show_result(title: str, intervals: list[Interval]) -> None:
    print("\n" + title)
    print("Process  Start  End")

    sequence: list[str] = []

    for pid, start, end in intervals:
        print(f"{pid:<9}{start:<7}{end}")

        if pid != "IDLE":
            sequence.append(pid)

    print("\nExecution Sequence: "," -> ".join(sequence))


print("INPUT PROCESSES")
print("PID  AT  BT")

for p in processes:
    print(f"{p['pid']:<5}{p['arrival']:<4}{p['burst']}")

show_result("FCFS SCHEDULING", fcfs(processes))
show_result("SJF SCHEDULING", sjf(processes))
