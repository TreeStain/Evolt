from datetime import datetime


# TODO: add timestamps to error and debug messages
# TODO: save logs to file
class Messenger(object):
    def __init__(self, file, show_debug=True, show_error=True, save_debug=False, save_error=False, save_time=10000):
        self.show_debug = show_debug
        self.show_error = show_error
        self.save_debug = save_debug
        self.save_error = save_error
        self.debug_to_save = []
        self.error_to_save = []
        self.last_save_time_ms = 0
        self.save_time = save_time
        self.file = open(file, "w+")

    def log_debug(self, msg):
        msg_show = str(datetime.now().time()) + ":" + msg
        print(msg_show)
        if self.save_debug:
            self.debug_to_save += [msg_show]

    def log_error(self, msg):
        msg_show = str(datetime.now().time()) + ":" + msg
        print(msg_show)
        if self.save_error:
            self.error_to_save += [msg_show]

    def save_log(self):
        self.file.writelines(self.error_to_save)
        self.file.writelines(self.debug_to_save)

    def timed_save_log(self, ms_current_time):
        if ms_current_time >= self.last_save_time_ms + self.save_time:
            self.last_save_time_ms = ms_current_time
            self.file.writelines(self.error_to_save)
            self.file.writelines(self.debug_to_save)
