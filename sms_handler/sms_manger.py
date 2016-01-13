import logging
from sms_handler.models import MessageLog, Message
from sms_handler.providers import ProviderFactory

log = logging.getLogger(__name__)


class SmsManager(object):
    """
    This is a gateway itself.
    """
    @staticmethod
    def send_message(body=None, phone_number=None, provider_class_name=None, ):
        """

        :param message: str Sms body
        :param phone_number: str Recipient phone number
        :param provider_class_name: str Class name of required SmsProvider
        :return: ProviderResponse
        """
        if provider_class_name is None:
            raise Exception('handler class name is required')

        sender = ProviderFactory.get_provider(provider_class_name=provider_class_name)
        message = Message(body=body,
                          phone_number=phone_number)
        message.save()
        try:
            # do whatever you need before you send the message
            response = sender.send(message)
            message_log = MessageLog()
            message_log.message = message
            message_log.response_data = response.data
            message_log.save()
            return response
        except Exception:
            log.error('handle it')

    def send_async(self):
        raise NotImplemented


