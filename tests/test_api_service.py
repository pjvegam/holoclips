from datetime import datetime

import pytest
import requests

import api_service
from api_service import HolodexApiError, HolodexApiService


def response(status, text="[]"):
    result = requests.Response()
    result.status_code = status
    result._content = text.encode()
    return result


@pytest.fixture
def fake_get(monkeypatch):
    """Replace requests.get with a single scripted result and record the call."""

    def install(result):
        calls = []

        def fake(url, headers, params, timeout):
            calls.append({"url": url, "headers": headers, "params": params})
            if isinstance(result, Exception):
                raise result
            return result

        monkeypatch.setattr(api_service.requests, "get", fake)
        return calls

    return install


def get_clips(service=None, **kwargs):
    service = service or HolodexApiService("secret")
    return service.get_clips(datetime(2026, 1, 1), datetime(2026, 1, 2), **kwargs)


def test_sends_documented_params_and_key_in_header(fake_get):
    calls = fake_get(response(200, '[{"id": "a"}]'))
    assert get_clips() == [{"id": "a"}]

    call = calls[0]
    assert call["headers"]["X-APIKEY"] == "secret"
    assert "secret" not in call["params"].values()
    assert call["params"]["limit"] == 50
    assert call["params"]["offset"] == 0
    assert call["params"]["type"] == "clip"
    assert call["params"]["lang"] == "en,es"
    assert call["params"]["include"] == "sources,mentions,refers"
    assert call["params"]["from"] == "2026-01-01T00:00:00"
    assert call["params"]["to"] == "2026-01-02T00:00:00"


def test_default_limit_respects_documented_maximum():
    assert HolodexApiService.MAX_LIMIT <= 50


@pytest.mark.parametrize("status", [400, 403, 429, 500, 503])
def test_error_status_raises_with_cause(fake_get, status):
    fake_get(response(status, "algo fue mal"))
    with pytest.raises(HolodexApiError, match=f"{status} - algo fue mal"):
        get_clips()


@pytest.mark.parametrize("error", [requests.Timeout("lento"), requests.ConnectionError("red")])
def test_network_errors_raise_api_error(fake_get, error):
    fake_get(error)
    with pytest.raises(HolodexApiError):
        get_clips()
