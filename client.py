class VectorClock:
    """
    Vector Clock Causality Tracker.
    Captures happens-before relationships and identifies concurrent distributed writes.
    """
    def __init__(self, node_id):
        self.node_id = node_id
        self.clock = {node_id: 0}

    def increment(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1
        return dict(self.clock)

    def update(self, other_clock):
        for nid, val in other_clock.items():
            self.clock[nid] = max(self.clock.get(nid, 0), val)
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1
        return dict(self.clock)

    @staticmethod
    def compare(c1, c2):
        c1_leq_c2 = all(c1.get(k, 0) <= c2.get(k, 0) for k in set(c1) | set(c2))
        c2_leq_c1 = all(c2.get(k, 0) <= c1.get(k, 0) for k in set(c1) | set(c2))
        if c1_leq_c2 and c2_leq_c1:
            return 'equal'
        if c1_leq_c2:
            return 'before'
        if c2_leq_c1:
            return 'after'
        return 'concurrent'
