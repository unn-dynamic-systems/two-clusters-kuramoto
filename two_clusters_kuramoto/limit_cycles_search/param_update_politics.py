import os
from clog import log_str
from tqdm import tqdm

class Politics:
    def __init__(self, h, inside_args_area, args_updater, h_limit=1e-3, bar_title="", Reverse=False, color='okblue'):
        self.bar_title = bar_title
        self.h = h
        self.h_limit = h_limit
        self.inside_args_area = inside_args_area
        self.args_updater = args_updater
        self.Reverse = Reverse
        self.color = color
        self.pbar = None

    def update(self, *args, fail=False):

        if fail:
            if self.h < self.h_limit:
                return False, ()

            args = self.args_updater(*args, self.h, not self.Reverse)
            self.h /= 2
            args = self.args_updater(*args, self.h, self.Reverse)
            return True, args

        if not self.pbar:
            self.pbar = tqdm(total=self.get_approx_total(args))


        args = self.args_updater(*args, self.h, self.Reverse)
        if not self.inside_args_area(*args):
            return False, ()

        
        self.pbar.set_description(log_str(f"{self.bar_title}, pid: {os.getpid()}", self.color))
        self.pbar.update(self.h); print("")
        return True, args
    
    def get_approx_total(self, args):
        total = 0
        while self.inside_args_area(*args):
            args = self.args_updater(*args, self.h, self.Reverse)
            total += self.h
        return round(total, 2)
