from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

from discussion.models import DiscussionPost

class TestConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name="test_consumer"
        self.room_group_name="test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
           self.room_group_name, self.channel_name
            )
        self.accept()
        # self.send(json.dumps({"type": "websocket.accept"}))

    def receive(self,text_data):
        if text_data == 'notification_seen':
            DiscussionPost.objects.all().update(is_seen='True')


    def disconnect(self, close_code):
        #Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,self.channel_name
        )

    def send_notification(self,event):
        notification_data=json.loads(event.get('value'))
        self.send(text_data=json.dumps({'data':notification_data}))
