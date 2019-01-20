# -*- coding: utf-8 -*-
# Copyright (c) 2019 PGkids Laboratory

from threading import Thread,Event
from time import sleep,clock

class RobotJob():
    __thread    = None
    __event     = None
    __active    = False
    
    def __init__(self, proc):
        def fn():
            proc(self)
            self.__active = False
            self.__event.set()
        self.__thrproc = fn

    def __call__(self):
        self.start()
        self.join()
        
    def _get_event(self):
        return self.__event

    # Safe Sleep
    def _safe_sleep(self, sec):
        if not self._active: return False
        clock_entered = clock()
        while True:
            if not self.__event.wait(sec):
                # Timed out
                return self.__active
            if not self.__active:
                return False
            self.__event.clear()
            cur_clock = clock()
            if (cur_clock - clock_entered) >= sec:
                return True
            sec -= cur_clock - clock_entered
            clock_entered = cur_clock

    def _wait_for_event(self):
        self.__event.wait(None)
        return self.__active
    
    def is_active(self):
        return self.__active
    
    def __start(self, join, event):
        if not self.__active:
            self.__active = True
            self.__event = event
            self.__thread = Thread(target=self.__thrproc)
            self.__thread.start()
            if join: self.join()
            return self
        else:
            raise(RuntimeError)

    def start(self, join=False):
        return self.__start(join, Event())

    def _start_with(self, event):
        return self.__start(False, event)
    
    def join(self, timeout=None):
        if self.__active:
            self.__thread.join(timeout)
            if self.__thread.is_alive():
                return False
            else:
                self.__thread = None
                self.__active = False
                self.__event.clear()
                return True
        else:
            return True
    def cancel(self):
        if self.__active:
            self.__active = False
            self.__event.set()

def mkjob(proc, *args) -> RobotJob:
    return RobotJob(lambda job:proc(*args))

def parjob(*jobs) -> RobotJob:
    def fn(master_job):
        ev = master_job._get_event()
        for job in jobs:
            job._start_with(ev)
        while master_job.is_active():
            still_alive = False
            for job in jobs:
                if job.is_active():
                    still_alive = True
            if still_alive:
                if not master_job._wait_for_event():
                    for job in jobs:
                        if not job.is_active():
                            job.cancel()
            else:
                break
        # join all jobs
        for job in jobs:
            job.join()

    return RobotJob(fn)

def ordjob(*jobs) -> RobotJob:
    def fn(master_job):
        ev = master_job._get_event()
        for job in jobs:
            job._start_with(ev)
            # master_jobがキャンセルされた場合
            if not master_job._wait_for_event():
                job.cancel()
            job.join()
            if not master_job.is_active():
                break

    return RobotJob(fn)

def loopjob(job) -> RobotJob:
    def fn(master_job):
        ev = master_job._get_event()
        while master_job.is_active():
            job._start_with(ev)
            if not master_job._wait_for_event():
                job.cancel()
            job.join()
            
    return RobotJob(fn)