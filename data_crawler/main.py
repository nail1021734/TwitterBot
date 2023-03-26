from data_crawler.utils import (
    load_jsonl,
    save_jsonl,
    get_user_posts,
    get_replies_by_conversation_id,
)

if __name__ == '__main__':
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
