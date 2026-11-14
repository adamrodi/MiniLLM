# convert text to a list of tokens
def encode(raw_text, char_to_id):
    token_ids = []
    for character in raw_text:
        token_ids.append(char_to_id[character])
    return token_ids

# convert a list of tokens to text
def decode(encoded_text, characters):
    decoded_text = ""
    for token_id in encoded_text:
        decoded_text += characters[token_id]
    return decoded_text
