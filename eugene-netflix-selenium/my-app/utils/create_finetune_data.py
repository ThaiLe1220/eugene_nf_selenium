import json
import os
import random

# Correct directory where the files are located
LANG_CODE = "vi"
DATA_DIRECTORY = f"../data/en-{LANG_CODE}/"

all_files = [file for file in os.listdir(DATA_DIRECTORY) if file.endswith(".json")]

NUM_FILE = 200
files = random.sample(all_files, min(NUM_FILE, len(all_files)))

# Initialize lists for different length categories
data_less_than_10 = []
data_less_than_20 = []
data_less_than_30 = []
data_less_than_40 = []
data_less_than_50 = []
data_50_or_more = []

# Initialize a list to hold all the translation pairs
all_data = []

for file_name in files:
    with open(os.path.join(DATA_DIRECTORY, file_name), "r", encoding="utf-8") as file:
        translations = json.load(file)

        for item in translations:
            len_en = len(item["translation"]["en"])
            len_lang = len(item["translation"][LANG_CODE])
            max_len = max(len_en, len_lang)
            length_diff_ratio = abs(len_en - len_lang) / max_len

            # Check length difference condition
            if length_diff_ratio <= 0.8:
                # Classify based on length criteria
                if len_en < 10 and len_lang < 10:
                    data_less_than_10.append(item)
                elif len_en < 20 and len_lang < 20:
                    data_less_than_20.append(item)
                elif len_en < 30 and len_lang < 30:
                    data_less_than_30.append(item)
                elif len_en < 40 and len_lang < 40:
                    data_less_than_40.append(item)
                elif len_en < 50 and len_lang < 50:
                    data_less_than_50.append(item)
                else:
                    data_50_or_more.append(item)

# Calculate proportions and extend all_data
TOTAL_ITEMS = (
    len(data_less_than_10)
    + len(data_less_than_20)
    + len(data_less_than_30)
    + len(data_less_than_40)
    + len(data_less_than_50)
    + len(data_50_or_more)
)

all_data.extend(
    random.sample(
        data_less_than_10, min(len(data_less_than_10), int(TOTAL_ITEMS * 0.08))
    )
)
all_data.extend(
    random.sample(
        data_less_than_20, min(len(data_less_than_20), int(TOTAL_ITEMS * 0.1))
    )
)
all_data.extend(
    random.sample(
        data_less_than_30, min(len(data_less_than_30), int(TOTAL_ITEMS * 0.12))
    )
)
all_data.extend(
    random.sample(
        data_less_than_40, min(len(data_less_than_40), int(TOTAL_ITEMS * 0.2))
    )
)
all_data.extend(
    random.sample(
        data_less_than_40, min(len(data_less_than_40), int(TOTAL_ITEMS * 0.2))
    )
)
all_data.extend(
    random.sample(data_50_or_more, min(len(data_50_or_more), int(TOTAL_ITEMS * 0.5)))
)


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

print(f"Number of translation pairs in train.json: {len(train_data)}")
print(f"Number of translation pairs in validation.json: {len(validation_data)}")
