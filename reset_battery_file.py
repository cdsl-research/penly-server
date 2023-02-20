import os

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

for k,v in espIdList.items():
    fileName = f"battery_data/{v}.csv"
    if os.path.exists(fileName):
        print("File already exists")
        with open(fileName,"w") as f:
            f.truncate(0)