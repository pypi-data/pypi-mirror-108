import requests
import json
from urllib.parse import urlencode

from django.conf import settings

from dnoticias_services.utils.request import get_headers
from .base import BasePaymentRequest


class GetPaymentProviders(BasePaymentRequest):
    """
    Gets all the active payment providers from dnoticias-payments.
    """
    def __call__(self, item_uuid, request, api_key=None):
        _api_key = api_key or self.api_key
        query_params = urlencode(request.query_params)
        query_params = '?' + query_params if query_params else ''

        response = requests.get(
            settings.PAYMENT_PROVIDERS_SELECT2VIEW_API_URL.format(item_uuid) + query_params,
            headers=get_headers(_api_key),
        )

        response.raise_for_status()

        return response


get_payment_providers = GetPaymentProviders()


__all__ = ("get_payment_providers", )
