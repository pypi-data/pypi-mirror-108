def begin_timer_raw(desc, pid):
    from toggl.api import TimeEntry
    from pendulum import now
    if pid >= 0:
        cur = TimeEntry.start_and_save(start=now(), description=desc, pid=pid)
    else:
        cur = TimeEntry.start_and_save(start=now(), pid=pid)
    cur.save()
    return cur

def get_timers(days):
    from toggl.api import TimeEntry
    from pendulum import now
    entries = TimeEntry.objects.all_from_reports(start=now().subtract(days=days), stop=now())
    seen = set()
    for i,e in enumerate(entries):
        if e.description not in seen:
            seen.add(e.description)
            yield { 'desc': e.description, 'pid': int(e.pid or -1) }

