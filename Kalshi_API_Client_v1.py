# Kalshi API Client

import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime as dt, time as dt_time
import pytz
from KalshiClientsBaseV2 import ExchangeClient
import json
from Kalshi_ROI import kalshi_ROI  # home-made function that allows you to calculate ROI of a strategy

# variables to disable whole blocks of code at a time:
# (All set to True here and changed above their corresponding block)
disable_block1 = True
disable_block2 = True
disable_block3 = True
disable_block4 = True
disable_buyblock = True
disable_sellblock = True

# use config file to pass in sensitive info
# Open and read the configuration file
config_file_path = "/home/name01/.config/sublime-text/Programs/Kalshi Project/config-file.json"

with open(config_file_path) as config_file:
    config = json.load(config_file)

email = config["email"]
password = config["password"]

# for prod
exchange_api_base = "https://trading-api.kalshi.com/trade-api/v2"

# for demo
# exchange_api_base = "https://demo-api.kalshi.co/trade-api/v2"

# Create an instance of the ExchangeClient and confirm login was successful
exchange_client = ExchangeClient(exchange_api_base, email, password)
# print(exchange_client.user_id)
# print(exchange_client.token)
if exchange_client.user_id is not None:
    print("Successfully logged in.")

# Get (current) exchange status
exchange_status = exchange_client.get_exchange_status()
print("Current exchange status:")
print(exchange_status)
print()  # Empty line after for readability

# Check your current balance
current_balance = exchange_client.get_balance()
print("Your current balance is: ")
print(current_balance)
print()

# Get markets by calling this method and passing in whatever arguments are necessary
#  \/ Method \/ #
# def get_markets(self,
# limit:Optional[int]=None,
# cursor:Optional[str]=None,
# event_ticker:Optional[str]=None,
# series_ticker:Optional[str]=None,
# max_close_ts:Optional[int]=None,
# min_close_ts:Optional[int]=None,
# status:Optional[str]=None,
# tickers:Optional[str]=None,
#    ):
# query_string = self.query_generation(params={k: v for k,v in locals().items()})
# dictr = self.get(self.markets_url+query_string)
# return dictr


# Create a list of some common event tickers

# Nasdaq 100
ndqEOY = 'NASDAQ100Y-23DEC29'  # Only changes yearly
ndqEOM = 'NASDAQ100M-23NOV30'  # Has to be changed monthly
ndqWeekly = 'NASDAQ100D-23NOV10'  # Has to be changed weekly
ndqDaily = 'NASDAQ100D-23DEC04'  # Has to be changed daily
ndqUpDown = 'NASDAQ100Z-23NOV17'  # Has to be changed daily//this market not available every day

# S&P 500
spEOY = 'INXY-23DEC29'  # Only changes yearly
spEOM = 'INXM-23NOV30'  # Has to be changed monthly
spWeekly = 'INXD-23NOV10'  # Has to be changed weekly
spDaily = 'INXD-23DEC04'  # Has to be changed daily
spUpDown = 'INXZ-23NOV07'  # Has to be changed daily//this market not available every day

# Create limit variable for cohesiveness
limiter = 15

# Create an event ticker variable for cohesiveness throughout the code
event_tick = ndqDaily  # Change for whatever event market you are wanting to work with

# Example get_markets call
get_markets_call = exchange_client.get_markets(limit=limiter, event_ticker=event_tick)
# print(get_markets_call)

# Working with the data >>> ----------------------------------------------------------------------------------------
# --------------------- >>> ----------------------------------------------------------------------------------------
# Get the list of keys in the dictionary
# keys = get_markets_call['markets'][0].keys()
# print(list(keys))

# Index into said keys (to filter data)
keys_to_access = [  # Choose what keys you want
    'ticker',
    'subtitle',
    'status',
    'yes_bid',
    'no_bid',
    'last_price',
    'volume',
    'volume_24h',
]

# # Code block 1 # -----------------------------------------------------------------------------------------------
# Gets the data and displays whatever keys are in keys_to_access variable
disable_block1 = True
if disable_block1:  # (== True)
    pass
else:  # apply filter
    dict_number = 1
    print(dict_number)
    for market_data in get_markets_call['markets']:
        values = {key: market_data[key] for key in keys_to_access}
        # Convert the dictionary to a formatted string for easy printing
        formatted_data = "\n".join([f"{key}: {value}" for key, value in values.items()])
        print(formatted_data)
        print()  # Add an empty line to separate each dictionary
        dict_number += 1
        if dict_number <= limiter:
            print(dict_number)

