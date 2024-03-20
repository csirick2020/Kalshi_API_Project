# Kalshi ROI Calculator

ROI = ''

def kalshi_ROI(win_ratio, contract_price, stop_loss):
    cost_of_contract = contract_price / 100
    stop_loss_cost = stop_loss / 100
    total_gain = win_ratio * (1.00 - cost_of_contract)
    total_loss = (100 - win_ratio) * (cost_of_contract - stop_loss_cost)
    net_gain = total_gain - total_loss
    global ROI
    ROI = round((net_gain / contract_price) * 100, 2)
    return ROI


if __name__ == "__main__":
    win_ratio = int(input("Please enter a win ratio...\n(Example: '60' (for 60%))\n"))
    contract_price = int(input("Please enter the (average) contract price in your buying scenario\n(Example: '70' for $0.70)\n"))
    stop_loss = int(input("Please enter your (average) 'stop-loss' price\n(Example: '30' for $0.30)\n"))
    kalshi_ROI(win_ratio, contract_price, stop_loss)
    print()
    print(f"ROI (before fees): {ROI} %")
