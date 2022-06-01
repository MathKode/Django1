
import requests
import shutil

#49.269817,6.134137,19
#49.271075,6.179451,19
x=271075
y=179451
v=9181
z=19
scale=1
url = f"https://sat-cdn3.apple-mapkit.com/tile?style=7&size=1&scale={scale}&z={z}&x={x}&y={y}&v={v}&accessKey=1653754290_4573888296627452574_%2F_yBVBLKoHps5Yvy5phxOFde%2Fbap%2FUXL2d1Z3J6%2BPE1tA%3D"

response = requests.get(url, stream=True)
with open('TEST.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response