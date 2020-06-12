import json
import ipdb
from django.core.management import BaseCommand


tag_lst = ['p', 'em', 'iframe', 'span', 'blockquote', 'a', 'div', 'i', 'b', 'u', 'strong', 'color',
           'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'body', 'head', 'html', 'title', 'script', 'table']


def get_token(file):
    """
    :return:
    """
    token = list()
    for line in file:
        tk = ''
        for l in line:
            if l in '<':
                if tk:
                    token.append(tk)
                tk = l
            elif l in '>':
                tk += l
                token.append(tk)
                tk = ''
            else:
                tk += l
    return token


def get_tag(token):
    """
    Получить тег по токену
    Возвращает символ(ы) - тег
    """
    tag = None
    if '<' in token:
        tag = token.split('<')[1].split('>')[0].split(' ')[0].strip()
    return tag


def get_attribute(content):
    if ' ' not in content:
        return None
    tag = get_tag(content)
    content_lst = content[1:-1].split(' ')
    content_lst.remove(tag)
    if not content_lst:
        return None
    content_clear = ' '.join(content_lst)
    cont_kv = content_clear.split('"')
    key = None
    return_dct = dict()
    for cc in cont_kv:
        if key:
            return_dct.update({key: cc})
        if cc and '=' == cc[-1]:
            key = cc.strip('=').strip()
        else:
            key = None

    return return_dct


def get_content(tail):
    ret_lst = list()
    while tail:
        content = tail.pop(0)
        tag = get_tag(content)

        if tag in tag_lst:
            tag_dct = dict()
            tag_dct.setdefault(tag, {}).update({'content': get_content(tail)})
            attribute = get_attribute(content)
            if attribute:
                tag_dct.setdefault(tag, {}).update({'attribute': attribute})
            ret_lst.append(tag_dct)
        elif tag and '/' in tag:
            return ret_lst

        else:
            if '<' == content[0]:
                tag_dct = dict()
                attribute = get_attribute(content)
                tag_dct.setdefault(tag, {}).update({'attribute': attribute})
                ret_lst.append(tag_dct)
            else:
                ret_lst.append(content)

    return ret_lst


class Command(BaseCommand):

    def handle(self, *args, **options):

        with open('/home/pascal65536/Загрузки/html.html', 'r') as file:
            token = get_token(file)

        ret_json = get_content(token)

        with open('/home/pascal65536/Загрузки/html.json', 'w') as f:
            json.dump(ret_json, f)
