from typing import List, Union


class MessageAttributes:
    def __init__(self):
        self.string_value: str = ""
        self.binary_value: bytes = b'bytes'
        self.string_list_values: List[str]
        self.binary_list_values: List[b'bytes']
        self.data_type: str


class SQSMessageConfig(object):
    def __init__(self, message_body: str,
                 message_group_id: str,
                 message_attributes: Union[MessageAttributes, None],
                 message_deduplication_id: str,
                 delay_seconds: int = 123):
        self.message_body: str = message_body
        self.message_group_id = message_group_id
        self.message_deduplication_id = message_deduplication_id
        self.message_attributes = message_attributes
        self.delay_seconds = delay_seconds
