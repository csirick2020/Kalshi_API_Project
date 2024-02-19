# Kalshi_Day_Trader
# Buy sleep time = 3 minutes
# Sell sleep time = 1 minute
# Number of contracts able to be (effectively) traded with these parameters is 7 - 25

import time
from datetime import datetime as dt  # Alias 'datetime' as 'dt'
from datetime import time as dt_time
import pytz
from stdiomask import getpass
from KalshiClientsBaseV2 import ExchangeClient

# Set time constants
SECONDS_PER_MINUTE = 60
BUY_SLEEP_TIME = SECONDS_PER_MINUTE * 3  # 3 minutes
SELL_SLEEP_TIME = SECONDS_PER_MINUTE * 1  # 1 minute

# Function for logging


def log_trade(action, timestamp, details, side):
    with open('trades_log.txt', 'a') as log_file:
        log_file.write(f"{timestamp}: {action} - {details} - {side}\n")


# WELCOME
print("Welcome to the Kalshi Interactive Trading Client!")
print()

# ### AUTHENTICATION/LOGIN #####################################################################################################################################################################################################################################
print("First, you will need to log in with your Kalshi credentials.")

email = input("Please enter your login email: ")
password = getpass(prompt='Enter your password: ', mask='*')

# for prod
exchange_api_base = "https://trading-api.kalshi.com/trade-api/v2"

# for demo
# exchange_api_base = "https://demo-api.kalshi.co/trade-api/v2"


# Create an instance of the ExchangeClient and confirm login was successful
try:
    exchange_client = ExchangeClient(exchange_api_base, email, password)
    if exchange_client.user_id is not None:
        print("Successfully logged in.")
except Exception as e:
    print()
    print(f"An error occurred during authentication: {e}")
    print()
    print("Please restart the program and enter valid credentials.")
    input("Press enter to quit...")

# Get (current) exchange status
exchange_status = exchange_client.get_exchange_status()
print("Current exchange status:")
print(exchange_status)
print()

# Check your current balance
current_balance = exchange_client.get_balance()
print("Your current balance is: ")
print(current_balance)
print()

# ################ ~~ Choose if 'demo mode' or 'trading mode' ~~ ###############################################################
# ########################### \\\\\ 0 ///// ####################################################################################

# Set 'demo mode' variable (uses log_only functionality from Kalshi_API_Client_v1 code)
print("Before we begin choosing markets and other parameters, please choose either 'demo mode' or 'trading mode'.")
print()
print("'Demo mode' will ONLY write trade data to a .txt file called 'trades_log.txt' and store it on your computer.")
print("'Trading mode' will execute real trades and will also log the data (in 'trades_log.txt').")
print()
print("Please enter (1) for 'trading mode' or (2) for 'demo mode'...")
demo_mode = input()
while True:
    if demo_mode == '1':
        demo_mode = False
        break
    elif demo_mode == '2':
        demo_mode = True
        break
    else:
        print("Please type the number key '1' or '2' (and then Enter) to choose.")
        demo_mode = input()
        continue

# extra variable created to keep code consistent between the two versions/files
log_only = demo_mode

# ################ ~~ Choose Market/Event/Date Interactive ~~ ##################################################################
# ############################ \\\\\ 1 ///// ###################################################################################

# set event_date variable to pass into and be able to construct event tickers
event_date = ''
# set break_outer and break_mid (loop) variables since we have loops within loops within loops (# roller coaster business)
break_outer = False
break_mid = False

