import os
import zipfile
from pathlib import Path
from ultralytics import YOLO

# -------------------------------
# 1. SET YOUR ZIP FILE NAME
# -------------------------------
zip_file_path = "D:/FORMORA/Plant disease prediction.v1i.yolov8.zip"  # Change to your dataset zip file

# -------------------------------
# 2. UNZIP DATASET
# -------------------------------
extract_dir = Path("dataset")
extract_dir.mkdir(exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print(f"✅ Dataset unzipped to: {extract_dir.resolve()}")

# -------------------------------
# 3. FIND data.yaml
# -------------------------------
data_yaml_path = None
for root, dirs, files in os.walk(extract_dir):
    for f in files:
        print("📂 Found file:", f)   # DEBUG PRINT
        if f == "data.yaml":
            data_yaml_path = os.path.join(root, f)
            break

if not data_yaml_path:
    raise FileNotFoundError("❌ data.yaml not found in extracted dataset!")

print(f"✅ Found data.yaml at: {data_yaml_path}")

# -------------------------------
# 4. TRAIN YOLOv8 MODEL
# -------------------------------
print("🚀 Starting training...")
model = YOLO("yolov8n.pt")  # You can also try yolov8s.pt or yolov8m.pt for better accuracy
model.train(
    data=data_yaml_path,
    epochs=50,   # Start small, then increase to 50+
    imgsz=640,
    batch=16
)

print("🎉 Training complete! Check 'runs/detect/train' for results.")
