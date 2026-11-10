"""Educational CPU scheduling simulator. It does not change the host OS scheduler."""

def fcfs(jobs):
    time = 0
    output = []
    for job in sorted(jobs, key=lambda x: x["arrival"]):
        time = max(time, job["arrival"])
        start = time
        time += job["burst"]
        output.append(_row(job, start, time))
    return output

def sjf(jobs):
    pending = [dict(j) for j in jobs]
    time, output = 0, []
    while pending:
        ready = [j for j in pending if j["arrival"] <= time]
        if not ready:
            time = min(j["arrival"] for j in pending)
            ready = [j for j in pending if j["arrival"] <= time]
        job = min(ready, key=lambda x: x["burst"])
        pending.remove(job)
        start = time
        time += job["burst"]
        output.append(_row(job, start, time))
    return output

def round_robin(jobs, quantum=2):
    pending = sorted([dict(j, remaining=j["burst"]) for j in jobs], key=lambda x: x["arrival"])
    time, index, ready, completion = 0, 0, [], {}
    while index < len(pending) or ready:
        while index < len(pending) and pending[index]["arrival"] <= time:
            ready.append(pending[index]); index += 1
        if not ready:
            time = pending[index]["arrival"]
            continue
        job = ready.pop(0)
        run = min(quantum, job["remaining"])
        time += run
        job["remaining"] -= run
        while index < len(pending) and pending[index]["arrival"] <= time:
            ready.append(pending[index]); index += 1
        if job["remaining"]:
            ready.append(job)
        else:
            completion[job["pid"]] = time
    return [{
        "pid": j["pid"],
        "completion": completion[j["pid"]],
        "turnaround": completion[j["pid"]] - j["arrival"],
        "waiting": completion[j["pid"]] - j["arrival"] - j["burst"]
    } for j in pending]

def _row(job, start, finish):
    turnaround = finish - job["arrival"]
    return {
        "pid": job["pid"], "start": start, "completion": finish,
        "turnaround": turnaround, "waiting": turnaround - job["burst"]
    }
