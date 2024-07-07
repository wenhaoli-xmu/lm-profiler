from .utils import profile_log, profile_log_once, Dummy
from pygments import console
import numpy as np
from timeit import default_timer as timer
import torch
from typing import List, Optional


class WallTime:
    regist = {}
    

    def __init__(
            self, 
            name: str, 
            cuda: Optional[int|List[int]] = None):

        self.name = name
        self.time = []
        self.cuda = cuda if isinstance(cuda, list) else [cuda]
        self.regist.update({name: self})


    @classmethod
    def get(cls, name):
        if name not in cls.regist:
            profile_log_once(f"profiler `{name}` is not registered.")
            return Dummy()
        return cls.regist[name]
    

    def _synchronize(self):
        for cuda in self.cuda:
            torch.cuda.synchronize(cuda)


    def __enter__(self):
        if self.cuda is not None:
            self._synchronize()
            self.start = timer()
        else:
            self.start = timer()


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            raise exc_type(exc_val)
        
        if self.cuda is not None:
            self._synchronize()
            self.time.append(timer() - self.start)
        else:
            self.time.append(timer() - self.start)


    def result(self, postfix="", detail=False):
        if detail:
            profile_log(
                console.colorize("green", f"{self.name}{postfix} (wall time)") 
                + f"\t{np.mean(self.time):.6f}"
                + console.colorize("green", "\tmax-") + f"{max(self.time):.6f}"
                + console.colorize("green", "\tmin-") + f"{min(self.time):.6f}"
                + console.colorize("green", "\tnum-") + f"{len(self.time)}")
        else:
            profile_log(console.colorize("green", f"{self.name}{postfix}") + f"\t{np.mean(self.time):.6f}")


    def reset(self):
        self.time = []
