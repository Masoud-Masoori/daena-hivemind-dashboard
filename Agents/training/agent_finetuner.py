### File: agents/training/agent_finetuner.py

import os
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer

def finetune_agent(agent_name, dataset_path):
    print(f"[Training] Starting fine-tune for {agent_name}")
    tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")
    model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-6.7b-instruct")

    with open(dataset_path, "r") as f:
        lines = f.readlines()
        texts = [{"text": l.strip()} for l in lines if l.strip()]
        dataset = Dataset.from_list(texts)

    def tokenize(example): return tokenizer(example["text"], truncation=True, padding="max_length", max_length=512)
    tokenized_dataset = dataset.map(tokenize)

    output_dir = f"trained/{agent_name}"
    os.makedirs(output_dir, exist_ok=True)
    trainer = Trainer(
        model=model,
        args=TrainingArguments(output_dir=output_dir, per_device_train_batch_size=2, num_train_epochs=1),
        train_dataset=tokenized_dataset
    )
    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
