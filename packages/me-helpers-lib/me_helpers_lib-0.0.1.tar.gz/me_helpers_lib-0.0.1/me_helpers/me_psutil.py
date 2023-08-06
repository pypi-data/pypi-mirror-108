import signal
import os
import psutil


def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls


def kill_proc_children(sig=signal.SIGTERM,
                       timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig".
    "on_terminate", if specified, is a callback function which is
    called as soon as a child terminates.
    """
    try:
        parent = psutil.Process(os.getpid())
        children = parent.children(recursive=True)
        for p in children:
            p.kill()
    except:
        return 1
    return 0


def kill_proc_tree(pid, sig=signal.SIGTERM, include_parent=False,
                   timeout=None, on_terminate=None):
    """Kill a process tree (including grandchildren) with signal
    "sig" and return a (gone, still_alive) tuple.
    "on_terminate", if specified, is a callback function which is
    called as soon as a child terminates.
    """
    try:
        assert pid != os.getpid(), "won't kill myself"
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
        for p in children:
            try:
                p.send_signal(sig)
            except psutil.NoSuchProcess:
                pass
        gone, alive = psutil.wait_procs(children, timeout=timeout,
                                        callback=on_terminate)
        for p in children:
            p.kill()
    except:
        return 1
    return 0


def read_processes_running():
    processes = [(p.pid, p.info) for p in psutil.process_iter(
        ['name', 'status']) if p.info['status'] == psutil.STATUS_RUNNING]
    return processes
