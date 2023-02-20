from flask import Flask, request,render_template,jsonify
import json,os,time
import plotly.graph_objs as go
import sys,datetime

app = Flask(__name__)

CHECK_CONNECTION = {}
CHECK_COMPLETED = {}

CHECK_CDSL_NETWORK_CONNECTED = {}

COMPLETING_ESP32 = [
    "ESP_27B055",
    "ESP_7B0B85",
    "ESP_A97611",
    "ESP_A974B5"
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
"A" : "ESP_27B055",
"B" : "ESP_7B0B85",
"C" : "ESP_A97611",
"D" : "ESP_A974B5",
"E" : "ESP_A966F1",
"F" : "ESP_A9F0D9",
"G" : "ESP_5242C9",
"H" : "ESP_529B71",
"I" : "ESP_5267D1",
"J" : "ESP_51621D",
"K" : "ESP_60981D",
"L" : "ESP_530955"
}

espIpDict = {
    "A" : "192.168.100.158",
    "B" : "192.168.100.164",
    "C" : "192.168.100.177",
    "D" : "192.168.100.130",
    "E" : "192.168.100.92",
    "F" : "192.168.100.122",
    "G" : "192.168.100.138",
    "H" : "192.168.100.124",
    "I" : "192.168.100.173",
    "J" : "192.168.100.147",
    "K" : "192.168.100.46",
    "L" : "192.168.100.55"
}

espNameDict = {
    "ESP_27B055":"A",
    "ESP_7B0B85":"B",
    "ESP_A97611":"C",
    "ESP_A974B5":"D",
    "ESP_A966F1":"E",
    "ESP_A9F0D9":"F",
    "ESP_5242C9":"G",
    "ESP_529B71":"H",
    "ESP_5267D1":"I",
    "ESP_51621D":"J",
    "ESP_60981D":"K",
    "ESP_530955":"L"
}

log_file_path = "/home/sugi/esp32_connection/flask_run/debug.log"
# sys.stdout = open(log_file_path, "w")


def printF(textF):
    with open(log_file_path,"a") as f:
        f.write(textF)
        f.write("\n")
    
def init_check_connection():
    global CHECK_CONNECTION
    for k,v in espIdList.items():
        CHECK_CONNECTION[v] = False

def init_check_complete():
    global CHECK_COMPLETED
    for k,v in espIdList.items():
        CHECK_COMPLETED[v] = False

def init_check_cdsl_connection():
    global CHECK_CDSL_NETWORK_CONNECTED
    for k,v in espIdList.items():
        CHECK_CDSL_NETWORK_CONNECTED[v] = False

def get_key(value):
    for key, val in espIdList.items():
        if val == value:
            return key
    return None

def transpose(matrix):
    return [list(x) for x in zip(*matrix)]



## データのグラフ用ページ
@app.route('/graph')
def display_graph():
    lists = {}
    path = "/home/sugi/esp32_connection/battery_data"
    file_names = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file_name in file_names:
        with open(os.path.join(path, file_name)) as f:
            lists[file_name] = [float(line.strip()) for line in f]
    
    fileNameList = list()
    all_lists =list()
    length_sum = list()
    for k,v in lists.items():
        fileNameList.append(k)
        all_lists.append(v)
        length_sum.append(len(v))
    
    length_max = max(length_sum) + 10
    
    labels = list()
    for i in range(1,length_max):
        labels.append(i)
    
    return render_template('graph.html', data=lists, labels=labels)

##データ閲覧用ページ
@app.route('/display')
def display():
    timeDict = {}
    dataDict = {}
    countDict = {}
    length_data = 0
    for k, v in espIdList.items():
        fileName = f"/home/sugi/esp32_connection/battery_data/{v}.csv"
        timeList = list()
        dataList = list()
        countList = list()
        with open(fileName,"r") as f:
            for line in f:
                dataSplit = line.split(",")
                time = dataSplit[0]
                data = float(dataSplit[1])
                count = int(dataSplit[2])
                timeList.append(time)
                dataList.append(data)
                countList.append(count)
            timeDict[v] = timeList
            dataDict[v] = dataList
            countDict[v] = countList
            if length_data < len(dataList):
                length_data = len(dataList)
    
    return render_template('table.html',countDict=countDict,length_data=length_data,espNameDict=espNameDict,ESP32_NAME_LIST=ESP32_NAME_LIST,timeDict=timeDict,dataDict=dataDict)


