1st run:

train split: 34088 examples, validation split: 6016 examples 

args = Seq2SeqTrainingArguments(
    f"opus-mt-en-es-NLP-finetuned-en-to-es",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=5,
    predict_with_generate=True,
)


2nd run:

train split: 106800 examples, validation split: 18848 examples 

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