while True:
    if break_outer is False:
        try:
            market_choice = int(
                input("Please choose a market:\n(1) for Nasdaq100(NDQ)\n(2) for S&P500(SPX)\nYour choice here: ")
            )

            if 2 < market_choice < 1:  # user enters number that's not 1 or 2
                print()
                print("Please enter 1 for Nasdaq100 market or 2 for S&P500 market.")
                continue

            elif market_choice == 1:  # user chooses 1 for Nasdaq100
                # ######################################--- "Market choice pattern" ---################################
                # ########################################\\\ (Repeat for S&P500) \\\##################################
                print()
                print("You chose the Nasdaq100.")
                print()
                while True:
                    if break_mid is False:
                        try:
                            event_type = int(
                                input(
                                    "Please choose your Nasdaq100 Event...\n(1) for 'Daily (Range) Bracket'\n(2) for 'Daily Up/Down'\nYour choice here: "
                                )
                            )

                            if 1 > event_type > 2:  # User did not enter 1 or 2
                                print()
                                print("Please enter the number 1 or 2.")
                                print()
                                continue
                            elif event_type == 1:
                                print()
                                print("---Daily Bracket---")
                                print()
                                while True:
                                    event_date = input(
                                        "Please enter the year/month/day (of the daily bracket you want to work with) in this exact format...\nYY/MON/DD\nExample: 23/DEC/10\n*If you do not enter the year/month/day in the exact format mentioned, the program will break and you will have to start over.\nYou enter here: "
                                    ).upper()
                                    # Remove "/" characters from the user input
                                    event_date = event_date.replace("/", "")
                                    break_mid = True
                                    break
                            elif event_type == 2:
                                print()
                                print("---Daily Up/Down---")
                                print()
                                while True:
                                    event_date = input(
                                        "Please enter the year/month/day (of the daily Up/Down market you want to work with) in this exact format...\nYY/MON/DD\nExample: 23/DEC/10\n*If you do not enter the year/month/day in the exact format mentioned, the program will break and you will have to start over.\nYou enter here: "
                                    ).upper()
                                    # Remove "/" characters from the user input
                                    event_date = event_date.replace("/", "")
                                    break_mid = True
                                    break
                        except ValueError:  # User did not type an integer
                            print()
                            print("Invalid entry. Please type in a valid integer.")
                            print()
                    else:
                        break_outer = True
                        break
            # #################### --- end pattern --- ###################################################################################################
            elif market_choice == 2:  # user chooses 2 for SPY
                # ######################################--- "Market choice pattern" ---################################
                print()
                print("You chose the S&P500.")
                print()
                while True:
                    if break_mid is False:
                        try:
                            event_type = int(
                                input(
                                    "Please choose your S&P500 Event...\n(1) for 'Daily (Range) Bracket'\n(2) for 'Daily Up/Down'\nYour choice here: "
                                )
                            )

                            if 1 > event_type > 2:  # User did not enter 1 or 2
                                print()
                                print("Please enter the number 1 or 2.")
                                print()
                                continue
                            elif event_type == 1:
                                print()
                                print("---Daily Bracket---")
                                print()
                                while True:
                                    event_date = input(
                                        "Please enter the year/month/day (of the daily bracket you want to work with) in this exact format...\nYY/MON/DD\nExample: 23/DEC/10\n*If you do not enter the year/month/day in the exact format mentioned, the program will break and you will have to start over.\nYou enter here: "
                                    ).upper()
                                    # Remove "/" characters from the user input
                                    event_date = event_date.replace("/", "")
                                    break_mid = True
                                    break
                            elif event_type == 2:
                                print()
                                print("---Daily Up/Down---")
                                print()
                                while True:
                                    event_date = input(
                                        "Please enter the year/month/day (of the daily Up/Down market you want to work with) in this exact format...\nYY/MON/DD\nExample: 23/DEC/10\n*If you do not enter the year/month/day in the exact format mentioned, the program will break and you will have to start over.\nYou enter here: "
                                    ).upper()
                                    # Remove "/" characters from the user input
                                    event_date = event_date.replace("/", "")
                                    break_mid = True
                                    break
                        except ValueError:  # User did not type an integer
                            print()
                            print("Invalid entry. Please type in a valid integer.")
                            print()
                    else:
                        break_outer = True
                        break
        # #################### --- end pattern --- ##############################################################################

        # Raise ValueError if user did not type an integer when choosing initial market
        except ValueError:
            print()
            print("Invalid entry. Please type in a valid integer.")
            print()
    else:  # This section has been completed
        break
# ############################ END ///// 1 \\\\\ END ############################################################################

# Create variables for our event tickers
# Nasdaq 100
ndqDaily = f'NASDAQ100-{event_date}'
ndqUpDown = f'NASDAQ100Z-{event_date}'  # Up/Down Event doesn't seem to be open every trading day (from past observation)

# S&P 500
spDaily = f'INX-{event_date}'
spUpDown = f'INXZ-{event_date}'  # Up/Down Event doesn't seem to be open every trading day (from past observation)

# Create limit variable to pass into 'get_markets()' function
limiter = 15  # Keep at 15 (there will not be more than 15 markets for any event)

# Create an event ticker variable (to pass into 'get_markets()' function)
event_tick = ''

# Create an individual market variable to work with (later in the code)
ind_mrkt_tick = ''

