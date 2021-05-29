from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = 'workwithapimedia'  # Must be replaced by your <storage_account_name>
    account_key = 'oxSy/usjeW7q6+TUG0GHbx1nbzT3K7b9L2kCtUlY3YVvKo0DfHSAopGZw6PMZxqABWRU8GVKoR/4QNxIh3CM6A=='  # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = 'workwithapimedia'  # Must be replaced by your storage_account_name
    account_key = 'oxSy/usjeW7q6+TUG0GHbx1nbzT3K7b9L2kCtUlY3YVvKo0DfHSAopGZw6PMZxqABWRU8GVKoR/4QNxIh3CM6A=='  # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
