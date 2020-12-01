import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_add)(
                f"user-{self.user.pk}", self.channel_name
            )

            self.send(
                text_data=json.dumps(
                    {
                        "user": self.user.username,
                    }
                )
            )

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # await login(self.scope, user)
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        self.send(text_data=json.dumps({"message": message}))

    def notification_create(self, event):
        self.send(
            text_data=json.dumps(
                {
                    "type": "notification",
                    "sender": event["sender"],
                    "recipient": event["recipient"],
                    "trigger": event["trigger"],
                }
            )
        )
