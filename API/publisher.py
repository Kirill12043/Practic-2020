import time
import random
from multiprocessing import Manager, Process
from prog.database import DataBaseConnector, DataBaseConfig


class Var:
    def __init__(self, begin_value, change_range, simul = True):
        self.value: float = float(begin_value)
        self.change_rate: float = float(change_range)
        self.simulation = simul


class PublisherClass:
    def __init__(self, db: DataBaseConnector):
        self._client = db
        self.manager = Manager()
        self._lc = Manager().Lock()
        self._var_list = self.manager.dict()
        self.wrk = None
        self.add_field = self.lock_func(self.add_field)
        self.del_field = self.lock_func(self.del_field)
        self.stop_work = self.lock_func(self.stop_work)
        self.get_var_list = self.lock_func(self.get_var_list)

    def lock_func(self, f):
        def l_decor(*args, **kwargs):
            self._lc.acquire(blocking=True)
            rt = f(*args, **kwargs)
            self._lc.release()
            return rt
        return l_decor

    def add_field(self, name, variable: Var):
        self._var_list[name] = variable

    def start_work(self):
        if self.wrk is not None:
            return False
        self.wrk = Process(target=PublisherClass.work_f, args=(self, ))
        self.wrk.start()
        return True

    def del_field(self, nm):
        if nm in self._var_list:
            self._var_list.pop(nm)
            return True
        return False

    def stop_work(self):
        if self.wrk is None:
            return False
        self.wrk.terminate()
        self.wrk.join()
        self.wrk = None
        return True

    def work_f(self):
        while True:
            lr = self._var_list.copy()
            if lr:
                vr = {}
                self._lc.acquire(blocking=True)
                for a in lr:
                    vr[a] = lr[a].value
                    if not lr[a].simulation:
                        continue
                    lr[a].value = -1 + 2 * random.randint(0, 1) + lr[a].change_rate * random.random()
                    self._var_list[a] = lr[a]
                self._lc.release()
                self._client.write(vr)
            time.sleep(1)

    def get_var_list(self):
        r_m = {}
        for a in self._var_list:
           r_m[a] = self._var_list[a].value
        return r_m


if __name__ == "__main__":
    database_config = DataBaseConfig()
    db = DataBaseConnector()
    db.set_configuration(database_config)
    db.connect()
    a = PublisherClass(db)
    a.start_work()
    a.add_field("q", Var(4, 2))
    a.add_field("z", Var(1, 3))
    print(a.get_var_list())
    while True:
        time.sleep(1)
    a.stop_work()
