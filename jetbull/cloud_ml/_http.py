from google.cloud import _http
from jetbull.cloud_ml import __version__


_CLIENT_INFO = _http.CLIENT_INFO_TEMPLATE.format(__version__)


class Connection(_http.JSONConnection):
    API_BASE_URL = "https://ml.googleapis.com"
    API_VERSION = "v1"
    API_URL_TEMPLATE = "{api_base_url}/{api_version}{path}"
    _EXTRA_HEADERS = {
        _http.CLIENT_INFO_HEADER: _CLIENT_INFO,
    }
