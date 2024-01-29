import transformers
from transformers import AutoTokenizer
from datasets import load_dataset, load_metric, DatasetDict
from IPython.display import display, HTML
from transformers import AutoTokenizer
from transformers import (
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    MarianMTModel,
    MarianTokenizer,
)


def ori_translate(src_lan, tar_lan):
    model_name = "Helsinki-NLP/opus-mt-{src_lan}-{tar_lan}"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    opus_mt_translation_txt = []

    for text in original_txt:
        translated = model.generate(
            **tokenizer([text], return_tensors="pt", padding=True)
        )
        translation = tokenizer.decode(translated[0], skip_special_tokens=True)
        opus_mt_translation_txt.append(translation)

    with open(
        f"./target/opus_mt_{src_lan}_{tar_lan}_translation.txt",
        "w",
        encoding="utf-8",
    ) as f:
        for l in opus_mt_translation_txt:
            f.write(l + "\n")


def finetune_translate(version, src_lan, tar_lan):
    finetuned_model_name = f"./target/{version}/opus-mt-{src_lan}-{tar_lan}-finetuned-{src_lan}-to-{tar_lan}"
    tokenizer = MarianTokenizer.from_pretrained(finetuned_model_name)
    finetuned_model = MarianMTModel.from_pretrained(finetuned_model_name)

    finetuned_opus_mt_translation_txt = []

    for text in original_txt:
        translated = finetuned_model.generate(
            **tokenizer([text], return_tensors="pt", padding=True)
        )
        translation = tokenizer.decode(translated[0], skip_special_tokens=True)
        finetuned_opus_mt_translation_txt.append(translation)

    with open(
        f"./target/{version}/finetuned_opus_mt_{src_lan}_{tar_lan}_translation_{version}.txt",
        "w",
        encoding="utf-8",
    ) as f:
        for l in finetuned_opus_mt_translation_txt:
            f.write(l + "\n")


FILE_PATH = "original_english_text.txt"
VERSION = "v2"
SOURCE_LANG = "en"
TARGET_LANG = "vi"

original_txt = []

with open(FILE_PATH, "r", encoding="utf-8") as file:
    for line in file:
        original_txt.append(line.strip())


# ori_translate(SOURCE_LANG, TARGET_LANG)
finetune_translate(VERSION, SOURCE_LANG, TARGET_LANG)
