import os
import keyboard
import numpy as np
import pandas as pd
from datetime import datetime
import serial, serial.tools.list_ports

# save_path = r"C:\Users\pr19556\OneDrive - Applied Medical\Documents\ER 20022640 Lap Fusion JFF EQ Updates\Programs\VoyantJFFEQ_Update\Data"
save_path = os.getcwd() + r"\Data"

def get_vals(test_num):
    force_data, data_values = np.array([], dtype = float), 0
    print(f"\n----- TEST {test_num} START -----")
    print(f"\nTest Num: {test_num}")
         
    while data_values <= 69:
        try: 
            data_raw = ser.readline().decode('ascii', errors = 'replace').strip()
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
            continue
        
        print(data_raw)
        force_data = np.append(force_data, data_raw)
        data_values = len(force_data)
        
    print(f"\n----- TEST {test_num} END -----\n")

    # print(force_data)
    return force_data 


for port in serial.tools.list_ports.comports():
    info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer, "Hwid": port.hwid})
    if port.manufacturer == "FTDI":
        ser_info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer, "Hwid": port.hwid})

        print(ser_info["Name"])

try:
    ser = serial.Serial(port = ser_info["Name"], baudrate = 115200, timeout = None)
    print(f"\n----- Connected to {ser_info['Name']} -----\n")

    print("Press Space to Begin Test. . .\n")
  
    test_num, flag = 1, True
    keyboard.wait("space")
    print("\n----- START TEST-----\n")

    final_data = {}
    ser.close()

    while True:
        try:
            ser.open()
            new_data = {str(test_num): get_vals(test_num)}
            test_num = test_num + 1
            ser.close()
            final_data.update(new_data)

        except KeyboardInterrupt:
            print("\n----- END TEST -----\n")

            df = pd.DataFrame(final_data)
        
            file_name = "ForceData_" + str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".csv"
            file_path = save_path + "\\" + file_name

            print(f"File Name: {file_name}")
            print(f"File Directory: {file_path}")

            print("\nForce Value Results\n")
            print(df)
            print(" ")
            
            df.to_csv(file_path, index = False)

            ser.close()
            print(f"\n----- Disconnected from {ser_info['Name']} -----\n")
            break

except serial.SerialException:
    print("\n----- Serial Connection Failed -----\n")

