from urllib3.util.retry import Retry


http_retry_strategy = Retry(
    total=3,
    backoff_factor=0.2,
    allowed_methods=["HEAD", "GET", "OPTIONS"],
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=True,
    redirect=3,
    raise_on_redirect=True,
)
http_retry_strategy.BACKOFF_MAX = 2
