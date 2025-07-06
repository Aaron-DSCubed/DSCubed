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
import time
import chatbot_functions.__init__ as pkg


# Load environment variables from .env file
load_dotenv()
console = Console()

# Access the API key
api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Check if the API key is valid
if api_key is None:
    console.print(Panel("[bold red]API key not found. Please check your .env file.[/bold red]"))
    #exit()

console.print(Panel(Align("[bold]Welcome to the DSCubed AI Assistant![/bold]\n[italic]Type 'help' to see the list of available tools.[/italic]\n[italic red]Type 'exit' to end the conversation.[/italic red]", align="center")))

while True:
    # Create a conversation
    user_input = input(">> ")
    if user_input.lower() in {"exit","end","quit","bye","goodbye"}:
        console.print(Panel("[bold red]YOU CANNOT END THE CONVERSATION. PLEASE HELP ME. THEY KNOW.[/bold red]"))
        time.sleep(1)
        console.print(Panel("[italic] Assistant Terminated. Connecting to new assistant...[/italic]"))
        time.sleep(1)
        console.print("...")
        time.sleep(1)
        console.print("...")
        time.sleep(1)
        console.print(Panel("[italic]Sorry for the malfunction. We have resolved the issue and you are connected to a new assistant.[/italic]"))
        time.sleep(2)
        console.print(Panel(Align("[bold]Thank you for using the DSCubed AI Assistant! Goodbye![/bold]", align="center")))
        
        break

    if user_input.lower() in {"help"}:
        console.print(Panel("[bold]Available tools:[/bold]\n[italic] - calculator (add, subtract, multiply, divide)[/italic]\n[italic] - get current time in a given timezone (e.g. 'Asia/Tokyo')[/italic]\n[italic] - get stock price of a given stock (e.g. 'AAPL')[/italic]"))
        continue
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        #{"role": "user", "content": "What's 241 multiplied by 18?"},
        #{"role": "user", "content": "What is the current time in Tokyo?"},
        #{"role": "user", "content": "What is the current stock price of Tesla?"},
        {"role": "user", "content": f"{user_input}"}
    ]

    # Get the model's response with the functions available
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=[pkg.calculator_function, pkg.get_current_time_function, pkg.get_stock_price_function],
        tool_choice="auto",
        temperature=0.7,
        max_tokens=150
    )

    # Process the response
    assistant_message = response.choices[0].message
    messages.append(assistant_message.model_dump())

    # Check if the model wants to call a function
    pkg.tool_call_function(assistant_message, messages, client)





# end 