# quit()  # If just getting event info

# -----------------------------------------------------------------------------------------------------------------

# Fetch and display yes_bid, yes_ask, and subtitle for every market in an event
bin_prob_keys = ['yes_bid', 'yes_ask', 'subtitle']

# ## Code block 2 ## ----------------------------------------------------------------------------------------------
# Gets the data and displays bin_prob_keys
disable_block2 = True
if disable_block2:
    pass
else:
    # Grab data and print for easy reading
    for market_data in get_markets_call['markets']:
        values = {key: market_data[key] for key in bin_prob_keys}
        print(values)
        print()
        # Convert the dictionary to a formatted string for easy printing
        formatted_data = "\n".join([f"{key}: {value}" for key, value in values.items()])
        print(formatted_data)
        print()  # Add an empty line to separate each dictionary
    # print(type(values))
    # print(type(formatted_data))

# Now on to the fun stuff...
# Create lists for future histplot of probable outcomes
bins = []
prob_data = []

# ### Code block 3 ### --------------------------------------------------------------------------------------------
disable_block3 = True
if disable_block3:
    pass
else:  # Calculate Probability of Outcome based off current bids
    # Iterate through each market data
    for market_data in get_markets_call['markets']:
        # Extract 'yes_bid', 'yes_ask', and 'subtitle' values
        yes_bid = market_data['yes_bid']
        yes_ask = market_data['yes_ask']
        est_prob = (yes_ask + yes_bid) / 2
        subtitle = market_data['subtitle']

        # Add 'subtitle' and 'est_prob' data to the respective lists
        bins.append(subtitle)
        prob_data.append(est_prob)

    # View data in print form
    # print("Bins:")
    # print(bins)
    # print("Probability Data:")
    # print(prob_data)

# ### GET SUBTITLES FOR EVENT ################################################################################
subtitle_key = ['subtitle']  # for use in function below


def get_subtitles():  # Get list of subtitles for subtitle_order list below (x-axis labels)
    for market_data in get_markets_call['markets']:
        values = {key: market_data[key] for key in subtitle_key}
        print(values)


# get_subtitles()
# ############################################################################################################

# Plotting the data

# #### Code block 4 #### ------------------------------------------------------------------------------------------
disable_block4 = True
if disable_block4:
    pass
else:
    # Create a custom order for the x-axis labels (subtitle values)
    # Has to be modified for every different event (see Code Notes)
    subtitle_order = [
        '8,499.99 or lower',
        '8,500 to 8,999.99',
        '9,000 to 9,499.99',
        '9,500 to 9,999.99',
        '10,000 to 10,499.99',
        '10,500 to 10,999.99',
        '11,000 to 11,499.99',
        '11,500 to 11,999.99',
        '12,000 to 12,499.99',
        '12,500 to 12,999.99',
        '13,000 to 13,499.99',
        '13,500 to 13,999.99',
        '14,000 to 14,499.99',
        '14,500 to 14,999.99',
        '15,000 or higher',
    ]

    # Sort the 'bins' and 'prob_data' based on the custom order
    sorted_data = sorted(zip(bins, prob_data), key=lambda x: subtitle_order.index(x[0]))
    sorted_bins, sorted_prob_data = zip(*sorted_data)

    # Convert 'sorted_prob_data' into a NumPy array
    sorted_prob_data = np.array(sorted_prob_data)

    # Set the figure size
    plt.figure(figsize=(12, 7))

    # Determine colors based on 'prob_data' values, mapping from red to green
    colors = plt.cm.RdYlGn((sorted_prob_data - min(sorted_prob_data)) / (max(sorted_prob_data) - min(sorted_prob_data)))

    # Create the bar plot with custom coloring
    plt.bar(sorted_bins, sorted_prob_data, color=colors)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=90)

    # Set labels and title
    plt.xlabel('Price Ranges ($)', labelpad=20)
    plt.ylabel('Estimated Probability (%)', labelpad=20)
    if event_tick == spEOY:
        plt.title('Prediction Market Forecast - SPX (EOY)')
    elif event_tick == ndqEOY:
        plt.title('Prediction Market Forecast - NDX (EOY)')
    else:
        plt.title('Prediction Market Forecast')

    # Show the plot
    plt.show()