@app.route("/")
def index():
    # 一応のメインページ 画面遷移を担当するかも
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return render_template('index.html', routes=routes)

@app.route("/status")
def status():
    return render_template('status_table.html', CHECK_CONNECTION=CHECK_CONNECTION,CHECK_COMPLETED=CHECK_COMPLETED,CHECK_CDSL_NETWORK_CONNECTED=CHECK_CDSL_NETWORK_CONNECTED,espNameDict=espNameDict)

@app.route("/init_status",methods=['GET', 'POST'])
def init_status():
    init_check_complete()
    init_check_connection()
    init_check_cdsl_connection()
    return "<h2><a href='/status'>back</a></h2>"

@app.route('/cdsl_network_connect', methods=['GET'])
def cdsl_network_connect():
    global CHECK_CDSL_NETWORK_CONNECTED
    
    espId = request.args.get('espid')
    data = request.args.get('data')
    
    printF(f"espid : {espId} ({get_key(espId)})")
    printF(f"data : {data}")
    
    CHECK_CDSL_NETWORK_CONNECTED[espId] = True
    
    printF("----")
    for k,v in CHECK_CDSL_NETWORK_CONNECTED.items():
        printF(f"{k} ({get_key(k)}) : {v}")
    printF(f"total : {len(CHECK_CDSL_NETWORK_CONNECTED)}")
    printF("----")
    return "success"

@app.route('/init_network_recieve', methods=['GET'])
def receive_data():
    global CHECK_CONNECTION
    global CHECK_COMPLETED
    # request.argsからGETパラメータを取得する
    # クエリパラメータを取得する
    
    espId = request.args.get('espid')
    data = request.args.get('data')
    transfer_espid = request.args.get('transfer_espid')
    route = request.args.get('route')
    
    printF(f"espid : {espId} ({get_key(espId)})")
    printF(f"data : {data}")
    printF(f"transfer_esp : {transfer_espid} ({get_key(transfer_espid)})")
    printF(f"temporary_route : {route}")
    
    if transfer_espid != None:
        CHECK_CONNECTION[transfer_espid] = True
    else:
        CHECK_CONNECTION[espId] = True
        if espId in COMPLETING_ESP32:
            CHECK_COMPLETED[espId] = True
    printF("----")
    for k,v in CHECK_CONNECTION.items():
        printF(f"{k} ({get_key(k)}) : {v}")
    printF(f"total : {len(CHECK_CONNECTION)}")
    printF("----")
    
    if data == "resist_complete":
        CHECK_COMPLETED[transfer_espid] = True
    for k,v in CHECK_COMPLETED.items():
        printF(f"{k} ({get_key(k)}) : {v}")
    printF(f"total : {len(CHECK_COMPLETED)}")
    printF("----")
    
    return 'success'


BATTERY_LEVEL = dict()
@app.route("/battery_recieve",methods=['GET'])
def battery_recieve():
    global BATTERY_LEVEL
    # 受信されるデータ : espid=ESP_27B055&data=9999.912&weight=0&
    espId = request.args.get('espid')
    data = request.args.get('data')
    weight = request.args.get('transfer_espid')
    transfer_espid = request.args.get('transfer_espid')
    timeStamp = request.args.get("timestamp")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+9*60*60))
    
    printF(f"""
        TIME            : {current_time}
        recieve ESP32   : {espId} ({get_key(espId)})
        from ESP32      : {transfer_espid} ({get_key(transfer_espid)})
        battery level   : {data}
        weight          : {weight}
        timeStamp          : {timeStamp}
    """)
    
    if transfer_espid not in BATTERY_LEVEL:
        BATTERY_LEVEL[transfer_espid] = []
    BATTERY_LEVEL[transfer_espid].append(data)
    fileName = f"/home/sugi/esp32_connection/battery_data/{transfer_espid}.csv"
    writeData = f"{str(current_time)},{data},{timeStamp}"
    with open(fileName, 'a') as f:
        f.write(writeData)
        f.write('\n')
    
    for k, v in BATTERY_LEVEL.items():
        printF(f"- - - {k} ({get_key(k)}) - - -")
        for batteryN in v:
            printF(f"{batteryN}[mA]")
    return "success"


if __name__ == '__main__':
    init_check_complete()
    init_check_connection()
    init_check_cdsl_connection()
    app.run(debug=True,host="0.0.0.0",threaded=True)
