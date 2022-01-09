from __future__ import annotations

import threading
import random
import string
from concurrent.futures import ThreadPoolExecutor, wait
from ..constant import FIRST_COMPLETED

def wait_for_futures(*futures, timeout=None, return_when=FIRST_COMPLETED):
    return wait(futures, timeout, return_when)

class ThreadManager:
    @property
    def active_threads(self):
        return threading.enumerate()

    def create_new_executor(self, *,max_workers: int = 100, thread_name: str = '', session_id: str = None) -> ThreadPoolExecutor:
        session_id = session_id or self.generate_thread_session()
        thread_name += f":session_id={session_id}:task_number="
        executor = ThreadPoolExecutor(max_workers, thread_name)
        setattr(executor, "futures", [])
        return executor

    def get_threads(self, session_id):
        threads = []
        for t in self.active_threads:
            if session_id in t.name:
                threads.append(t)
        return threads

    def generate_thread_session(self):
        return "".join((random.sample(string.ascii_lowercase, 10)))