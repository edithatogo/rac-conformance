🎯 **What:** The function `_step_path` in `contracts/tools/src/pic_contracts/traces.py` was missing test coverage. This function computes a trace path by iterating through the steps and parameter versions, which is crucial for evaluating trace equivalence accurately.

📊 **Coverage:** We introduced a new set of tests for this specific function in `contracts/tools/tests/test_pic_traces_schema.py`. The tests cover multiple scenarios:
- Empty trace dictionary.
- Trace with an empty steps list.
- Trace step with no parameter versions.
- Trace step with standard ID and specific parameter version ID alongside an effective-from date.

✨ **Result:** The tests effectively confirm the function correctly builds and returns the list of steps paths correctly. Test coverage and reliability of trace equivalence functionality have increased.
