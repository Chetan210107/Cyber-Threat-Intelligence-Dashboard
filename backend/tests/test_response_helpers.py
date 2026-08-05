from backend.utils.responses import api_response


def test_api_response_includes_expected_sections():
    payload = api_response(True, "ok", {"value": 1}, {"field": "invalid"})

    assert payload["success"] is True
    assert payload["message"] == "ok"
    assert payload["data"] == {"value": 1}
    assert payload["errors"] == {"field": "invalid"}
