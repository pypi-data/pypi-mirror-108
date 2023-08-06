
import json
import os
from pythonapm.util import current_milli_time, is_valid_rescode
from pythonapm.constants import manage_agent, delete_agent, shutdown

class Instanceinfo:

    def __init__(self):
        self.last_reported = None
        self.status = manage_agent
        self.modified_time = current_milli_time()

    def update_status(self, rescode):
        self.update_last_reported()
        if is_valid_rescode(rescode) is not True:
            return

        self.status = rescode
        if self.status == delete_agent:
            self.status = shutdown


    def get_status(self):
        return self.status

    def update_last_reported(self):
        self.last_reported = current_milli_time()

    def get_modiefied_time(self):
        return self.modified_time

    def get_retry_counter(self):
        return self.retry_counter

    def get_last_reported(self):
        return self.last_reported
    


