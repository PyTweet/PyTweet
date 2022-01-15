from __future__ import annotations

import threading
import random
import string
from concurrent.futures import ThreadPoolExecutor, wait
from typing import Optional, Callable, Any
from ..constants import ALL_COMPLETED

__all__ = ("Executor", "ThreadManager")


class Executor(ThreadPoolExecutor):
    def __init__(self, *args, **kwargs):
        self._session_id = kwargs.pop("session_id")
        self._thread_name = kwargs.get("thread_name")
        self._futures = []
        self._thread_name += f":session_id={self.session_id}:task_number="
        super().__init__(*args, **kwargs)

    @property
    def futures(self):
        return self._futures

    @property
    def threads(self):
        return self._threads

    @property
    def session_id(self):
        return self._session_id

    def submit(self, fn: Callable, *args: Any, **kwargs: Any):
        future = super().submit(fn, *args, **kwargs)
        self.futures.append(future)
        return future

    def clear_futures(self):
        self.futures.clear()

    def wait_for_futures(self, *, timeout: Optional[int] = None, return_when=ALL_COMPLETED, purge: bool = True):
        if not self.futures:
            return None
        result = wait(self.futures, timeout, return_when)
        if purge:
            self.clear_futures()
        return result


class ThreadManager:
    @property
    def active_threads(self) -> list:
        return threading.enumerate()

    def create_new_executor(self, *, max_workers: int = 100, thread_name: str = "", session_id: str = None) -> Executor:
        session_id = session_id or self.generate_thread_session()
        return Executor(max_workers, thread_name=thread_name, session_id=session_id)

    def get_threads(self, session_id):
        threads = []
        for t in self.active_threads:
            if session_id in t.name:
                threads.append(t)
        return threads

    def generate_thread_session(self):
        return "".join((random.sample(string.ascii_lowercase, 10)))
