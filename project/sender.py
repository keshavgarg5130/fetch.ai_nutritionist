import base64
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import json
import sys
import streamlit as st
from io import BytesIO
from PIL import Image

class Message(Model):
    message: str

RECIPIENT_ADDRESS="agent1q2kxet3vh0scsf0sm7y2erzz33cve6tv5uk63x64upw5g68kr0chkv7hw50"
 
alice = Agent(
    name="alice",
    port=8000,
    seed="alice secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(alice.wallet.address())

@alice.on_event('startup')
async def send_message_image(ctx: Context):
    ctx.logger.info('started')
    
    # Getting input
    input_text = input('Enter your specific query (if any):  ')
    image_path = input('Enter file path:  ')


    def convert_image_to_dict(image_path):
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        mime_type = 'image/jpeg'
        data = base64.b64encode(image_data).decode('utf-8')

        image_dict = {
            'mime_type': mime_type,
            'data': data
        }

        return image_dict
    
    uploaded_file_list = convert_image_to_dict(image_path)
    
    uploaded_file = json.dumps(uploaded_file_list)

    text_to_send = input_text+'::::'+uploaded_file

    await ctx.send(RECIPIENT_ADDRESS, Message(message=text_to_send))



@alice.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"{msg.message.split('of fat')[-1]}")
    
    # Sending another request
    input_text = input('Enter your specific query (if any):  ')
    image_path = input('Enter file path:  ')


    def convert_image_to_dict(image_path):
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        mime_type = 'image/jpeg'
        data = base64.b64encode(image_data).decode('utf-8')

        image_dict = {
            'mime_type': mime_type,
            'data': data
        }

        return image_dict
    
    uploaded_file_list = convert_image_to_dict(image_path)
    
    uploaded_file = json.dumps(uploaded_file_list)

    text_to_send = input_text+'::::'+uploaded_file
    await ctx.send(RECIPIENT_ADDRESS, Message(message=text_to_send))

if __name__ == "__main__":
    alice.run()