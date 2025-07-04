import os
#import requests
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Access the API key
APIkey = os.getenv("OPENAI_API_KEY")

client = OpenAI(
  api_key=APIkey
)



# Define a function that performs calculations
def calculate(operation, x, y):
    """
    Perform a mathematical operation on two numbers.

    Args:
        operation: The operation to perform (add, subtract, multiply, divide)
        x: The first number
        y: The second number

    Returns:
        The result of the operation
    """
    if operation == "add":
        return x + y
    elif operation == "subtract":
        return x - y
    elif operation == "multiply":
        return x * y
    elif operation == "divide":
        if y == 0:
            return "Error: Division by zero"
        return x / y
    else:
        return f"Error: Unknown operation '{operation}'"

# Define the function schema
calculator_function = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Perform a mathematical operation on two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The mathematical operation to perform"
                },
                "x": {
                    "type": "number",
                    "description": "The first number"
                },
                "y": {
                    "type": "number",
                    "description": "The second number"
                }
            },
            "required": ["operation", "x", "y"]
        }
    }
}

# Create a conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's 241 multiplied by 18?"}
]

# Get the model's response with the calculator function available
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=[calculator_function],
    tool_choice="auto",
    temperature=0.7,
    max_tokens=150
)

# Process the response
assistant_message = response.choices[0].message
messages.append(assistant_message.model_dump())

# Check if the model wants to call a function
if assistant_message.tool_calls:
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name

        if function_name == "calculate":
            # Parse the function arguments
            arguments = json.loads(tool_call.function.arguments)
            operation = arguments.get("operation")
            x = arguments.get("x")
            y = arguments.get("y")

            print(f"Function call: calculate({operation}, {x}, {y})")

            # Call the function
            result = calculate(operation, x, y)

            # Add the function result to the conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": str(result)
            })

            print(f"Function result: {result}")

    # Get a new response from the model with the function result
    second_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    # Print the final response
    print("\\nFinal response:")
    print(second_response.choices[0].message.content)
else:
    # The model chose to respond directly
    print("\\nDirect response (no function call):")
    print(assistant_message.content)







