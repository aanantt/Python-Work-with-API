from django.conf import settings
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = settings.AZURE_ACCOUNT_NAME
    account_key = settings.AZURE_STORAGE_KEY
    azure_container = settings.AZURE_MEDIA_CONTAINER
    expiration_secs = None
    overwrite_files = True

    # DefaultEndpointsProtocol=https;AccountName=workwithapimedia;AccountKey=43rBfSussln03p5wJVtfgHGvlBe/QeCm3aznFY3CyrtkQeFzIupfMBrkHVpE90vQawk+LmlBbaCSZKuhEatGYg==;EndpointSuffix=core.windows.net
