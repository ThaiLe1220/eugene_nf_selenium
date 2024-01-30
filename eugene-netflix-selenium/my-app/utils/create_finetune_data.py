import json
import os
import random

# Define language translation and set the directory path for data files
SOURCE_LANG = "en"
TARGET_LANG = "it"
DATA_DIRECTORY = f"../data/{SOURCE_LANG}-{TARGET_LANG}/"

# List all JSON files in the specified data directory
all_files = [file for file in os.listdir(DATA_DIRECTORY) if file.endswith(".json")]

# Randomly select files to process, limited to NUM_FILE or the total number of files, whichever is smaller
NUM_FILE = 800
files = random.sample(all_files, min(NUM_FILE, len(all_files)))

# Initialize lists to categorize translation pairs based on their length
data_less_than_10 = []
data_less_than_20 = []
data_less_than_40 = []
data_less_than_60 = []
data_less_than_80 = []
data_less_than_100 = []
data_100_or_more = []

# Initialize a list to hold all eligible translation pairs
all_data = []


def contains_control_characters(item):
    """
    Checks if the translation texts in both the source and target languages
    contain any specified control characters.

    Args:
        item (dict): A dictionary representing a translation pair

    Returns:
        bool: True if any of the specified control characters are found
        in either the source or target text, False otherwise.
    """
    # Define a set of characters you want to check for
    check_chars = set("♪-‏")

    # Check both SOURCE_LANG and TARGET_LANG text for any of the check_chars
    return any(
        char in item["translation"][SOURCE_LANG] + item["translation"][TARGET_LANG]
        for char in check_chars
    )


def is_valid_translation(item):
    """
    Checks if a translation pair is valid by looking for specific anomalies.
    """
    src_text = item["translation"]["en"]
    tar_text = item["translation"]["it"]

    # Check if the first 20 characters of both translations are the same
    if src_text[:15].replace(" ", "").strip() == tar_text[:15].replace(" ", "").strip():
        return False

    return True


def swap_translation_languages(item):
    """
    Swaps the languages in the translation dictionary of the item.

    Args:
        item (dict): A dictionary containing the translation pair.

    Returns:
        dict: A new dictionary with swapped languages.
    """
    return {
        "translation": {
            TARGET_LANG: item["translation"][TARGET_LANG],
            SOURCE_LANG: item["translation"][SOURCE_LANG],
        }
    }


# Process each file in the selected list
for file_name in files:
    with open(os.path.join(DATA_DIRECTORY, file_name), "r", encoding="utf-8") as file:
        translations = json.load(file)

        # Iterate over each translation pair in the file
        for item in translations:
            # Skip translation pairs with specific characters
            if contains_control_characters(item) or not is_valid_translation(item):
                continue

            item = swap_translation_languages(item)

            len_source = len(item["translation"][SOURCE_LANG])
            len_target = len(item["translation"][TARGET_LANG])
            max_len = max(len_source, len_target)

            # Skip empty translations
            if max_len == 0:
                continue

            # Calculate the length difference ratio between source and target language
            length_diff_ratio = abs(len_source - len_target) / max_len

            # Filter pairs where the length difference ratio is within an acceptable range (80%)
            if length_diff_ratio <= 0.6:
                # Classify based on length criteria
                if len_source < 10 and len_target < 10:
                    data_less_than_10.append(item)
                elif len_source < 20 and len_target < 20:
                    data_less_than_20.append(item)
                elif len_source < 40 and len_target < 40:
                    data_less_than_40.append(item)
                elif len_source < 60 and len_target < 60:
                    data_less_than_60.append(item)
                elif len_source < 80 and len_target < 80:
                    data_less_than_80.append(item)
                elif len_source < 100 and len_target < 100:
                    data_less_than_100.append(item)
                else:
                    data_100_or_more.append(item)

# Calculate total number of translation pairs across all categories
TOTAL = (
    len(data_less_than_10)
    + len(data_less_than_20)
    + len(data_less_than_40)
    + len(data_less_than_60)
    + len(data_less_than_80)
    + len(data_less_than_100)
    + len(data_100_or_more)
)

# Select a proportion of translation pairs from each category to form a diverse dataset
all_data.extend(
    random.sample(data_less_than_20, min(len(data_less_than_20), int(TOTAL * 0.01)))
)
all_data.extend(
    random.sample(data_less_than_40, min(len(data_less_than_40), int(TOTAL * 0.01)))
)
all_data.extend(
    random.sample(data_less_than_100, min(len(data_less_than_100), int(TOTAL * 1)))
)
all_data.extend(
    random.sample(data_100_or_more, min(len(data_100_or_more), int(TOTAL * 1)))
)
all_data.extend(
    random.sample(data_less_than_80, min(len(data_less_than_80), int(TOTAL * 1)))
)
all_data.extend(
    random.sample(data_less_than_60, min(len(data_less_than_60), int(TOTAL * 0.02)))
)
all_data.extend(
    random.sample(data_less_than_40, min(len(data_less_than_40), int(TOTAL * 0.01)))
)

# Split the data into training (80%) and validation (20%) sets
DATA_LENGTH = len(all_data)
SPLIT_INDEX = int(DATA_LENGTH * 0.8)
train_data = all_data[:SPLIT_INDEX]
validation_data = all_data[SPLIT_INDEX:]


def save_to_json(file_path, data):
    """Saves provided data to a JSON file.

    Args:
        file_path (str): Path to the output JSON file.
        data (list): Data to be saved in JSON format.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Save the training and validation sets to their respective JSON files
TRAIN_FILE_PATH = "./train.json"
VALIDATION_FILE_PATH = "./validation.json"

save_to_json(TRAIN_FILE_PATH, train_data)
save_to_json(VALIDATION_FILE_PATH, validation_data)

# Print the number of translation pairs in each set
print(f"Number of translation pairs in train.json: {len(train_data)}")
print(f"Number of translation pairs in validation.json: {len(validation_data)}")
print(TOTAL)
