from argparse import ArgumentParser
from tokenizers import ByteLevelBPETokenizer
from transformers import GPT2LMHeadModel, GPT2Tokenizer

TRAIN_BASE = False
TOKENIZER_DIR = "../tokenizer"
DATA_FILE_PATHS = ["../data.txt"]
VOCAB_SIZE = 52000
MIN_FREQ = 2
SPECIAL_TOKENS = {
    "eos_token": "</s>",
    "bos_token": "<s>",
    "unk_token": "<unk>",
    "pad_token": "<pad>",
    "mask_token": "<mask>"
}
INPUT_TEXT = "print('hello world!')"


def train_tokenizer():
    tokenizer = ByteLevelBPETokenizer()

    tokenizer.train(
        files=DATA_FILE_PATHS,
        vocab_size=VOCAB_SIZE,
        min_frequency=MIN_FREQ,
        special_tokens=list(SPECIAL_TOKENS.values())
    )

    tokenizer.save_model(TOKENIZER_DIR)


def encode_input_text():
    tokenizer = GPT2Tokenizer.from_pretrained(TOKENIZER_DIR)
    tokenizer.add_special_tokens(SPECIAL_TOKENS)

    encoded_input = tokenizer.encode(INPUT_TEXT)
    print(encoded_input)


if __name__ == "__main__":
    parser = ArgumentParser(description="Train tokenizer and encode input text with GPT-2")
    parser.add_argument("-t", "--train", action="store_true", help="Train the ByteLevelBPETokenizer")
    parser.add_argument("-e", "--encode", action="store_true", help="Encode the input text")
    args = parser.parse_args()

    if args.train:
        train_tokenizer()

    if args.encode:
        encode_input_text()