from typing import NewType

from nats.js.kv import KeyValue


MailingKeyValueStorage = NewType("MailingKeyValueStorage", KeyValue)
MailingId = NewType("MailingId", int)