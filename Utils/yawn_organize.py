import os
import shutil
from sklearn.model_selection import train_test_split

# Define paths
YAWN_DATASET_PATH = r"C:\driver-drowsiness\yawn_dataset"  # Update this to your actual path
NEW_DATASET_PATH = r"C:\driver-drowsiness\yawning_dataset"  # Where the split dataset will be stored

# Categories
CATEGORIES = ["yawn", "no_yawn"]

# Create train, test, and validation folders
for split in ["train", "test", "validation"]:
    for category in CATEGORIES:
        os.makedirs(os.path.join(NEW_DATASET_PATH, split, category), exist_ok=True)

# Function to split and copy images
def split_and_move(category):
    source_folder = os.path.join(YAWN_DATASET_PATH, category)
    images = [f for f in os.listdir(source_folder) if f.endswith(('.jpg', '.png', '.jpeg'))]

    # Split into train (80%), test (10%), validation (10%)
    train, test = train_test_split(images, test_size=0.2, random_state=42)
    test, val = train_test_split(test, test_size=0.5, random_state=42)

    # Copy files to respective folders
    for img in train:
        shutil.copy(os.path.join(source_folder, img), os.path.join(NEW_DATASET_PATH, "train", category))
    for img in test:
        shutil.copy(os.path.join(source_folder, img), os.path.join(NEW_DATASET_PATH, "test", category))
    for img in val:
        shutil.copy(os.path.join(source_folder, img), os.path.join(NEW_DATASET_PATH, "validation", category))

# Process each category
for category in CATEGORIES:
    split_and_move(category)

print("✅ Yawning dataset split successfully!")
