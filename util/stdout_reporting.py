from util.reporting import Reporting


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
