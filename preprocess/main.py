from pathlib import Path
from data_crawler.utils import load_multiple_jsonl, save_jsonl
from typing import List, Dict
from preprocess.funcs import (
    concat_post_replies,
    preprocess,
)


if __name__ == '__main__':
    # Merge each file.
    filenames = [
        # 'data_crawler/HibikiVtuberTW.jsonl',
        # 'data_crawler/KSPKSP01.jsonl',
        # 'data_crawler/lily.jsonl',
        'data_crawler/LocoLost65.jsonl',
    ]
    data = load_multiple_jsonl(filenames=filenames)

    # Concat post text and reply.
    concated_data = []
    [concated_data.extend(concat_post_replies(post=post, min_reply_like_count=2, min_length=5)) for post in data]

    # Preprocessing
    data = [preprocess(text=text) for text in concated_data]

    # Save as jsonl file.
    save_jsonl(data=data, filename='merged_data.jsonl', overwrite=True)
