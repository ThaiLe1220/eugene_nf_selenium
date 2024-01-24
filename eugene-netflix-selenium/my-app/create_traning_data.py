import json
import os

# Correct directory where the files are located
DATA_DIRECTORY = "./data/en-vi/"

# Listing the first 20 json files in the directory
first_10_files = sorted(
    [file for file in os.listdir(DATA_DIRECTORY) if file.endswith(".json")]
)[:35]

# Initialize a list to hold all the translation pairs
all_data = []

# Iterate through the first 10 files and read their contents
for file_name in first_10_files:
    with open(os.path.join(DATA_DIRECTORY, file_name), "r", encoding="utf-8") as file:
        data = json.load(file)
        all_data.extend(data)

# Split the data into training and validation sets manually
DATA_LENGTH = len(all_data)
SPLIT_INDEX = int(DATA_LENGTH * 0.85)
train_data = all_data[:SPLIT_INDEX]
validation_data = all_data[SPLIT_INDEX:]


def save_to_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# Save the training and validation sets to json files
TRAIN_FILE_PATH = "./train.json"
VALIDATION_FILE_PATH = "./validation.json"

save_to_json(TRAIN_FILE_PATH, train_data)
save_to_json(VALIDATION_FILE_PATH, validation_data)

print(f"Number of translation pairs in train.json: {DATA_LENGTH *0.85}")
print(f"Number of translation pairs in validation.json: {DATA_LENGTH*0.15}")