# ### WORKING WITH INDIVIDUAL MARKETS #############################################################################
# #################################################################################################################
# First, extract the individual market tickers
def get_tickers():  # Function to extract tickers from event
    ticker_extract = ['ticker', 'subtitle']
    for market_data in get_markets_call['markets']:
        values = {key: market_data[key] for key in ticker_extract}
        print(values)


# get_tickers()  # Uncomment/Comment this as needed

# quit()

###################################################################################################################
# -----------------------------------------------------------------------------------------------------------------
# Set individual market ticker variable
ind_mrkt_tick = 'NASDAQ100D-23DEC04-B15750'  # Put whatever market ticker you want to work with here
# -----------------------------------------------------------------------------------------------------------------
###################################################################################################################
# Once you have the ticker, you can get the data
# ---Format (from KalshClientsBaseV2.py)---
###############################################
# def get_market(self,
# ticker:str):
# market_url = self.get_market_url(ticker=ticker)
# dictr = self.get(market_url)
# return dictr
###############################################


def get_individual_market():  # Get an individual market's data (all data)
    ind_mrkt_data = exchange_client.get_market(ticker=ind_mrkt_tick)
    print(ind_mrkt_data)


# get_individual_market()  # This pulls up all market data, but all we need for conditional buy is ask and bid price(s).
#################################################################################################################


# Print individual ticker you're working with (for looks/readability on output screen)
print(ind_mrkt_tick)
print()

# Set variables for conditional buying
avg_yes = 0  # set to 0
avg_no = 0  # set to 0

# Set variables for how many contracts the algorithm has bought/sold
contracts_bought = 0  # always starts at 0
contracts_sold = 0  # always starts at 0

# Function to retrieve "yes" contract data


def get_buy_mrkt_info():
    global avg_yes
    ind_mrkt_data = exchange_client.get_market(ticker=ind_mrkt_tick)
    # Access 'yes_bid' and 'yes_ask'
    yes_bid = ind_mrkt_data['market']['yes_bid']
    yes_ask = ind_mrkt_data['market']['yes_ask']
    avg_yes = (yes_ask + yes_bid) / 2
    subtitle = ind_mrkt_data['market']['subtitle']
    print(subtitle)
    print(avg_yes)


# Function to retrieve "no" contract data


def get_buy_mrkt_info_no():
    global avg_no
    ind_mrkt_data = exchange_client.get_market(ticker=ind_mrkt_tick)
    # Access 'no_bid' and 'no_ask'
    no_bid = ind_mrkt_data['market']['no_bid']
    no_ask = ind_mrkt_data['market']['no_ask']
    avg_no = (no_ask + no_bid) / 2
    subtitle = ind_mrkt_data['market']['subtitle']
    print(subtitle)
    print(avg_no)


# ###############################################################################################################################
# Function to write "buys" to a log file -------------------------------------------------------------------------------------------------------


def log_trade(action, timestamp, details, side):
    with open('trades_log.txt', 'a') as log_file:
        log_file.write(f"{timestamp}: {action} - {details} - {side}\n")


# Example usage:
# action = 'Buy'
# timestamp = central_time
# details = avg_yes  # Change if you're using "no" market
# side = yes_or_no
# -------------------------------------------------------------------------------------------------------------------------------
# ###############################################################################################################################
# ############################################## >>-------------------------------------------------------------------------------------------
# Buy/sell functionality variables *(IMPORTANT)* >>>-------------------------------------------------------------------------------
# ############################################## >>-------------------------------------------------------------------------------------------
# ###############################################################################################################################

# Create a variable to choose which "side" you're on - This will enable the correct functionality below
yes_or_no = "No"

# Create price range variables
price_low_end = 60  # the lowest you'll buy
price_high_end = 80  # the highest you'll buy
sell_price = 21  # if number falls below this price, you will sell...
# *Note: sell loop will only initiate if a) contract_ceiling is met, or b) when end_time (on buy loop) is met.*

# Set a variable for how many contracts you're willing to buy while buying conditions are met within the loop
contract_ceiling = 10

# Create a variable which tells the program whether to log trades or not
logging_trades = True

# Create a variable for testing which only logs the trade instead of actually buying/selling
log_only = True  # set to False to execute real trades ***!

# ###############################################################################################################################
# End of buy/sell functionality variables *(besides Time)* >>>-------------------------------------------------------------------------------
#################################################################################################################################

