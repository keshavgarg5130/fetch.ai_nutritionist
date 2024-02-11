from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model
from dotenv import load_dotenv
import json

load_dotenv() ## load all the environment variables

import os
import google.generativeai as genai
from PIL import Image


class Message(Model):
    message: str

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

bob = Agent(
    name="bob",
    port=8001,
    seed="bob secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"]
)
 
fund_agent_if_low(bob.wallet.address())

@bob.on_event('startup')
async def start(ctx: Context):
    ctx.logger.info(f'Started Bob and the address is {bob.address}')

@bob.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    input_prompt="""
    You are an expert in nutritionist where you need to see the food items from the image
                and calculate the total calories, also provide the details of every food items with calories intake
                is below format

                1. Item 1 - no of calories, carbohydrates, proteins, fats
                2. Item 2 - no of calories, carbohydrates, proteins, fats
                ----
                ----
    """
    def get_gemini_repsonse(input,image,prompt):
        model=genai.GenerativeModel('gemini-pro-vision')
        response=model.generate_content([input,image,prompt])
        return response.text
    input, image_data=msg.message.split('::::')
    image = json.loads(image_data)
    response=get_gemini_repsonse(input_prompt, image, input)
    ctx.logger.info(type(response))
    ctx.logger.info(f"Response of the AI is: {response}")
    await ctx.send(sender, Message(message=response))

if __name__ == "__main__":
    bob.run()