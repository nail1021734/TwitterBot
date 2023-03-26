import argparse
import json
import math
import snscrape.modules.twitter as sntwitter
from pathlib import Path
from tqdm import tqdm

from typing import List, Dict


def load_jsonl(filename: str) -> List:
    filepath = Path(filename)
    data = []
    with filepath.open('r') as input_file:
        for d in input_file.readlines():
            data.append(json.loads(d))

    return data


def save_jsonl(filename: str, data: List, overwrite: bool=False) -> None:
    filepath = Path(filename)
    if not filepath.exists() or overwrite:
        with filepath.open('w') as output_file:
            for d in data:
                output_file.write(json.dumps(d) + '\n')
    else:
        with filepath.open('a') as output_file:
            for d in data:
                output_file.write(json.dumps(d) + '\n')


def get_user_posts(user_name: str, max_post_num: int = math.inf) -> List:
    posts = []
    count = 0
    tqdm_iter = tqdm(sntwitter.TwitterSearchScraper(f'from:{user_name}').get_items(), desc=f'hit:{count}')
    for post in tqdm_iter:
        if count < max_post_num:
            if post.inReplyToUser is not None:
                continue
            count += 1
            tqdm_iter.set_description(desc=f'hit:{count}')
            posts.append({
                'url': post.url,
                'user': post.user.username,
                'date': post.date.timestamp(),
                'likeCount': post.likeCount,
                'renderedContent': post.renderedContent,
                'rawContent': post.rawContent,
                'conversationId': post.conversationId,
            })
        else:
            break

    return posts


def get_replies_by_conversation_id(conversation_id: int, max_reply_num: int = math.inf, min_like: int = 0) -> List:
    replies = []
    count = 0
    for reply in sntwitter.TwitterSearchScraper(f'conversation_id:{conversation_id}(filter:safe)').get_items():
        if count < max_reply_num:
            if reply.likeCount < min_like:
                continue
            count += 1
            replies.append({
                'user': reply.user.username,
                'date': reply.date.timestamp(),
                'likeCount': reply.likeCount,
                'renderedContent': reply.renderedContent,
                'rawContent': reply.rawContent,
            })
        else:
            break

    return replies


if __name__ == "__main__":
    # User list
    users = [
        # 'margaretthebox',
        # 'linglanthebox',
        'LocoLost65',
        'MizukiVtuberTW',
        'SekiVtuberTW',
        'KSPKSP01',
        'shibasakithebox',
        'HibikiVtuberTW',
        'paitan6111',
    ]

    for name in users:
        # Enter user name
        user_posts = get_user_posts(user_name=name)

        # Get reply of each post.
        for index, post in tqdm(list(enumerate(user_posts))):
            replies = get_replies_by_conversation_id(conversation_id=post['conversationId'], max_reply_num=10000, min_like=2)
            user_posts[index]['replies'] = replies

        save_jsonl(filename=f'{name}.jsonl', data=user_posts, overwrite=True)
