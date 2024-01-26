from transformers import LlamaTokenizerFast
import pathlib


def get_content(max_tokens=999999):
    file_path = pathlib.Path(__file__).parent.resolve() / "charlie_munger.txt"
    total_tokens = 0
    content = ""
    tokenizer = LlamaTokenizerFast.from_pretrained(
        "hf-internal-testing/llama-tokenizer"
    )

    get_token_length = lambda text: len(tokenizer.encode(text))

    with open(file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            token_len = get_token_length(line)
            if total_tokens + token_len > max_tokens:
                break
            content += line
            total_tokens += token_len

    print(f"Token length of prompt to summarize: {total_tokens}")
    return content

