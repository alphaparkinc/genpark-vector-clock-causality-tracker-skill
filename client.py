"""
Vector Clock Causality Tracker Skill Client
Pure Python Standard Library implementation of Vector Clocks (Fidge & Mattern).
Tracks causal relationships between asynchronous agent events, determines happens-before (->),
identifies concurrent operations (||), and detects causal race conditions.
"""

from typing import List, Dict, Any, Tuple, Optional, Set
import copy


class VectorClock:
    def __init__(self, node_id: str, initial_clock: Optional[Dict[str, int]] = None):
        self.node_id = node_id
        self.clock: Dict[str, int] = copy.deepcopy(initial_clock) if initial_clock else {node_id: 0}

    def increment(self) -> Dict[str, int]:
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1
        return copy.deepcopy(self.clock)

    def merge(self, received_clock: Dict[str, int]):
        for nid, count in received_clock.items():
            self.clock[nid] = max(self.clock.get(nid, 0), count)
        self.increment()

    def compare(self, other_clock: Dict[str, int]) -> str:
        """
        Compare self with other_clock:
        - "HAPPENED_BEFORE": self -> other
        - "HAPPENED_AFTER": other -> self
        - "CONCURRENT": self || other
        - "EQUAL": self == other
        """
        all_keys = set(self.clock.keys()).union(set(other_clock.keys()))
        self_le_other = True
        other_le_self = True

        for k in all_keys:
            v_self = self.clock.get(k, 0)
            v_other = other_clock.get(k, 0)
            if v_self > v_other:
                self_le_other = False
            if v_other > v_self:
                other_le_self = False

        if self_le_other and other_le_self:
            return "EQUAL"
        elif self_le_other:
            return "HAPPENED_BEFORE"
        elif other_le_self:
            return "HAPPENED_AFTER"
        else:
            return "CONCURRENT"


class CausalEvent:
    def __init__(self, event_id: str, node_id: str, action: str, clock: Dict[str, int]):
        self.event_id = event_id
        self.node_id = node_id
        self.action = action
        self.clock = clock

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "node_id": self.node_id,
            "action": self.action,
            "clock": self.clock
        }


class CausalTracker:
    def __init__(self):
        self.clocks: Dict[str, VectorClock] = {}
        self.events: List[CausalEvent] = []

    def get_or_create_node(self, node_id: str) -> VectorClock:
        if node_id not in self.clocks:
            self.clocks[node_id] = VectorClock(node_id)
        return self.clocks[node_id]

    def record_local_event(self, node_id: str, action: str) -> CausalEvent:
        vc = self.get_or_create_node(node_id)
        clk = vc.increment()
        ev = CausalEvent(f"ev_{len(self.events) + 1:04d}", node_id, action, clk)
        self.events.append(ev)
        return ev

    def send_message(self, sender_id: str, action: str) -> Tuple[CausalEvent, Dict[str, int]]:
        ev = self.record_local_event(sender_id, f"SEND: {action}")
        return ev, copy.deepcopy(ev.clock)

    def receive_message(self, receiver_id: str, sender_clock: Dict[str, int], action: str) -> CausalEvent:
        vc = self.get_or_create_node(receiver_id)
        vc.merge(sender_clock)
        ev = CausalEvent(f"ev_{len(self.events) + 1:04d}", receiver_id, f"RECV: {action}", copy.deepcopy(vc.clock))
        self.events.append(ev)
        return ev

    def analyze_concurrency(self, ev1_id: str, ev2_id: str) -> str:
        ev1 = next((e for e in self.events if e.event_id == ev1_id), None)
        ev2 = next((e for e in self.events if e.event_id == ev2_id), None)
        if not ev1 or not ev2:
            return "NOT_FOUND"

        vc = VectorClock("temp", ev1.clock)
        return vc.compare(ev2.clock)