# Populate 'event_tick' variable based on user's choices
if market_choice == 1:  # User chose Nasdaq100
    if event_type == 1:
        event_tick = ndqDaily
    elif event_type == 2:
        event_tick = ndqUpDown
if market_choice == 2:  # User chose S&P 500
    if event_type == 1:
        event_tick = spDaily
    elif event_type == 2:
        event_tick = spUpDown

print()
print(f"Event ticker: {event_tick}")
print()

time.sleep(1)

# Example get_markets call --- retrieves data you need (to filter, work with, etc.)
get_markets_call = exchange_client.get_markets(limit=limiter, event_ticker=event_tick)

# Index into said keys (to filter data)
keys_to_access = [  # These are the data the user will be shown
    'ticker',
    'subtitle',
    'status',
    'yes_bid',
    'no_bid',
    'last_price',
    'volume',
    'volume_24h',
]


# Get the data (based on keys_to_access variable)
print("Here is the current data for the market you have chosen: ")
print()
time.sleep(3)
dict_number = 1
print(dict_number)
for market_data in get_markets_call['markets']:
    values = {key: market_data[key] for key in keys_to_access}
    # Convert the dictionary to a formatted string for easy viewing
    formatted_data = "\n".join([f"{key}: {value}" for key, value in values.items()])
    print(formatted_data)
    print()
    dict_number += 1
    if dict_number <= limiter:
        print(dict_number)

print()
ind_mrkt_tick = input(
    "Which market would you like to work with?\nPlease copy and paste one of the tickers from above. ***Example (format): NASDAQ100-24JAN18-B17450\n(*In the case of the 'Daily Up/Down' market, there is only one ticker.)\nPlease note that if the ticker is copied incorrectly, the program will not be able to read it and you will have to start over.\n(If no ticker was displayed above, make sure the date you've entered is a valid trading date and not a bank holiday.)\nPaste market ticker here:  "
)

# Remove spaces - (if user accidentally copied ticker w/ a space character)
ind_mrkt_tick = f"{ind_mrkt_tick}".replace(" ", "")

# Print individual ticker you're working with (for looks/readability on output screen)
print()
print(ind_mrkt_tick)
print()

# Have user choose a side ("yes" or "no")
choose_side = input(
    "Would you like to bet 'for' ('Yes') or 'against' ('No') this market position?\nPlease type 'Y' for 'Yes' or 'N' for 'No'.\n(If you type anything besides 'Y' or 'N' you will not pass 'Go' and you will NOT collect $200.)\nType your choice here: "
).upper()

# Create variables for conditional buying
avg_yes = 0  # 0 is place holder
avg_no = 0  # 0 is place holder

# Set a variable for how many contracts you're willing to buy while buying conditions are met within the loop
print()
contract_ceiling = int(
    input(
        "In a moment, we will choose some parameters like price and time of day to direct the program's (algorithmic) trading.\nBefore we do so, please set a maximum number of contracts you would be able/willing to buy in this session.\n(Tip: Do not set above 25 in this version of the program.)\nType in a valid (whole) number: "
    )
)

# Set variables for how many contracts the algorithm has bought and sold
contracts_bought = 0  # always begins at 0
contracts_sold = 0  # always begins at 0


# Function for "yes" contract data


def get_buy_mrkt_info():
    global avg_yes
    ind_mrkt_data = exchange_client.get_market(ticker=ind_mrkt_tick)
    # Access 'yes_bid' and 'yes_ask'
    yes_bid = ind_mrkt_data['market']['yes_bid']
    yes_ask = ind_mrkt_data['market']['yes_ask']
    avg_yes = (yes_ask + yes_bid) / 2
    subtitle = ind_mrkt_data['market']['subtitle']
    print(f"Subtitle: {subtitle}")
    print(f"Bid/ask average: {avg_yes}")


# Function for "no" contract data


def get_buy_mrkt_info_no():
    global avg_no
    ind_mrkt_data = exchange_client.get_market(ticker=ind_mrkt_tick)
    # Access 'no_bid' and 'no_ask'
    no_bid = ind_mrkt_data['market']['no_bid']
    no_ask = ind_mrkt_data['market']['no_ask']
    avg_no = (no_ask + no_bid) / 2
    subtitle = ind_mrkt_data['market']['subtitle']
    print(f"Subtitle: {subtitle}")
    print(f"Bid/ask average: {avg_no}")


