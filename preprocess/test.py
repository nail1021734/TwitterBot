import pytest
from preprocess import (
    subs_by_table,
    build_tag_dict,
    build_user_dict,
    subs_urls,
)


POST = '@askdjh @Loco I\'m hungry... #alkdfj #ajskldj'

replies = '@askdjh @aksw me2 #alkdfj'

def test_subs_by_table():
    article = 'I am a smart robot, isn\'t it?'

    assert subs_by_table(
        text=article,
        table={'sm': 'test', 'art': 'test'},
        add_number=True,
    ) == 'I am a [test0][test1] robot, isn\'t it?'

    assert subs_by_table(
        text=article,
        table={'sm': 'dog', 'art': 'dog'},
        add_number=True,
    ) == 'I am a [dog0][dog1] robot, isn\'t it?'

    assert subs_by_table(
        text=article,
        table={'sm': 'art', 'art': 'gg'},
        add_number=True,
    ) == 'I am a [art0][gg0] robot, isn\'t it?'

    assert subs_by_table(
        text=article,
        table={'sm': 'art', 'art': 'gg', 'bvvc': 'art'},
        add_number=False,
    ) == 'I am a [art][gg] robot, isn\'t it?'

    assert subs_by_table(
        text=article,
        table={'sm': 'art', 'art': 'gg', 'bot': 'art'},
        add_number=True,
    ) == 'I am a [art0][gg0] ro[art1], isn\'t it?'


def test_build_user_dict():
    example = '[BOS]@sad @slas @saddd\n ldk I am dog man. #dog_man #bigdog [EOS]'

    assert build_user_dict(text=example) == {
        '@sad': 'user',
        '@slas': 'user',
        '@saddd': 'user',
    }


def test_build_tag_dict():
    example = '[BOS] @sad @slas ldk I am dog man. #asd #dog_man\n#bigdog[EOS]'

    assert build_tag_dict(text=example) == {
        '#asd': 'tag',
        '#dog_man': 'tag',
        '#bigdog': 'tag',
    }

def test_subs_urls():
    example = '[BOS] https://sadkjl.com.tw ;lfjlsajdklak ewljf [EOS]'

    assert subs_urls(text=example) == '[BOS] [URL] ;lfjlsajdklak ewljf [EOS]'
