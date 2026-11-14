from datasets import load_dataset
from tokenizer import encode, decode

stories = load_dataset(
    "roneneldan/TinyStories",
    split="train",
    streaming=True,
)

texts = []
for example in stories.take(1000):
    texts.append(example["text"])

vocabulary_text = "".join(texts)
characters = sorted(set(vocabulary_text))

char_to_id = {}
for i, character in enumerate(characters):
    char_to_id[character] = i


validation_stories = load_dataset(
    "roneneldan/TinyStories",
    split="validation",
    streaming=True,
)

validation_texts = []
for example in validation_stories.take(100):
    validation_texts.append(example["text"])

validation_text = "".join(validation_texts)
unseen = set(validation_text) - set(characters)


for story in texts:
    token_ids = encode(story, char_to_id)
    recovered = decode(token_ids, characters)
    assert recovered == story, "Story round trip failed"
print("Training round trips passed:", len(texts))

for story in validation_texts:
    token_ids = encode(story, char_to_id)
    recovered = decode(token_ids, characters)
    assert recovered == story, "Story round trip failed"
print("Validation round trips passed:", len(validation_texts))

context_length = 8
story_tokens = encode(texts[0], char_to_id)
chunk = story_tokens[:context_length + 1]

inputs = chunk[:-1]
targets = chunk[1:]
print("Inputs:", repr(decode(inputs, characters)))
print("Targets:", repr(decode(targets, characters)))
print("Lengths:", len(inputs), len(targets))