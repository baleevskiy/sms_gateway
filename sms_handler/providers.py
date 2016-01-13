import httplib
import urllib
import urllib2
from django.conf import settings
import logging
import json
from sms_handler.models import Provider

log = logging.getLogger(__name__)


class SmsProvider(object):
    """
    base class which just sends message to a number.
    """
    # TODO: ABC subclass
    def send(self, message):
        """
        :param message: Message
        :rtype : ProviderResponse
        """
        # do whatever you need here
        result = self._send(message)
        if not isinstance(result, ProviderResponse):
            raise Exception('Bad response from provider')

        return result

    def _send(self, message):
        """

        :param message: Message
        :return: ProviderResponse
        """
        raise NotImplemented


class SmsProvider1(SmsProvider):
    def _send(self, message):

        try:
            url_2 = settings.PROVIDERS['provider1']['url']
            values = dict(number=message.number, message=message.body)
            data = urllib.urlencode(values)
            request = urllib2.Request(url_2, data)
            response = urllib2.urlopen(request)
            content = json.loads(response.read())
        except urllib2.HTTPError, e:
            log.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            log.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            log.error('HTTPException')
        except Exception:
            import traceback
            log.error('generic exception: ' + traceback.format_exc())

        return ProviderResponse(ProviderResponseCodes.SUCCESS, data=content)


class SmsProvider2(SmsProvider):
    def _send(self, message):

        try:
            url_2 = settings.PROVIDERS['provider2']['url']
            values = dict(number=message.number, message=message.body)
            data = urllib.urlencode(values)
            request = urllib2.Request(url_2, data)
            response = urllib2.urlopen(request)
            content = json.loads(response.read())
        except urllib2.HTTPError, e:
            log.error('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            log.error('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            log.error('HTTPException')
        except Exception:
            import traceback
            log.error('generic exception: ' + traceback.format_exc())

        return ProviderResponse(ProviderResponseCodes.SUCCESS, data=content)


class ProviderFactory(object):
    @staticmethod
    def get_provider(provider_class_name=None):
        """
        :param provider_class_name: Class name of required provider
        :rtype : SmsProvider
        """
        try:
            provider_record = Provider.objects.filter(class_name=provider_class_name,
                                                      enabled=True).get()
            return globals()[provider_record.class_name]()

        except Provider.DoesNotExist:
            log.error()
            # return defaultProvider()


class ProviderResponse(object):
    """
    unified way to process
    """

    def __init__(self, error_code=None, data=None):
        if error_code is None:
            raise Exception('error code is None')

        self.__error_code = error_code
        self.__data = data

    @property
    def error_code(self):
        return self.__error_code

    @property
    def data(self):
        return self.data


class ProviderResponseCodes(object):
    ERROR_CONNECT_FAILED = '000'
    ERROR_BALANCE_LOW = '001'
    ERROR_CUSTOMER_UNREACHABLE = '002'
    ERROR_CUSTOMER_BLACKLISTED = '003'
    SUCCESS = '100'
