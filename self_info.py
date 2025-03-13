
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def read_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [line.strip() for line in data]


def tokenize_input(input_data, tokenizer):
    input_ids = []
    attention_masks = []
    for text in input_data:
        encoded_dict = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            padding=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])
    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    return input_ids, attention_masks


def calculate_entropy(text):

    # specify the model name
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-7B")
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-7B")

    t_input = tokenizer(text, padding=True, return_tensors="pt")
    input_ids_expanded = t_input['input_ids'].unsqueeze(-1)

    with torch.no_grad():
        outputs = model(**t_input)

    logits = outputs.logits
    predicted_probs = torch.softmax(logits, dim=-1)

    self_info = -torch.log2(predicted_probs)
    token_info = self_info.gather(-1, input_ids_expanded).squeeze(-1).squeeze(0)

    return sum(token_info)


def main(path='data.txt'):
    texts = read_txt(path)
    entropies = list(map(calculate_entropy, texts))

    sorted_zip = sorted(zip(texts, entropies), key=lambda x: x[1], reverse=True)
    sorted_texts, sorted_entropies = zip(*sorted_zip)

    for i in range(len(sorted_texts)):
        print(sorted_texts[i], sorted_entropies[i].item())

if __name__ == '__main__':
    #specify the name of the candidate homo
    main("laozi")