import re


class Pattern:
    def __init__(self, patterns):
        self.last_match = None
        self.patterns = patterns

    def load_with_file(self, pattern_file):
        with open(pattern_file) as f:
            self.patterns = f.read().split('\n')

    def matches(self, subject):
        for pattern in self.patterns:
            if len(pattern) == 0:
                continue

            try:
                p = re.compile(pattern)
                if p.match(subject):
                    self.last_match = pattern
                    return True
            except:
                continue

        return False

    def not_empty(self):
        return len(self.patterns)

    def get_last_match(self):
        return self.last_match

