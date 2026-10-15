import os
import shutil
import zipfile

src = r"d:\A\A_5chai\honey_pot\hinh_anh_chuong_3"
dst = r"d:\A\A_5chai\honey_pot\chapter3_evidence"
zip_path = r"d:\A\A_5chai\honey_pot\chapter3_evidence.zip"

if os.path.exists(dst):
    shutil.rmtree(dst)
os.makedirs(dst, exist_ok=True)

files = os.listdir(src)
print(f"Copying {len(files)} files to {dst}...")
for f in files:
    s = os.path.join(src, f)
    d = os.path.join(dst, f)
    if os.path.isfile(s):
        shutil.copy2(s, d)
        print(f"  -> Copied {f} ({os.path.getsize(d)} bytes)")

print(f"Creating zip file {zip_path}...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for f in os.listdir(dst):
        p = os.path.join(dst, f)
        if os.path.isfile(p):
            zipf.write(p, arcname=f)

print(f"Zip created successfully! Size: {os.path.getsize(zip_path)} bytes")
