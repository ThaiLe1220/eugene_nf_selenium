import json
import os
import random

# Correct directory where the files are located
LANG_CODE = "es"
DATA_DIRECTORY = f"./data/en-{LANG_CODE}/"

all_files = [file for file in os.listdir(DATA_DIRECTORY) if file.endswith(".json")]

NUM_FILE = 300
files = random.sample(all_files, min(NUM_FILE, len(all_files)))


# Initialize a list to hold all the translation pairs
all_data = []

for file_name in files:
    with open(os.path.join(DATA_DIRECTORY, file_name), "r", encoding="utf-8") as file:
        translations = json.load(file)
        filtered_data = [
            item
            for item in translations
            if len(item["translation"]["en"]) > 30
            and len(item["translation"][LANG_CODE]) > 30
            and abs(
                len(item["translation"]["en"]) - len(item["translation"][LANG_CODE])
            )
            / max(
                len(item["translation"]["en"]),
                len(item["translation"][LANG_CODE]),
            )
            <= 0.8
        ]
        all_data.extend(filtered_data)

# Split the data into training and validation sets manually
DATA_LENGTH = len(all_data)
SPLIT_INDEX = int(DATA_LENGTH * 0.85)
train_data = all_data[:SPLIT_INDEX]
validation_data = all_data[SPLIT_INDEX:]


def save_to_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Save the training and validation sets to json files
TRAIN_FILE_PATH = "./train.json"
VALIDATION_FILE_PATH = "./validation.json"

save_to_json(TRAIN_FILE_PATH, train_data)
save_to_json(VALIDATION_FILE_PATH, validation_data)

print(f"Number of translation pairs in train.json: {DATA_LENGTH *0.85}")
print(f"Number of translation pairs in validation.json: {DATA_LENGTH*0.15}")
