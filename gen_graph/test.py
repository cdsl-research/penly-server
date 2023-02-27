import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import gnuplotlib as gp



COMPLETING_ESP32 = [
    "ESP_27B055",
    "ESP_7B0B85",
    "ESP_A97611"
]

ESP32_NAME_LIST = [
    "ESP_27B055",
    "ESP_7B0B85",
    "ESP_A97611",
    "ESP_A974B5",
    "ESP_A966F1",
    "ESP_A9F0D9",
    "ESP_5242C9",
    "ESP_529B71",
    "ESP_5267D1",
    "ESP_51621D",
    "ESP_60981D",
    "ESP_530955"
]

espIdList = {
"B" : "ESP_27B055",
"A1" : "ESP_7B0B85",
"A2" : "ESP_A97611",
"A3" : "ESP_A974B5",
"A4" : "ESP_A966F1",
"A5" : "ESP_A9F0D9",
"sA" : "ESP_5242C9",
"sB" : "ESP_529B71",
"sC" : "ESP_5267D1",
"sD" : "ESP_51621D",
"sE" : "ESP_60981D",
"sF" : "ESP_530955"
}

espNameDict = {
    "ESP_27B055":"B",
    "ESP_7B0B85":"A1",
    "ESP_A97611":"A2",
    "ESP_A974B5":"A3",
    "ESP_A966F1":"A4",
    "ESP_A9F0D9":"A5",
    "ESP_5242C9":"sA",
    "ESP_529B71":"sB",
    "ESP_5267D1":"sC",
    "ESP_51621D":"sD",
    "ESP_60981D":"sE",
    "ESP_530955":"sF"
}

CONNECTION_CDSL = {
    "B" : "192.168.100.158",
    "A1" : "192.168.100.164",
    "A2" : "192.168.100.177"
}

GROUPS_1 = [
    ["B","A1"],
    ["B","A1"],
    ["A1,A2"],
    ["A1","A2"]
]
GROUPS_2 = [
    ["A3","A4"],
    ["A3","A4"],
    ["A3,A4,sA"],
    ["sA,sB"]
]
GROUPS_3 = [
    ["sC","sD"],
    ["sD","sC"]
]

HOP_DEVICE_NUM = [3,4,2,2]



def graph_generator():
    timestamp_length = {}
    
    timeDict = {}
    dataDict = {}
    for k, v in espIdList.items():
        fileName = f"/home/sugi/esp32_connection/battery_data/{v}.csv"
        timeList = list()
        dataList = list()
        timestamps = []
        values = []
        timestamp_length_count = 0
        print(f"fileName : {fileName}")
        with open(fileName,"r") as f:
            for line in f:
                dataSplit = line.split(",")
                time = dataSplit[0]
                data = float(dataSplit[1])
                timeStamp = int(dataSplit[2])
                print(f"{time} >> {data} >> {timeStamp}")
                timeList.append(time)
                timestamp = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
                timestamps.append(timestamp)
                dataList.append(data)
                values.append(data)
                timestamp_length_count += 1
            timestamp_length[v] = timestamp_length_count
            plt.plot(timestamps,values,label=v,marker="o", markeredgewidth=0,markersize=3)
        timeDict[fileName] = timeList
        dataDict[fileName] = dataList
    
    
    
    # # 折れ線グラフを描画
    # plt.plot(timestamps[:5], values[:5], label='ESP_27B055')
    # plt.plot(timestamps[5:10], values[5:10], label='ESP_7B0B85')
    # plt.plot(timestamps[10:], values[10:], label='ESP_A97611')

    # Set the font size and font type
    plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

    # Enable grid and set style
    plt.grid(linestyle='--', color='black', linewidth=0.5)

    # Display the legend with a more appropriate location
    plt.legend(loc='lower left', fontsize='small', facecolor='white', framealpha=0.7)

    # Format the x-axis ticks to display dates in a more readable format
    plt.gcf().autofmt_xdate()

    # Set the graph title and axis labels
    plt.title('Graph', fontsize=14, fontweight='bold', color='black')
    plt.xlabel('Time', fontsize=12, color='black')
    plt.ylabel('Value', fontsize=12, color='black')

    # Save the graph with a high-resolution DPI (dots per inch)
    plt.savefig('graph4.png', dpi=300)




# def graph_generator():
#     timestamp_length = {}
    
#     timeDict = {}
#     dataDict = {}
#     for k, v in espIdList.items():
#         fileName = f"/home/sugi/esp32_connection/battery_data/{v}.txt"
#         timeList = list()
#         dataList = list()
#         timestamps = []
#         values = []
#         timestamp_length_count = 0
#         print(f"fileName : {fileName}")
#         with open(fileName,"r") as f:
#             for line in f:
#                 dataSplit = line.split(",")
#                 time = dataSplit[0]
#                 data = float(dataSplit[1])
#                 print(f"{time} >> {data}")
#                 timeList.append(time)
#                 timestamp = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
#                 timestamps.append(timestamp)
#                 dataList.append(data)
#                 values.append(data)
#                 timestamp_length_count += 1
#             timestamp_length[v] = timestamp_length_count
        
#         timeDict[fileName] = timeList
#         dataDict[fileName] = dataList
    
#     gp.plot(timeDict.values(), dataDict.values(), terminal='png', unset='grid', 
#             style='linespoints', legend=espIdList.values(), title='Graph',
#             xlabel='Time', ylabel='Value')

#     plt.title('Graph')
#     plt.xlabel('Time')
#     plt.ylabel('Value')
#     plt.legend()
#     plt.gcf().autofmt_xdate()
#     plt.savefig('graph2.png')


def main():
    graph_generator()

if __name__ == "__main__":
    main()