from client import VectorClock

def main():
    print("=== Testing Vector Clock Causality Tracker ===")
    v_a = VectorClock("NodeA")
    v_b = VectorClock("NodeB")
    
    ca1 = v_a.increment() # {NodeA: 1}
    cb1 = v_b.increment() # {NodeB: 1}
    
    cmp1 = VectorClock.compare(ca1, cb1)
    print(f"Compare ca1 vs cb1: {cmp1} (expected concurrent)")
    assert cmp1 == "concurrent"
    
    ca2 = v_a.update(cb1) # {NodeA: 2, NodeB: 1}
    cmp2 = VectorClock.compare(cb1, ca2)
    print(f"Compare cb1 vs ca2: {cmp2} (expected before)")
    assert cmp2 == "before"
    print("=== Vector Clock Verification Complete ===")

if __name__ == "__main__":
    main()
