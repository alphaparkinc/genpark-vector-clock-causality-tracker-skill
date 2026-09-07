"""
Demonstration of Vector Clock Causality Tracker Skill
"""

from client import CausalTracker

def main():
    print("=== Tracing Distributed Multi-Agent Causal Events ===")
    tracker = CausalTracker()

    # Agent A performs local task
    ev_a1 = tracker.record_local_event("agent_A", "generate_plan")
    print(f"Event A1: {ev_a1.action} -> Clock: {ev_a1.clock}")

    # Agent B performs independent concurrent task
    ev_b1 = tracker.record_local_event("agent_B", "fetch_telemetry")
    print(f"Event B1: {ev_b1.action} -> Clock: {ev_b1.clock}")

    # Check relation between A1 and B1 (concurrent)
    relation = tracker.analyze_concurrency(ev_a1.event_id, ev_b1.event_id)
    print(f"Causal relation between A1 and B1: {relation}")
    assert relation == "CONCURRENT"

    # Agent A sends message to Agent B
    send_ev, msg_clock = tracker.send_message("agent_A", "dispatch_subtask")
    print(f"Event A2 (Send): Clock: {send_ev.clock}")

    # Agent B receives message
    recv_ev = tracker.receive_message("agent_B", msg_clock, "dispatch_subtask")
    print(f"Event B2 (Recv): Clock: {recv_ev.clock}")

    # Verify causality: A2 happened before B2
    relation_msg = tracker.analyze_concurrency(send_ev.event_id, recv_ev.event_id)
    print(f"Causal relation between Send (A2) and Recv (B2): {relation_msg}")
    assert relation_msg == "HAPPENED_BEFORE"

    print("Vector Clock Causality Tracker Verification PASS!")

if __name__ == "__main__":
    main()