# --------------------------------------- USER PICKS TIME ----------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# Have user select their (U.S.) time zone
print()  # always before new input message (spacing)
usr_tz_choice = int(
    input(
        "You will be choosing a time range in which the program will be able to execute buying.\nIn order to do so, please first choose your (U.S.) time zone.\nType (1) for Eastern; (2) for Central; (3) for Mountain; or (4) for Pacific.\nYour choice here: "
    )
)

# Implement datetime logic into code
if usr_tz_choice == 1:
    usr_tz = pytz.timezone('US/Eastern')
elif usr_tz_choice == 2:
    usr_tz = pytz.timezone('US/Central')
elif usr_tz_choice == 3:
    usr_tz = pytz.timezone('US/Mountain')
elif usr_tz_choice == 4:
    usr_tz = pytz.timezone('US/Pacific')
else:
    print("Invalid choice. Please choose a number between 1 and 4.")
    input("Press enter to quit...")

# Get the current time in the user's chosen timezone
current_time = dt.now(usr_tz).time()
# Create new time object without microseconds
current_time = dt_time(current_time.hour, current_time.minute, current_time.second)
print(f"Current time (based on your choice): {current_time}")
print()

# Have user choose time range (for buying)
print("Next, you will be choosing a time range during which the program is allowed to buy.\nKeep in mind you will also be setting a price range...\n(So that, IF the time of day is in your range AND the contract's price is in your range, buying will occur.)")
print()
start_time = input("Please enter the start time for your 'buy' range in the following 24 hr. format.\n'HH:MM' --- Example--- 08:30 = 8:30 AM /// 12:07 = 12:07 PM /// 15:20 = 3:20 PM\nYou enter here: ")
print()
end_time = input("Please enter the end time for your 'buy' range in the same (24 hr.) format.\n(Tip: Buy range should end at least 20 minutes before market close to allow time for stop-loss selling.)\nYou enter here: ")
print()
print("(Tip: Market closing time is automatically calculated based on the time zone you entered.\nBe aware of normal Wall St. trading hours in your time zone to avoid setting your 'buy' time incorrectly.)")
print()
# Convert user inputs to time objects
start_hours, start_minutes = map(int, str(start_time).split(':'))
end_hours, end_minutes = map(int, str(end_time).split(':'))

# Strip leading zeros
start_hours = int(str(start_hours).lstrip('0'))
end_hours = int(str(end_hours).lstrip('0'))

# Create time objects
start_time = dt_time(start_hours, start_minutes)
end_time = dt_time(end_hours, end_minutes)

# Display formatted variable time range
print(f"'Buy' time range set: {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')}")
print()

# Create new time objects without microseconds
start_time = dt_time(start_time.hour, start_time.minute, start_time.second)
end_time = dt_time(end_time.hour, end_time.minute, end_time.second)
# ##############################################################################################################################
# --#--#--#- ### SET 'SELL' TIME RANGE ### -#--#--#--#-------------------------------------------------------------------------
start_time2 = end_time  # * Selling will not occur until 'buy' time range is over *
# Create a variable for (selling) end time (based on Wall St. close)

end_time2 = dt_time()
# Selling end time will vary based on U.S. Time Zone
if usr_tz_choice == 1:
    end_time2 = dt_time(15, 58)  # 3:58 PM
elif usr_tz_choice == 2:
    end_time2 = dt_time(14, 58)  # 2:58 PM
elif usr_tz_choice == 3:
    end_time2 = dt_time(13, 58)  # 1:58 PM
elif usr_tz_choice == 4:
    end_time2 = dt_time(12, 58)  # 12:58 PM
# -------------------------------------------------------------------------------------------------------------------------------
# ##############################################################################################################################
# Make end_time2 uniform (no microseconds)
end_time2 = dt_time(end_time2.hour, end_time2.minute, end_time2.second)
# --------------------------- END OF USER PICK TIME ----------------------------------------------------------------


# ------------------------- USER PICKS PRICE (RANGE) -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
print("You will now choose your price range for buying contracts.")
min_price_range = int(input("Please enter the minimum price (at which you will buy):\n(Example: '40' = $0.40)\n"))
max_price_range = int(input("Please enter the maximum price (at which you will buy):\n(Example: '90' = $0.90)\n"))
print(f"Your price range: {min_price_range} to {max_price_range}")
print()
print("You will now set a stop-loss price (at which the program will sell).\n(NOTE: The contracts will sell one by one with a short interval in between each sale, NOT all at once.")
sell_price = int(input("Set your stop-loss price: "))
print()
print("Program loop is now active.")
print()
# ---------------------------- END OF USER PICKS PRICE (RANGE) -----------------------------------------------------

