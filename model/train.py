import os
from datasets import load_dataset
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer, DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

# Disable W&B logging to prevent errors
os.environ["WANDB_DISABLED"] = "true"


# Define the function to encode text using the tokenizer
def encode(lines):
    return tokenizer(lines['text'], add_special_tokens=True, truncation=True, max_length=512)


# Set the paths for the input data and the tokenizer
DATA_PATHS = ["../data.txt"]
TOKENIZER_DIR = "../tokenizer"

# Check if training the tokenizer is required
TRAIN_TOKENIZER = False

# If training the tokenizer is required, train and save it
if TRAIN_TOKENIZER:
    tokenizer = ByteLevelBPETokenizer()
    tokenizer.train(files=DATA_PATHS, vocab_size=52000, min_frequency=2, special_tokens=[
        "<s>",
        "<pad>",
        "</s>",
        "<unk>",
        "<mask>",
    ])
    tokenizer.save_model(TOKENIZER_DIR)

# Define the input text to be used for testing the tokenizer and the model
input_text = "print('hello world!')"

# Load the tokenizer and add any required special tokens
tokenizer = GPT2Tokenizer.from_pretrained(TOKENIZER_DIR)
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})

# Encode the input text using the tokenizer and print the result
encoded_input = tokenizer.encode(input_text)
print(encoded_input)
print(tokenizer.decode(encoded_input))

# Define the model configuration
config = GPT2Config(
    vocab_size=tokenizer.vocab_size,
    bos_token=tokenizer.bos_token_id,
    eos_token=tokenizer.eos_token_id
)

# Create the GPT-2 language model
model = GPT2LMHeadModel(config)

# Load the input data and apply the encoding function to it
dataset = load_dataset("text", data_files=DATA_PATHS)
dataset.set_transform(encode)
dataset = dataset['train']

# Define the data collator for the language modeling task
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

# Define the training arguments and set the output directory and other options
output_dir = "../GPyT"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

training_args = TrainingArguments(
    output_dir=output_dir,
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=4,
    save_steps=100,
    save_total_limit=2,
    prediction_loss_only=True,
    remove_unused_columns=False
)

# Create the Trainer object and start training the model
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset
)
trainer.train()

# Save the trained model
trainer.save_model("GPyT")
