import json
import logging
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings

logger = logging.getLogger(__name__)

VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
# Cloudflare's published test site keys (always pass, always block, forced challenge).
TEST_SITE_KEYS = {
    "1x00000000000000000000AA",
    "2x00000000000000000000AB",
    "3x00000000000000000000FF",
}
RESPONSE_FIELD = "cf-turnstile-response"


def verify(token, remote_ip=None):
    """Ask Cloudflare whether a Turnstile token is valid. Any failure counts as not verified."""
    if not token:
        return False
    data = {"secret": settings.TURNSTILE_SECRET_KEY, "response": token}
    if remote_ip:
        data["remoteip"] = remote_ip
    request = Request(VERIFY_URL, data=urlencode(data).encode(), method="POST")
    try:
        # VERIFY_URL is a constant https:// address, so no file:// or custom scheme can reach it.
        with urlopen(request, timeout=8) as response:  # nosec B310
            result = json.load(response)
    except (URLError, TimeoutError, ValueError):
        logger.exception("Turnstile verification request failed")
        return False
    if not result.get("success"):
        logger.info("Turnstile rejected a token: %s", result.get("error-codes"))
    return bool(result.get("success"))
