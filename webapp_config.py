default_app_name="LOST FOUND APP"
default_app_desc="LOST FOUND APP"
default_email_domain="@gmail.com"
default_bg="linear-gradient(to bottom right, #2A7B9B, #EDDD53)"
default_pad="2rem"
default_b1="green"
default_b2="red"
default_h="purple"

from os import path, makedirs
from pathlib import Path
while True:
    logo_path=input("Logo Path (PNG Format): ").strip()
    try:
        if logo_path[-4:]!=".png":
            print("Please provide .png format")
            continue
        Path(path.join("webapp/assets","logo.png")).write_bytes(Path(logo_path).read_bytes())
    except:
        print("NO SUCH FILE")
        continue
    break
while True:
    banner_path=input("Banner Path (PNG Format): ").strip()
    try:
        if logo_path[-4:]!=".png":
            print("Please provide .png format")
            continue
        Path(path.join("webapp/assets","banner.png")).write_bytes(Path(banner_path).read_bytes())
    except:
        print("NO SUCH FILE")
        continue
    break
app_name=input(f"App Name ['{default_app_name}']: ").strip()
if app_name=="": app_name=default_app_name
app_desc=input(f"App Description ['{default_app_desc}']:").strip()
if app_desc=="": app_desc=default_app_desc
email_domain=input(f"Email Domain ['{default_email_domain}']: ").strip()
if email_domain=="": email_domain=default_email_domain
bg=input(f"CSS Background Style ['{default_bg}']: ").strip()
if bg=="": bg=default_bg
pad=input(f"CSS Padding ['{default_pad}']: ").strip()
if pad=="": pad=default_pad
b1=input(f"Button Color 1 ['{default_b1}']: ").strip()
if b1=="": b1=default_b1
b2=input(f"Button Color 2 ['{default_b2}']: ").strip()
if b2=="": b2=default_b2
h=input(f"Hover Color ['{default_h}']: ").strip()
if h=="": h=default_h
if not path.exists("./configs"):
    makedirs("./configs")
config_file=open("./configs/config.txt","w")
config_file.write("\n".join([app_name, app_desc, email_domain, bg, pad, b1, b2, h]))