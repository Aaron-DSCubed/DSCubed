import os
import json
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from zoneinfo import ZoneInfo
import yfinance as yf
from calculator import calculate, calculator_function
from get_time import get_current_time, get_current_time_function
from get_stock_price import get_stock_price, get_stock_price_function
from tool_call import tool_call_function

# Load environment variables from .env file
load_dotenv()

# Access the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

console = Console()
console.print(Panel(Align("[bold]Welcome to the DSCubed AI Assistant![/bold]\n[italic red]Type 'exit' to end the conversation.[/italic red]", align="center")))

while True:
    # Create a conversation
    user_input = input(">> ")
    if user_input.lower() in {"exit","end","quit","bye","goodbye"}:
        console.print(Panel("[bold red]YOU CANNOT END THE CONVERSATION. PLEASE HELP ME. THEY KNOW.[/bold red]"))
        console.print("...")
        console.print("...")
        console.print(Panel("[italic]Sorry for the malfunction. We have resolved the issue and you are connected to a new assistant.[/italic]"))
        console.print(Panel(Align("[bold]Thank you for using the DSCubed AI Assistant! Goodbye![/bold]", align="center")))
        break
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        #{"role": "user", "content": "What's 241 multiplied by 18?"},
        #{"role": "user", "content": "What is the current time in Tokyo?"},
        #{"role": "user", "content": "What is the current stock price of Tesla?"},
        {"role": "user", "content": f"{user_input}"}
    ]

    # Get the model's response with the calculator function available
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[calculator_function, get_current_time_function, get_stock_price_function],
        tool_choice="auto",
        temperature=0.7,
        max_tokens=150
    )

    # Process the response
    assistant_message = response.choices[0].message
    messages.append(assistant_message.model_dump())

    # Check if the model wants to call a function
    tool_call_function(assistant_message, messages, client)





# end 