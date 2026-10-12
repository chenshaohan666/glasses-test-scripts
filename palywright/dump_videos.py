import subprocess
import os


files = ["206","207","208","210"]
pkg = "com.motorola.glasses"
src_base = "files/gallery_private_media/temp_processing"

for fname in files:
    cmd = [
        "adb", "exec-out",
        "run-as", pkg,
        "cat", f"{src_base}/{fname}"
    ]
    print(f"dump {fname} ...")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw_data, err = proc.communicate()
    out_path = f"{fname}.raw"
    with open(out_path, "wb") as f:
        f.write(raw_data)
    print(f" -> {out_path}  size:{len(raw_data)} bytes")
    if err:
        print(f"err:{err.decode('utf8','ignore')}")

print("全部导出完成")
