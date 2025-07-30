from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset
import torch
from transformers import BitsAndBytesConfig


model_name = "microsoft/phi-2"
dataset_path = "./finetune/your_dataset.json"

# Load model + tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_enable_fp32_cpu_offload=True
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Apply LoRA config
lora_config = LoraConfig(task_type=TaskType.CAUSAL_LM, r=8, lora_alpha=16, lora_dropout=0.1, bias="none")
model = get_peft_model(model, lora_config)

# Load dataset
ds = load_dataset("json", data_files=dataset_path)["train"]

def format_example(example):
    return tokenizer(
        f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}",
        truncation=True, padding="max_length", max_length=512
    )

tokenized_ds = ds.map(format_example)

# Training config
training_args = TrainingArguments(
    per_device_train_batch_size=4,
    num_train_epochs=3,
    logging_steps=10,
    output_dir="./finetune/output",
    save_strategy="no"
)

trainer = Trainer(
    model=model,
    train_dataset=tokenized_ds,
    args=training_args,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()