import os, uuid, json, base64, platform, tarfile
from subprocess import Popen
from urllib.request import urlopen
from urllib.request import urlretrieve

HOME = os.path.expanduser("~")

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
  
  found = findPackageR('v2fly/v2ray-core', f'v2ray-{platform.system().lower()}-64.zip', all_=True)
  downUrl = found['assets']['browser_download_url']
  print(f"Installing v2ray {found['tag_name']} ...")
  os.system(f'mkdir v2raybin && cd v2raybin && curl -L -H "Cache-Control: no-cache" -o v2ray.zip {downUrl}  && unzip v2ray.zip')
  CONFIG_JSON1="{\"log\":{\"access\":\"\",\"error\":\"\",\"loglevel\":\"warning\"},\"inbound\":{\"protocol\":\"vmess\",\"port\":"
  CONFIG_JSON2=",\"settings\":{\"clients\":[{\"id\":\""
  CONFIG_JSON3="\",\"alterId\":64}]},\"streamSettings\":{\"network\":\"ws\"}},\"inboundDetour\":[],\"outbound\":{\"protocol\":\"freedom\",\"settings\":{}}}"
  with open("config.json","w") as f:
    f.write(CONFIG_JSON1+str(port)+CONFIG_JSON2+id+CONFIG_JSON3)
  d=json.loads('{"add":"{0}","aid":"64","host":"","id":"{1}","net":"ws","path":"","port":"80","ps":"1","tls":"","type":"none","v":"2"}')
  d["add"]="<<tunnelURL>>"
  d["id"]=ID
  config="vmess://"+base64.b64encode(json.dumps(d).encode()).decode("utf-8")
  print(config)
  return Popen("v2raybin/v2ray")

def wetty(port=4343):
  os.makedirs('tools/temp', exist_ok=True)
  wettyBF = 'https://github.com/biplobsd/temp/releases/download/v0.001/wetty.tar.gz'
  fileSN = 'tools/temp/wetty.tar.gz'
  urlretrieve(wettyBF, fileSN)
  with tarfile.open(fileSN, 'r:gz') as t:t.extractall('tools/')
  os.remove(fileSN)
  return Popen(f'tools/wetty/wetty --port {port} --bypasshelmet -b "/" -c "/bin/bash"'.split(), cwd=os.getcwd())

def noVnc():
  password = "12345678"
  os.makedirs("tools/noVnc", exist_ok=True)
  os.makedirs(f'{HOME}/.vnc', exist_ok=True)
  os.system("sudo apt update -y && sudo apt install -y icewm firefox tightvncserver autocutsel xterm")
  os.system('echo "{password}" | vncpasswd -f > ~/.vnc/passwd')
  data = """
#!/bin/bash
xrdb $HOME/.Xresources
xsetroot -solid black -cursor_name left_ptr
autocutsel -fork
icewm-session &
"""
  with open(f'{HOME}/.vnc/xstartup', 'w+') as wNow:
    wNow.write(data)
  os.chmod(f'{HOME}/.vnc/xstartup', 0o755)
  os.chmod(f'{HOME}/.vnc/passwd', 0o400)
  Popen('sudo vncserver :1 -geometry 1440x870 -economictranslate -dontdisconnect'.split())
  
  urlF = findPackageR('geek1011/easy-novnc', 'easy-novnc_linux-64bit')
  output_file = "tools/noVnc/easy-noVnc_linux-64bit"
  urlretrieve(urlF, output_file)
  os.chmod(output_file, 0o755)
  
  print(f'http://0.0.0.0:6080/vnc.html?autoconnect=true&password={password}&path=vnc&resize=scale&reconnect=true&show_dot=true')
  return Popen("./easy-noVnc_linux-64bit --addr 0.0.0.0:6080 --port 5901".split(), cwd="tools/noVnc/")      

ID = str(uuid.uuid4())
print("Setting up v2ray server ... ")
v2ray(ID, 9910)

if platform.system() == "Linux":
  print("Installing wetty ...")
  wetty()
        
  print("Setting up noVnc ...")
  noVnc()

