## Introduction

This project aims to demonstrate how machine learning models can be used to generate Python code based on user input.
The project uses the GitHub API to collect Python repositories, preprocesses the collected data, trains a GPT-2 language
model on the preprocessed data, and generates Python code using the trained model.

The project is intended to showcase the potential of machine learning models in generating code, and to provide a
starting point for developers interested in exploring this area. While the generated code may not always be perfect, it
can serve as a source of inspiration or a starting point for further refinement.

The project is divided into several components, including data collection, data cleaning, data preprocessing,
tokenization, model training, and code generation.

## Data Collection

The first step in this project is to collect Python repositories from GitHub. This is done using the GitHub API, which
allows us to search for repositories based on various criteria, such as language, creation date, and keyword.

The data collection script `data_collector.py` takes a start date and an end date as inputs and collects all
repositories that were created between those dates and are written in Python. It then clones these repositories into a
local directory for further processing.

## Data Cleaning

The next step is to clean the collected data. The data cleaning script `data_cleaner.py` walks through all the cloned
repositories and deletes any file that is not a Python file. This is intended to help clean the dataset before
preprocessing.

## Data Preprocessing

After cleaning the data, the next step is to preprocess it. The data preprocessing script `data_preprocess.py` walks
through all the cleaned Python files and processes them one by one. It does this by removing comments and splitting long
files into smaller ones. The processed data is then outputted to a file called `data.txt`.

## Tokenization

Tokenization is the process of breaking up text into smaller units, or tokens, for further processing. In this project,
we use a Byte Level Byte Pair Encoding (BPE) tokenizer to tokenize our preprocessed data. The tokenizer
script `tokenizer.py` trains the tokenizer on the preprocessed data in`data.txt`. It also encodes a sample input text
using the trained tokenizer.

Byte Level Byte Pair Encoding (BPE) is a popular technique for subword tokenization. It works by iteratively merging the
most frequent pairs of bytes in a corpus to create a vocabulary of subword units. This allows the model to handle rare
words or out-of-vocabulary words more effectively.

## Model Training

The next step is to train a language model on the preprocessed and tokenized data. In this project, we use the GPT-2
language model, which is a state-of-the-art language model developed by OpenAI.

The model training script `train.py` loads the preprocessed data, loads the trained tokenizer, and trains the GPT-2
model. The trained model is then saved in a directory called `GPyT`.

Training a language model can be a resource-intensive process, requiring large amounts of computational power and time.
However, once the model is trained, it can be used to generate new text based on user input.

## Code Generation

The final step in this project is to use the trained language model to generate Python code based on user input. The
code generator script `code_generator.py` loads the trained GPT-2 model and prompts the user for input. It then
generates Python code based on the user input and outputs it to the console.

Code generation can be a challenging task, as the model must generate syntactically correct code that performs the
desired task. However, the GPT-2 model has shown promise in generating high-quality text, making it a good candidate for
code generation tasks.

## Usage

To use this project, you can follow the steps outlined in the previous answer:

1. Clone the repository and navigate to the project root directory.
2. Create a GitHub access token and save it to a file called `token.txt` in the project root directory.
3. Run the data collector script to collect Python repositories from GitHub: `python data_collector/data_collector.py`
4. Run the data cleaner script to delete non-Python files: `python preprocess/data_cleaner.py`
5. Run the data preprocessing script to preprocess the data: `python preprocess/data_preprocess.py`
6. Train the tokenizer: `python preprocess/tokenizer.py -t`
7. Encode input text using the trained tokenizer: `python preprocess/tokenizer.py -e`
8. Train the GPT-2 model: `python model/train.py`
9. Generate code using the trained model: `python model/code_generator.py`

Note that steps 1-5 only need to be run once to collect, clean, and preprocess the data. Steps 6-9 can be run multiple
times to train the model and generate code with different inputs.