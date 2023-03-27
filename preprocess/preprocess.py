import re

from typing import List, Dict


#TODO Update the pattern, make the pattern can match the USER that following [EOS], \s, \n or endoftext.
USER_PATTERN = re.compile(r'(@.+?)(?:\s|\[EOS\]|\n|$)')

TAG_PATTERN = re.compile(r'(#.+?)(?:\s|\[EOS\]|\n|$)')


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
    for match in re.finditer('|'.join(table.keys()), text):
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
    return re.sub(r'https?://[A-Za-z0-9\-._~:/?#\[\]@!$&\'()*+,;%=]+', '[URL]', text)
