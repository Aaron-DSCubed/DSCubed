from Package.calculator import calculate, calculator_function
from Package.get_time import get_current_time, get_current_time_function
from Package.get_stock_price import get_stock_price, get_stock_price_function
import json
from rich.panel import Panel
from rich.console import Console

console = Console()

# Check if the model wants to call a function
def tool_call_function(assistant_message, messages, client):
    if assistant_message.tool_calls:
        for tool_call in assistant_message.tool_calls:
            check=0
            function_name = tool_call.function.name

            if function_name == "calculate":
                # Parse the function arguments
                arguments = json.loads(tool_call.function.arguments)
                operation = arguments.get("operation")
                x = arguments.get("x")
                y = arguments.get("y")

                console.print(f"[italic](System Message) Function call: calculate({operation}, {x}, {y})[/italic]")

                # Call the function
                result = calculate(operation, x, y)

                # Add the function result to the conversation
                check=1

                #print(f"Function result: {result}")

            elif function_name == "get_current_time":
                # Parse the function arguments
                arguments = json.loads(tool_call.function.arguments)
                timezone_str = arguments.get("timezone_str")

                console.print(f"[italic](System Message) Function call: get_current_time({timezone_str})[/italic]")

                # Call the function
                result = get_current_time(timezone_str)

                # Add the function result to the conversation
                check=1
                #print(f"Function result: {result}")

            elif function_name == "get_stock_price":
                # Parse the function arguments
                arguments = json.loads(tool_call.function.arguments)
                ticker = arguments.get("ticker")

                console.print(f"[italic](System Message) Function call: get_stock_price({ticker})[/italic]")

                # Call the function
                result = get_stock_price(ticker)

                # Add the function result to the conversation
                check=1

                #print(f"Function result: {result}")
            if check==1:
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(result)
                })

        # Get a new response from the model with the function result
        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Print the final response
        # print("\nFinal response:")
        console.print(Panel(second_response.choices[0].message.content))
    else:
        # The model chose to respond directly
        #print("\n\nDirect response (no function call):")
        console.print(Panel(assistant_message.content))






