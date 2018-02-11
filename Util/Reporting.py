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


class StdoutReporting(Reporting):
    def error(self, msg):
        print msg
        exit(0)

    def debug(self, msg):
        if self.debug_flag:
            print "DEBUG: {}".format(msg)

    def verbose(self, msg):
        if self.verbose_flag:
            print msg