# Create a variable for number of loops (to prevent possible time-outs)
num_of_loops = 0

# ##############################################################################################################################
# This is the "Buy" loop -------------------------------------------------------------------------------------------------------
# ##############################################################################################################################
while True:
    # First, check if buying time is over...
    # This line is repeated in the 'while' loop because time always updates (obviously)
    current_time = dt.now(usr_tz).time()
    # Create new time object without microseconds (for proper comparison)
    current_time = dt_time(current_time.hour, current_time.minute, current_time.second)
    # compare to user's set 'end_time'
    if current_time > end_time:
        print(f"The current time is {current_time}. Your 'buy' range ended at {end_time}.")
        print()
        break
    # Check number of loops and log in again if > 20 --- (to prevent possible time-outs)
    if num_of_loops > 20:
        exchange_client = ExchangeClient(exchange_api_base, email, password)
        # Get (current) exchange status and display it
        exchange_status = exchange_client.get_exchange_status()
        print(exchange_status)
        print()
        num_of_loops = 0  # reset loop count

    # For "yes" contract
    if choose_side == 'Y':
        get_buy_mrkt_info()
    # For "no" contract
    elif choose_side == 'N':
        get_buy_mrkt_info_no()
    else:
        print("Error: choose_side variable should be set to either 'Y' or 'N'")
        input("Press enter to quit...")

    # This line is repeated in the 'while' loop because time always updates (obviously)
    current_time = dt.now(usr_tz).time()

    # Create new time object without microseconds and display it
    current_time = dt_time(current_time.hour, current_time.minute, current_time.second)
    print(current_time)
    print()

    # ##### 'buyblock' ##### ---------------------------------------------------------------------------------------
    # Implement conditional buying
    # "YES" SIDE *****
    if choose_side == 'Y':
        # If the price is right...
        if min_price_range <= avg_yes <= max_price_range:
            # If the time is right...
            if start_time <= current_time <= end_time:
                # If not just logging...
                if log_only is False:
                    # Actual buying occurs...
                    exchange_client.create_order(
                        ticker=ind_mrkt_tick,
                        client_order_id=exchange_client.user_id,
                        side="yes",
                        action="buy",
                        count=1,
                        type="market",
                    )
                contracts_bought += 1  # add one to contracts_bought before logging
                # Write buys to a log file
                log_trade(action='Buy', timestamp=current_time, details=avg_yes, side=choose_side)
                print(f"Buying conditions met, a total of {contracts_bought} {choose_side} contract(s) have been purchased.")
                print("Trade logged in .txt file.")
                print()
                num_of_loops += 1
                if contracts_bought < contract_ceiling:
                    time.sleep(BUY_SLEEP_TIME)  # sleep for longer after a "buy" to make sure price is staying consistent
                    continue
                else:
                    print("Buy ceiling has been met.")
                    break
            else:
                num_of_loops += 1
                time.sleep(20)
                continue
        else:
            num_of_loops += 1
            time.sleep(20)
            continue
    # "NO" SIDE *****
    elif choose_side == 'N':
        # If the price is right...
        if min_price_range <= avg_no <= max_price_range:
            # If the time is right...
            if start_time <= current_time <= end_time:
                # If not just logging...
                if log_only is False:
                    # Actual buying occurs...
                    exchange_client.create_order(
                        ticker=ind_mrkt_tick,
                        client_order_id=exchange_client.user_id,
                        side="no",
                        action="buy",
                        count=1,
                        type="market",
                    )
                contracts_bought += 1  # add one to contracts_bought before logging
                # Write buys to a log file
                log_trade(action='Buy', timestamp=current_time, details=avg_no, side=choose_side)
                print(f"Buying conditions met, a total of {contracts_bought} {choose_side} contract(s) have been purchased.")
                print()
                print("Trade logged in .txt file.")
                print()
                num_of_loops += 1
                if contracts_bought < contract_ceiling:
                    time.sleep(BUY_SLEEP_TIME)  # sleep for longer after a "buy" to make sure price is staying consistent
                    continue
                else:
                    print("Buy ceiling has been met.")
                    break
            else:
                num_of_loops += 1
                time.sleep(20)
                continue
        else:
            num_of_loops += 1
            time.sleep(20)
            continue

    else:
        print("Error: choose_side variable should be set to either 'Y' or 'N'")
        input("Press enter to quit...")

