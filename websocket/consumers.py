from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event): #this handler is called when client initially opens a connection and is about to finish handshake.
        #print("websocket connected",event)
        self.send({
            'type' : 'websocket.accept'
        })

    def websocket_receive(self,event): #this handler is called when data is received  from client
        pass
        #print("websocket Received...",event) 
        #print("message is ", event['text'])
    
    def websocket_send(self,message):
        self.send({
            'type': 'websocket.send',
            'text': message
        })
    
    def websocket_disconnect(self,event): #this handler is called when either connection to the client is lost , either from client closing the connection , the server closing the connection or connection lost.
        #print("websocket disconnecte...",event)
        raise StopConsumer()



from channels.consumer import AsyncConsumer

class MyAyncConsumer(AsyncConsumer):
    # def __init__(self, scope):
    #     super().__init__(scope)
    #     self.email = None
    
    async def websocket_connect(self,event): #this handler is called when client initially opens a connection and is about to finish handshake.
        #print("websocket connected",event)
        self.email = self.scope['url_route']['kwargs'].get('email')  # Retrieve email from URL route parameters
        group_name = "admin"      
        # Add the user to the group
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        await self.send({
            'type' : 'websocket.accept'
        })

    async def websocket_receive(self,event): #this handler is called when data is received  from client
        #print("websocket Received...",event) 
        #print("message is ", event['text'])
        await self.send_message_to_group('admin',self.email+":message to all group")
    
    async def websocket_disconnect(self,event): #this handler is called when either connection to the client is lost , either from client closing the connection , the server closing the connection or connection lost.
        #print("websocket disconnecte...",event)
        raise StopConsumer()
    
    async def send_message_to_group(self, group_name, message):
        await self.channel_layer.group_send(
            group_name,
            {
                'type': 'group.message',
                'message': message
            }
        )
    
    async def group_message(self, event):
        message = event['message']
        await self.send({
            'type': 'websocket.send',
            'text': message
        })
    
    async def get_user_by_email(self, email):
        from account.models  import CustomUser
        try:
            user = await CustomUser.objects.get(email=email)
            return user
        except:
            return None

    