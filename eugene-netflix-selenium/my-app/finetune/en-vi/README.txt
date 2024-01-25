1st run:

train split: 10000 examples, validation split: 1300 examples 

args = Seq2SeqTrainingArguments(
    f"opus-mt-en-es-NLP-finetuned-en-to-es",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=24,
    per_device_eval_batch_size=24,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=5,
    predict_with_generate=True,
)


2nd run:

train split: 119159 examples, validation split: 29790 examples 

args = Seq2SeqTrainingArguments(
    f"opus-mt-en-es-NLP-finetuned-en-to-es",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=5,
    predict_with_generate=True,
)
