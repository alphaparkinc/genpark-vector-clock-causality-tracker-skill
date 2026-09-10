from client import VectorClock
import json

def handle_request(req):
    action = req.get("action")
    if action == "compare":
        c1 = req.get("c1", {})
        c2 = req.get("c2", {})
        return {"status": "ok", "relation": VectorClock.compare(c1, c2)}
    return {"status": "error", "message": "Unknown action"}

if __name__ == "__main__":
    print(json.dumps(handle_request({"action": "compare", "c1": {"a": 1}, "c2": {"a": 2}})))
