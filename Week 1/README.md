# My Package

> Tool Calling Chat Bot with ChatGPT

---

## 📦 Features

- Uses API Key from .env file
- Tools included for accessing current data and performing calculations (Calculator, Stock Price, and Time in a Given Timezone)

---

## 📁 Project Structure

- ask_ChatGPT.py: runs the program, includes initialisation, interface code and looping.
- tool_call.py: calls the tools that can be used by the program.
- calculator.py: calculate(operator, x, y) that takes in an operator (add, subtract, multiply, divide) and returns the result of the two floats x and y with operator. Also includes the function schema.
- get_stock_price.py: get_stock_price(ticker) that takes in the ticker symbol of the stock, e.g., 'AAPL', 'TSLA' and returns the current price of the stock. Also includes the function schema.
- get_time.py: get_current_time(timezone_str) that takes in the IANA timezone name, e.g., 'Asia/Tokyo', 'America/New_York' and returns the current local date and 24-hour time in the specified timezone. Also includes the function schema.

