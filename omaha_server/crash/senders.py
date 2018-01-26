import logging

from django.conf import settings

from raven import Client
from celery import signature

from omaha_server.utils import add_extra_to_log_message


class BaseSender(object):
    name = None
    client = None

    def send(self, message, extra={}, tags={}, data={}, crash_obj=None):
        pass


class SentrySender(BaseSender):
    name="Sentry"

    def __init__(self):
        self.client = Client(
            getattr(settings, 'RAVEN_DSN_STACKTRACE', None),
            name=getattr(settings, 'HOST_NAME', None),
            release=getattr(settings, 'APP_VERSION', None)
        )

    def send(self, message, extra={}, tags={}, data={}, crash_obj=None):
        event_id = self.client.capture(
            'raven.events.Message',
            message=message,
            extra=extra,
            tags=tags,
            data=data
        )
        signature("tasks.get_sentry_link", args=(crash_obj.pk, event_id)).apply_async(queue='private', countdown=1)


class ELKSender(BaseSender):
    name="ELK"
    handler = None

    def send(self, message, extra={}, tags={}, data={}, crash_obj=None):
        logger = logging.getLogger('crashes')
        extra.update(tags)
        # sentry.interfaces.Exception
        extra.update(data)
        extra.update({
            'signature': message
        })
        logger.info(add_extra_to_log_message(message, extra=extra))

senders_dict = {
    "Sentry": SentrySender,
    "ELK": ELKSender,
}


def get_sender(tracker_name=None):
    if not tracker_name:
        tracker_name = getattr(settings, 'CRASH_TRACKER', 'Sentry')
    try:
        sender_class = senders_dict[tracker_name]
    except KeyError:
        raise KeyError("Unknown tracker, use one of %s" % senders_dict.keys())
    return sender_class()