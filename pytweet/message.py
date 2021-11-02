#{'event': {'type': 'message_create', 'id': '1455541764257894410', 'created_timestamp': '1635863173914', 'message_create': {'target': {'recipient_id': '1382006704171196419'}, 'sender_id': '1445987330582405122', 'message_data': {'text': 'Hello Le World', 'entities': {'hashtags': [], 'symbols': [], 'user_mentions': [], 'urls': []}}}}}
from typing import Dict, Any

class Message:
    def __init__(self, data: Dict[str, Any]):
        self.payload=data