import json
from django.contrib.auth.models import User
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Ad, ChatMessage


class MessageAddConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })

        ad_id = await self.get_ad_id(self.scope['url_route']['kwargs']['ad_slug'])

        self.ad = 'ad_' + ad_id

        await self.channel_layer.group_add(
            self.ad,
            self.channel_name
        )

    async def websocket_receive(self, event):
        data = event.get('text')
        comment_data = json.loads(data)
        ad_slug = comment_data['ad_slug']
        author_id = comment_data['author_id']
        author_name = User.objects.get(id=author_id).username
        body = comment_data['body']

        await self.create_comment(ad_slug, body, author_id)

        created_on = str(ChatMessage.objects.get(body=body).created_on.strftime("%Y-%m-%d %H:%M:%S"))

        comment = {
            'body': body,
            'author': author_name,
            'created_on': created_on
        }

        await self.channel_layer.group_send(
            self.ad,
            {
                'type': 'show_comment',
                'text': json.dumps(comment)
            }
        )

    async def websocket_disconnect(self, event):
        pass

    @database_sync_to_async
    def create_comment(self, ad_slug, body, author_id):
        author = User.objects.get(id=author_id)
        ad = Ad.objects.get(slug=ad_slug)
        ChatMessage.objects.create(ad=ad, body=body, author=author)

    @database_sync_to_async
    def get_ad_id(self, ad_slug):
        return str(Ad.objects.get(slug=ad_slug).id)

    async def show_comment(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
