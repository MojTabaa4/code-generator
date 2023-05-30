import os

from curtsies.fmtfuncs import green
from tokenizers import ByteLevelBPETokenizer
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    PreTrainedTokenizer,
    PreTrainedModel
)

# Disable Weights & Biases logging to avoid unnecessary output
os.environ["WANDB_DISABLED"] = "true"

# Set constants
TRAIN_BASE = False
TOKENIZER_DIR = "../tokenizer"
DATA_FILE = "../data.txt"

# Train tokenizer if necessary
if TRAIN_BASE:
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(
        files=[DATA_FILE],
        vocab_size=52000,
        min_frequency=2,
        special_tokens=[
            "<s>",
            "<pad>",
            "</s>",
            "<unk>",
            "<mask>",
        ]
    )

    tokenizer.save_model(TOKENIZER_DIR)

# Load tokenizer and add special tokens
tokenizer = GPT2Tokenizer.from_pretrained(TOKENIZER_DIR)
tokenizer.add_special_tokens({
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
})


def generate_code(model: PreTrainedModel, tokenizer: PreTrainedTokenizer, prompt: str) -> str:
    """
    Generate text using a pretrained GPT-2 model and tokenizer given a prompt.

    Args:
        model (PreTrainedModel): A pretrained GPT-2 model.
        tokenizer (PreTrainedTokenizer): A pretrained GPT-2 tokenizer.
        prompt (str): The prompt to generate text from.

    Returns:
        str: The generated text.
    """
    # Encode the prompt using the tokenizer
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to("cuda")

    # Generate text using the model
    beam_output = model.generate(
        input_ids,
        max_length=512,
        num_beams=10,
        temperature=0.7,
        no_repeat_ngram_size=5,
        num_return_sequences=1
    )

    # Decode the generated text using the tokenizer
    for beam in beam_output:
        out = tokenizer.decode(beam, skip_special_tokens=True)
        out = out.replace("<N>", "\n")

    # Return the generated text
    return out

# Load the trained GPT-2 model from the "GPyT" directory and set it to use the GPU for faster processing
model = GPT2LMHeadModel.from_pretrained("GPyT").to("cuda")

# Continuously prompt user for input and generate text using the GPT-2 model
while True:
    # Prompt user for input
    prompt = input("Insert your prompt: ")

    # Generate text using the GPT-2 model and print it
    output = generate_code(model, tokenizer, prompt)
    print(green(str(output)))
