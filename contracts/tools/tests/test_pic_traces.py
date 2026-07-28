from pic_contracts.traces import _step_sources

def test_step_sources_empty_trace():
    assert _step_sources({}) == []
    assert _step_sources({"steps": []}) == []

def test_step_sources_missing_keys():
    trace = {
        "steps": [
            {},  # Missing both
            {"stepId": "step1"},  # Missing sourceRefs
            {"sourceRefs": ["ref1", "ref2"]}  # Missing stepId
        ]
    }
    expected = [
        ("", ()),
        ("step1", ()),
        ("", ("ref1", "ref2"))
    ]
    assert _step_sources(trace) == expected

def test_step_sources_happy_path():
    trace = {
        "steps": [
            {"stepId": "step1", "sourceRefs": ["ref1", "ref2"]},
            {"stepId": "step2", "sourceRefs": ["ref3"]}
        ]
    }
    expected = [
        ("step1", ("ref1", "ref2")),
        ("step2", ("ref3",))
    ]
    assert _step_sources(trace) == expected
