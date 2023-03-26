from pathlib import Path
from data_crawler.utils import load_jsonl
from typing import List, Dict


def load_multiple_jsonl(filenames: List[str]):
    merged_data = []
    for filename in filenames:
        merged_data += load_jsonl(filename)

    return merged_data


def concat_post_replies(post: Dict, min_reply_like_count: int):
    concated_data = []
    for reply in post.replies:
        concated_data.append('[BOS]')


if __name__ == '__main__':
    # Merge each file.
    filenames = [
        'data_crawler/HibikiVtuberTW.jsonl',
        'data_crawler/KSPKSP01.jsonl',
        'data_crawler/lily.jsonl',
        'data_crawler/LocoLost65.jsonl',
    ]
    data = load_multiple_jsonl(filenames=filenames)

    # Concat post text and reply.
    print(data[0])
    # Preprocessing
    # Save as jsonl file.
