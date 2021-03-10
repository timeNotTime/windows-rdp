import os, uuid, json, base64
from subprocess import Popen
from urllib.request import urlopen

#v2ray
def findPackageR(id_repo, p_name, tag_name=False, all_=False):
  for rawData in json.load(urlopen(f"https://api.github.com/repos/{id_repo}/releases")):
    if tag_name:
      if rawData['tag_name'] != tag_name:
        continue

    for f in rawData['assets']:
      if p_name == f['browser_download_url'][-len(p_name):]:
        rawData['assets'] = f 
        return f['browser_download_url'] if not all_ else rawData
  raise Exception("not found or maybe api changed!\n Try again with Change packages name")
  
def v2ray(id=None,port=9999):
  
  found = findPackageR('v2fly/v2ray-core', 'v2ray-windows-64.zip', all_=True)
  downUrl = found['assets']['browser_download_url']
  print(f"Installing v2ray {found['tag_name']} ...")
  os.system(f'mkdir v2raybin && cd v2raybin && curl -L -H "Cache-Control: no-cache" -o v2ray.zip {downUrl}  && unzip v2ray.zip')
  CONFIG_JSON1="{\"log\":{\"access\":\"\",\"error\":\"\",\"loglevel\":\"warning\"},\"inbound\":{\"protocol\":\"vmess\",\"port\":"
  CONFIG_JSON2=",\"settings\":{\"clients\":[{\"id\":\""
  CONFIG_JSON3="\",\"alterId\":64}]},\"streamSettings\":{\"network\":\"ws\"}},\"inboundDetour\":[],\"outbound\":{\"protocol\":\"freedom\",\"settings\":{}}}"
  with open("config.json","w") as f:
    f.write(CONFIG_JSON1+str(port)+CONFIG_JSON2+id+CONFIG_JSON3)
  return Popen("v2raybin/v2ray")

ID = str(uuid.uuid4())
print("Setting up v2ray server ... ")
v2ray(ID, 9910)
d=json.loads('{"add":"{0}","aid":"64","host":"","id":"{1}","net":"ws","path":"","port":"80","ps":"1","tls":"","type":"none","v":"2"}')
d["add"]="<<tunnelURL>>"
d["id"]=ID
config="vmess://"+base64.b64encode(json.dumps(d).encode()).decode("utf-8")
print(config)
