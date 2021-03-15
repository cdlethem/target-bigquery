from singer.statediff import paths, diff, Add, Change, Remove


class State(dict):

    def __init__(self, **kwargs):
        super(State, self).__init__(**kwargs)

    def __missing__(self, key):
        self[key] = {}
        return self[key]

    def merge(self, state):
        d = diff(self, state)
        for m in d:
            t = self
            if isinstance(m, Add) or isinstance(m, Change):
                for i, p in enumerate(m.path):
                    if i == len(m.path)-1:
                        t[p] = m.newval
                    else:
                        if p not in t: t[p] = {}
                        t = t[p]

            elif isinstance(m, Remove):
                pass
