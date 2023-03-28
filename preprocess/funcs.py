import re

from typing import List, Dict
from unicodedata import normalize


USER_PATTERN = re.compile(r'(@.+?)(?:\s|\[EOS\]|\[SEP\]|\n|$)')

TAG_PATTERN = re.compile(r'(#.+?)(?:\s|\[EOS\]|\[SEP\]|\n|$)')


def NFKC_and_whitespace_filter(text: str):
    return re.sub(r'\s+', ' ', normalize('NFKC', text))


def remove_emoji(text: str):
    emoji_pattern = re.compile("["
       u"\U0001F600-\U0001F64F"  # emoticons
       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
       u"\U0001F680-\U0001F6FF"  # transport & map symbols
       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
       "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def subs_by_table(
    text: str,
    table: Dict[str, str],
    add_number: bool,
):
    r"""
    text: source text
    table: key=target word, value=repl prefix
    add_number: If add number after repl.
    """
    if add_number:
        # key is tag and value is a list of target word which use the same tag.
        word_number_dict = {v: [] for v in set(table.values())}

    replaced_text = ''
    last_index = 0
    # Add backslash before parenthesises.
    # new_table = []
    # for k in table.keys():
    #     temp_key = k
    #     for match in list(re.finditer(r'[+*?^$|\\\{\}\[\]()]', k))[::]:
    #         temp_key = temp_key[:match.start()-1] + '\\' + temp_key[match.start():]
    #     new_table.append(temp_key)

    # Replace tags.
    for match in re.finditer('|'.join([re.escape(key) for key in table.keys()]), text):
        word = match.group(0)
        tag = table[word]

        if add_number:
            if word not in word_number_dict[tag]:
                word_number_dict[tag].append(word)
            tag = tag + str(word_number_dict[tag].index(word))

        replaced_text += text[last_index: match.start()] + f'[{tag}]'
        last_index = match.end()
    replaced_text += text[last_index:]

    return replaced_text


def build_user_dict(text: str):
    return {user: 'user' for user in USER_PATTERN.findall(text)}


def build_tag_dict(text: str):
    return {tag: 'tag' for tag in TAG_PATTERN.findall(text)}


def subs_urls(text: str):
    return re.sub(r'https?://[A-Za-z0-9\-._~:/?#@!$&\'()*+,;%=]+', '[URL]', text)

def concat_post_replies(post: Dict, min_reply_like_count: int, min_length: int = 0):
    concated_data = []
    for reply in post['replies']:
        if reply['likeCount'] > min_reply_like_count and len(reply['rawContent']) > min_length:
            concated_data.append('[BOS]' + post['rawContent'] + '[SEP]' + reply['rawContent'] + '[EOS]')

    return concated_data


def preprocess(text: str):
    # Remove.
    text = NFKC_and_whitespace_filter(text=text)
    # text = remove_emoji(text=text)

    # Build entity :tag table.
    table = build_user_dict(text=text)
    table.update(build_tag_dict(text=text))

    # Replace user and tag by special tokens.
    if table != {}:
        text = subs_by_table(text=text, table=table, add_number=True)

    # Replace url by special tokens.
    text = subs_urls(text=text)

    return text