# ##############################################################################################################################
# This is the "Sell" loop ------------------------------------------------------------------------------------------------------
# ##############################################################################################################################
while True:
    # The first thing to check is if any contracts were bought...
    if contracts_bought < 1:
        print(f"The number of contracts purchased is {contracts_bought}. Exiting the 'Sell loop'.")
        print()
        break
    # Next, check if 'selling time' is over...
    # This line is repeated in the 'while' loop because time always updates (obviously)
    current_time = dt.now(usr_tz).time()
    # Create new time object without microseconds (for proper comparison)
    current_time = dt_time(current_time.hour, current_time.minute, current_time.second)
    # compare to 'end_time2' variable
    if current_time > end_time2:
        print(f"The current time is {current_time}. This market's 'sell' time range ended at {end_time2}.")
        print()
        break
    # Check number of loops and log in again if > 20 --- (to prevent possible time-outs)
    if num_of_loops > 20:
        exchange_client = ExchangeClient(exchange_api_base, email, password)
        # Get (current) exchange status and display it
        exchange_status = exchange_client.get_exchange_status()
        print(exchange_status)
        print()
        num_of_loops = 0  # reset loop count

    # For "yes" contract
    if choose_side == 'Y':
        get_buy_mrkt_info()
    # For "no" contract
    elif choose_side == 'N':
        get_buy_mrkt_info_no()
    else:
        print("Error: choose_side variable should be set to either 'Y' or 'N'")
        input("Press enter to quit...")

    # This line is repeated in the 'while' loop because time always updates (obviously)
    current_time = dt.now(usr_tz).time()

    # Create new time object without microseconds and display it
    current_time = dt_time(current_time.hour, current_time.minute, current_time.second)
    print(current_time)
    print()

    # ##### 'sellblock' ##### ---------------------------------------------------------------------------------------
    # Implement conditional selling
    # "YES" SIDE *****
    if choose_side == 'Y':
        # If the price drops to sell_price...
        if avg_yes <= sell_price:
            # If not just logging...
            if log_only is False:
                # Actual selling occurs...
                exchange_client.create_order(
                    ticker=ind_mrkt_tick,
                    client_order_id=exchange_client.user_id,
                    side="yes",
                    action="sell",
                    count=1,
                    type="market",
                )
            contracts_sold += 1  # add one to contracts_sold before logging
            # Write sells to log file
            log_trade(action='Sell', timestamp=current_time, details=avg_yes, side=choose_side)
            print(f"Selling conditions met, a total of {contracts_sold} {choose_side} contract(s) have been sold.")
            print()
            print("Trade logged in .txt file.")
            print()
            num_of_loops += 1
            if contracts_sold < contracts_bought:
                time.sleep(SELL_SLEEP_TIME)  # Sell time sleep quicker than buy sleep
                continue
            else:
                print("All contracts bought in this session have been sold.")
                print()
                break
        else:
            num_of_loops += 1
            time.sleep(20)
            continue

    # "NO" SIDE *****
    elif choose_side == 'N':
        # If the price drops to sell_price...
        if avg_no <= sell_price:
            # If not just logging...
            if log_only is False:
                # Actual selling occurs...
                exchange_client.create_order(
                    ticker=ind_mrkt_tick,
                    client_order_id=exchange_client.user_id,
                    side="no",
                    action="sell",
                    count=1,
                    type="market",
                )
            contracts_sold += 1  # add one to contracts_sold before logging
            # Write sells to log file
            log_trade(action='Sell', timestamp=current_time, details=avg_no, side=choose_side)
            print(f"Selling conditions met, a total of {contracts_sold} {choose_side} contract(s) have been sold.")
            print()
            print("Trade logged in .txt file.")
            print()
            num_of_loops += 1
            if contracts_sold < contracts_bought:
                time.sleep(SELL_SLEEP_TIME)  # Sell time sleep quicker than buy sleep
                continue
            else:
                print("All contracts bought in this session have been sold.")
                print()
                break
        else:
            num_of_loops += 1
            time.sleep(20)
            continue

# Logout Functionality (can't seem to get it to work) --------------------------------------------------------------------------

# def logout(self,):
# ### result = self.post("/logout")
# ### return result
# exchange_client.logout()  # Not working, missing some kind of argument(s)...

# Logout -----------------------------------------------------------------------------------------------------------------------

input("Press enter to quit...")
