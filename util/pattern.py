import re


class Pattern(object):
    def __init__(self, patterns):
        self.last_match = None
        self.patterns = patterns

    def load_with_file(self, pattern_file):
        with open(pattern_file) as f_p:
            self.patterns = f_p.read().split('\n')

    def matches(self, subject):
        for pattern in self.patterns:
            if not pattern:
                continue

            try:
                regexp = re.compile(pattern)
                if regexp.match(subject):
                    self.last_match = pattern
                    return True
            except ValueError:
                continue

        return False

    def not_empty(self):
        return len(self.patterns)

    def get_last_match(self):
        return self.last_match
