import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Messages, User, Chat
from datetime import  datetime

class PersonalChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    my_id = self.scope['url_route']['kwargs']['my_id']
    other_user_id = self.scope['url_route']['kwargs']['id']
    if int(my_id) > int(other_user_id):
      self.room_name = f'{my_id}-{other_user_id}'
    else:
      self.room_name = f'{other_user_id}-{my_id}'

    self.room_group_name = 'chat_%s' % self.room_name

    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()


  async def receive(self, text_data=None, bytes_data=None):
    data = json.loads(text_data)
    message = data['message']
    username = data['username']

    await self.save_message(username, self.room_group_name, message)
    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'message': message,
        'username': username,
      }
    )


  async def chat_message(self, event):
    message = event['message']
    username = event['username']

    await self.send(text_data=json.dumps({
      'message': message,
      'username': username
    }))


  async def disconnect(self, code):
    self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )


  @database_sync_to_async
  def save_message(self, username, thread_name, message):
    Chat.objects.create(
      sender=username,
      message=message,
      thread_name=thread_name,
      status=0,
      timestamp=datetime.now())

    sender = User.objects.get(username=username).id_user
    receiver = None
    if int(thread_name.split('-')[1]) != sender:
      receiver = thread_name.split('-')[1]
    else:
      receiver = thread_name.split('_')[1].split('-')[0]
    Messages.objects.create(
      id_user_receiver=receiver,
      id_user_sender=sender,
      text=message, status=0,
      date=datetime.now())