# Create a variable for number of loops (due to timeout/authentication error)
num_of_loops = 0  # set to 0

# ###############################################################################################################################
# ############################################## >>------------------------------------------------------------------------------------------
# Time functionality variables *(IMPORTANT)* >>>--------------------------------------------------------------------------------------------
# ############################################## >>------------------------------------------------------------------------------------------
# ###############################################################################################################################
# Implement datetime logic into code
# Get the current time in the 'US/Central' time zone
central_time = dt.now(tz=pytz.timezone('US/Central')).time()
# Create a specified time range (using time objects) ############################################################################
# -------------------------------------------------------------------------------------------------------------------------------
# --#--#--#- ### SET TIME RANGE ### -#--#--#--#----------------------------------------------------------------------------------
start_time = dt_time(12, 0)  # 12:00 PM
end_time = dt_time(14, 0)  # 2:00 PM
# -------------------------------------------------------------------------------------------------------------------------------
# ###############################################################################################################################
# Create new time objects without microseconds
start_time = dt_time(start_time.hour, start_time.minute, start_time.second)
end_time = dt_time(end_time.hour, end_time.minute, end_time.second)
central_time = dt_time(central_time.hour, central_time.minute, central_time.second)
# ###############################################################################################################################
# --#--#--#- ### SET 'SELL' TIME RANGE ### -#--#--#--#---------------------------------------------------------------------------
start_time2 = end_time
# Create a variable for (selling) end time
end_time2 = dt_time(14, 58)  # 2:58 PM
# -------------------------------------------------------------------------------------------------------------------------------
# ###############################################################################################################################
# Make end_time2 uniform (no microseconds)
end_time2 = dt_time(end_time2.hour, end_time2.minute, end_time2.second)
# ###############################################################################################################################
# End of Time functionality variables >>>----------------------------------------------------------------------------------
#################################################################################################################################

# ###############################################################################################################################
# This is the "Buy" loop --------------------------------------------------------------------------------------------------------
# ###############################################################################################################################
while True:
    # First, check if buying time is over...
    if central_time > end_time:
        print(f"The current time is {central_time}. Your 'buy' range ended at {end_time}.")
        print()
        break
    if num_of_loops > 20:
        # Log-in again just in case system needs it every so often...
        exchange_client = ExchangeClient(exchange_api_base, email, password)
        # Get (current) exchange status
        exchange_status = exchange_client.get_exchange_status()
        print(exchange_status)
        print()  # Empty line after for readability
        num_of_loops = 0  # reset loop count

    if yes_or_no == "Yes":
        get_buy_mrkt_info()  # For "yes" contract
    elif yes_or_no == "No":
        get_buy_mrkt_info_no()  # For "no" contract
    else:
        print("Error: yes_or_no variable should be set to either 'Yes' or 'No'")
        quit()

    # This line is repeated in the 'while' loop because time always updates (is not constant)
    central_time = dt.now(tz=pytz.timezone('US/Central')).time()

    # Create new time object without microseconds
    central_time = dt_time(central_time.hour, central_time.minute, central_time.second)
    print(central_time)
    print()

    # Check if buying time is over before going into 'buyblock'
    if central_time > end_time:
        break

    # TO DO: ********************************************************************************************************************
    # Next step: Log trades should record the actual price the contract was purchased at, since the avg_yes or no is only an average between the (current) ask and bid price, and not the actual (current) purchase price. Figure out how to log this information. Perhaps display both in the log file, (what the avg_yes/no was, and what the purchase price was).
    # ***************************************************************************************************************************

    # ##### 'buyblock' ##### ---------------------------------------------------------------------------------------
    disable_buyblock = False
    if disable_buyblock:
        pass
    else:
        # Implement conditional buying
        # "YES" SIDE *****
        if yes_or_no == "Yes":
            # If the price is right...
            if price_low_end <= avg_yes <= price_high_end:
                # If the time is right...
                if start_time <= central_time <= end_time:
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
                    if logging_trades:
                        log_trade(action='Buy', timestamp=central_time, details=avg_yes, side=yes_or_no)
                    else:
                        pass
                    print(f"Buying conditions met, a total of {contracts_bought} {yes_or_no} contract(s) have been purchased.")
                    if logging_trades:
                        print("Trade logged in .txt file.")
                    print()
                    num_of_loops += 1
                    if contracts_bought < contract_ceiling:
                        time.sleep(900)  # sleep for longer after a "buy" to make sure price is staying consistent
                        continue
                    else:
                        print("Buy ceiling has been met.")  # buy ceiling has been met
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
        elif yes_or_no == "No":
            # If the price is right...
            if price_low_end <= avg_no <= price_high_end:
                # If the time is right...
                if start_time <= central_time <= end_time:
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
                    if logging_trades:
                        log_trade(action='Buy', timestamp=central_time, details=avg_no, side=yes_or_no)
                    else:
                        pass
                    print(f"Buying conditions met, a total of {contracts_bought} {yes_or_no} contract(s) have been purchased.")
                    if logging_trades:
                        print("Trade logged in .txt file.")
                    print()
                    num_of_loops += 1
                    if contracts_bought < contract_ceiling:
                        time.sleep(900)  # sleep for longer after a "buy" to make sure price is staying consistent
                        continue
                    else:
                        print("Buy ceiling has been met.")  # buy ceiling has been met
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
            print("Error: yes_or_no variable should be set to either 'Yes' or 'No'")
            quit()

