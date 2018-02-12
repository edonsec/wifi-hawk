class Reporting:
    def __init__(self, verbose=False, debug=False):
        self.verbose_flag = verbose
        self.debug_flag = debug

    def error(self, msg):
        pass

    def debug(self, msg):
        pass

    def verbose(self, msg):
        pass


