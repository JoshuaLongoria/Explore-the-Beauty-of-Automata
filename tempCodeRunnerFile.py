    for s in test_strings: 

                            # calls the Trace functions 
                            accepted, path = run_nfa_trace(nfa, s)

                            # displays status of NFA (ACCEPTED/REJECTED)
                            if accepted: 
                                # provides visual trace element ['q0', 'q1'] into "q0 -> q1"
                                trace_display = " -> ".join(path)
                                print(f"{s:<12} | ACCEPT       | {trace_display}")

                            # rejected paths show "No Path Found"
                            else:
                                print(f"{s:<12} | REJECT       | No path found")