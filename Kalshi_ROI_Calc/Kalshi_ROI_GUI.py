import PySimpleGUI as sg
from Kalshi_ROI import kalshi_ROI

ROI = ''

# Function to check if user input is a number
def is_int(value):
    try:
        int_value = int(value)
        return True
    except ValueError:
        return False

sg.theme('LightGreen1')
layout = [
    [sg.VPush()],
    [sg.Text("Win Ratio (%) :", font = 'Calibri 16'), sg.Push(), sg.InputText(size=(5, 0), pad = (10, 7), key = '-WINRATE-')],
    [sg.Text("Contract Price (avg) :", font = 'Calibri 16'), sg.Push(), sg.InputText(size=(5, 0), pad = (10, 7), key = '-AVGPRICE-')],
    [sg.Text("Stop-loss (avg) :", font = 'Calibri 16'), sg.Push(), sg.InputText(size=(5, 0), pad = (10, 7), key = '-STOPLOSS-')],
    [sg.VPush()],
    [sg.VPush()],
    [sg.Push(), sg.Button('Submit', size = (14, 1), pad = (0, 7), key = '-SUBMIT-'), sg.Push()],
    [sg.Push(), sg.Text("____________________________________________", font = 'Calibri 16'), sg.Push()],
    [sg.VPush()],
    [sg.Push(), sg.Text("-----ROI-----", font = 'Calibri 20', pad = (2, 15)), sg.Push()],
    [sg.Push(), sg.Text('', font = 'Calibri 20', key = '-ROI-'), sg.Push()],
    [sg.VPush()]
]

window = sg.Window('Kalshi ROI Calculator', layout, size = (320, 325))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == '-SUBMIT-':
        win_ratio = (values['-WINRATE-'])
        contract_price = (values['-AVGPRICE-'])
        stop_loss = (values['-STOPLOSS-'])
        if is_int(win_ratio) and \
                is_int(contract_price) and \
                is_int(stop_loss):
            # Call imported function
            # to calculate ROI
            kalshi_ROI(int(win_ratio), int(contract_price), int(stop_loss))
            window['-ROI-'].update(f'{ROI}%')
        else:
            sg.Popup("Make sure all three value fields are filled with integer values.")

window.close()
