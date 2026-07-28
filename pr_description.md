🎯 **What:** The testing gap addressed
The `_parameters_by_id` function in `contracts/tools/src/pic_contracts/diff.py` lacked explicit test coverage. This function takes a document dictionary and returns a dictionary mapping parameter IDs to parameter dictionaries.

📊 **Coverage:** What scenarios are now tested
1. **Happy Path:** Correctly mapping multiple parameters by their IDs.
2. **Missing Key:** Handling a document without a "parameters" key (returns an empty dictionary).
3. **Empty List:** Handling a document with an empty "parameters" list (returns an empty dictionary).
4. **Missing ID:** Ensuring a `KeyError` is raised if a parameter dictionary is missing the "id" key.

✨ **Result:** The improvement in test coverage
The `_parameters_by_id` function is now fully covered by tests, ensuring its behavior remains correct and deterministic. This prevents regressions if the way parameter IDs are extracted or mapped is changed in the future.
