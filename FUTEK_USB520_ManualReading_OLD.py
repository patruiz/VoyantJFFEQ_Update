import os
import keyboard
import numpy as np
import pandas as pd
from datetime import datetime
import serial, serial.tools.list_ports

save_path = os.getcwd() + r"\Data"

for port in serial.tools.list_ports.comports():
    info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer, "Hwid": port.hwid})
    if port.manufacturer == "FTDI":
        ser_info = dict({"Name": port.name, "Description": port.description, "Manufacturer": port.manufacturer, "Hwid": port.hwid})

try:
    ser = serial.Serial(port = ser_info["Name"], baudrate = 115200, timeout = None)
    print(f"\n----- Connected to {ser_info['Name']} -----\n")
    ser.close()

    print("Press Space to Take Record Values . . .\n")
  
    final_data = []

    try:

        test_num, flag = 1, True
        while True:
    
            keyboard.wait("space")
            ser.open()
            force_data, data_values = np.array([], dtype = float), 0
            print(f"\nTest Num: {test_num}")
                                                            
            while data_values < 25:
                try:
                    data_raw = ser.readline().decode('utf-8', errors = 'replace').strip()
                except UnicodeDecodeError as e:
                    print(f"UnicodeDecodeError: {e}")
                    continue
                
                data_raw = data_raw.replace("\n", '').replace('\r', '') 
                if data_raw != "****************":
                    data_raw = round(float(data_raw.split()[0]), 4)
                    force_data = np.append(force_data, data_raw)
                
                data_values = len(force_data)

            force_value = round(float(np.max(force_data)), 4)
            print(f"Force: {force_value}")

            data_new = round(float(np.average(force_data)), 4)
            final_data.append(data_new)

            test_num = test_num + 1
            ser.close()

    except KeyboardInterrupt:

        print("\n----- End Test -----\n")
        
        df = pd.DataFrame(final_data, columns = ["Force (lbf)"])
        
        now = datetime.now()
        file_name = "Force Data " + now.strftime("%Y-%m-%d %H-%M-%S") + ".csv"
        print(f"File Name: {file_name}")
        print(f"File Directory: {save_path}")

        print("\nForce Value Results\n")
        print(df)
 
        os.chdir(save_path)       
        df.to_csv(file_name, index = True) 

        ser.close()
        print(f"\n----- Disconnected from {ser_info['Name']} -----\n")
    
except serial.SerialException:
    print("\n----- Serial Connection Failed -----\n")