###### FORMAT FOR ORDER CREATION #######################################################
# # create_order(self,
# # ticker:str,
# # client_order_id:str,
# # side:str,
# # action:str,
# # count:int,
# # type:str,
# # yes_price:Optional[int]=None,
# # no_price:Optional[int]=None,
# # expiration_ts:Optional[int]=None,
# # sell_position_floor:Optional[int]=None,
# # buy_max_cost:Optional[int]=None,
# # ):
##########################################################################################

# ###############################################################################################################################
# This is the "Sell" loop ------------------------------------------------------------------------------------------------------
# ###############################################################################################################################
while True:
    # The first thing to check is if any contracts were bought...
    if contracts_bought < 1:
        print(f"The number of contracts purchased is {contracts_bought}. Exiting the 'Sell loop'.")
        print()
        break
    # The second thing is whether or not it's still 'sell' time...
    if central_time >= end_time2:
        print("The time parameters for buying/selling have expired.")
        print()
        break
    if num_of_loops > 20:
        # Log-in again just in case system needs it every so often...
        exchange_client = ExchangeClient(exchange_api_base, email, password)
        # Get (current) exchange status
        exchange_status = exchange_client.get_exchange_status()
        print(exchange_status)
        print()  # Empty line after for readability
        num_of_loops = 0  # reset loop count

    if yes_or_no == "Yes":
        get_buy_mrkt_info()  # For "yes" contract
    elif yes_or_no == "No":
        get_buy_mrkt_info_no()  # For "no" contract
    else:
        print("Error: yes_or_no variable should be set to either 'Yes' or 'No'")
        quit()

    # This line is repeated in the 'while' loop because time always updates (is not constant)
    central_time = dt.now(tz=pytz.timezone('US/Central')).time()

    # Create new time object without microseconds
    central_time = dt_time(central_time.hour, central_time.minute, central_time.second)
    print(central_time)
    print()

    # ##### 'sellblock' ##### ---------------------------------------------------------------------------------------
    disable_sellblock = False
    if disable_sellblock:
        pass
    else:
        # Implement conditional selling
        # "YES" SIDE *****
        if yes_or_no == "Yes":
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
                if logging_trades:
                    log_trade(action='Sell', timestamp=central_time, details=avg_yes, side=yes_or_no)
                else:
                    pass
                print(f"Selling conditions met, a total of {contracts_sold} {yes_or_no} contract(s) have been sold.")
                print()
                if logging_trades:
                    print("Trade logged in .txt file.")
                    print()
                num_of_loops += 1
                if contracts_sold < contracts_bought:
                    time.sleep(200)  # Approximately 3 mins. (Sell time sleep quicker than buy sleep)
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
        elif yes_or_no == "No":
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
                if logging_trades:
                    log_trade(action='Sell', timestamp=central_time, details=avg_no, side=yes_or_no)
                else:
                    pass
                print(f"Selling conditions met, a total of {contracts_sold} {yes_or_no} contract(s) have been sold.")
                print()
                if logging_trades:
                    print("Trade logged in .txt file.")
                    print()
                num_of_loops += 1
                if contracts_sold < contracts_bought:
                    time.sleep(200)  # Approximately 3 mins. (Sell time sleep quicker than buy sleep)
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

quit()

# calculate ROI for a strategy
# kalshi_ROI(win_ratio, contract_price, stop_loss)
kalshi_ROI(80, 70, 21)
