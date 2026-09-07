"""
MCP Server for Vector Clock Causality Tracker Skill
"""

import json
import sys
from client import CausalTracker

tracker = CausalTracker()

def handle_call(name: str, args: dict) -> dict:
    if name == "record_event":
        nid = args.get("node_id")
        action = args.get("action", "op")
        ev = tracker.record_local_event(nid, action)
        return ev.to_dict()
    elif name == "check_causality":
        ev1 = args.get("event1")
        ev2 = args.get("event2")
        rel = tracker.analyze_concurrency(ev1, ev2)
        return {"event1": ev1, "event2": ev2, "relation": rel}
    return {"error": f"Unknown tool: {name}"}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        res = handle_call(req.get("method"), req.get("params", {}))
        sys.stdout.write(json.dumps(res) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
