'''
문장 데이터중 Comment가 있는 데이터만 뽑아주는 스크립트
'''

import os
import json
from xml.etree.ElementTree import parse

def getCommentedSentInfo(xml_path):
    commented_item = []

    try:
        xml_tree = parse(xml_path)
        root = xml_tree.getroot()
    except:
        return []

    sent_node_list = root.findall('sent_item')
    for sent_node in sent_node_list:
        sent_id = sent_node.get('id')
        sent = sent_node.find('sent').text.strip()
        sbj = sent_node.find('sbj').text.strip()
        obj = sent_node.find('obj').text.strip()
        relation = sent_node.find('gold').text.strip()
        dependency = sent_node.find('gsdp').text.strip()
        dependency_lemma = sent_node.find('gsdp_lemma').text
        dependency_lemma = dependency_lemma.strip() if dependency_lemma != None else ''

        comment = sent_node.find('comment').text
        if (comment != None and len(comment) > 0):
            commented_item.append({
                'sent_id' : sent_id,
                'sent' : sent,
                'sbj' : sbj,
                'obj' : obj,
                'relation': relation,
                'gsdp': dependency,
                'gsdp_lemma': dependency_lemma,
                'comment': comment
            })

    return commented_item


def main():

    commented_sent_list = []

    root_dir_list = os.listdir('./')
    for dir_name in root_dir_list:
        if (os.path.isdir(dir_name) and dir_name.startswith('D')):
            xml_file_list = os.listdir(dir_name)
            for xml_file_name in xml_file_list:
                xml_file_path = dir_name + '/' + xml_file_name
                result = getCommentedSentInfo(xml_file_path)
                commented_sent_list.extend(result)
            debug =  1

    f = open('commented_items.json', 'w', encoding='utf-8')
    f.write(json.dumps(commented_sent_list, indent=4, ensure_ascii=False, sort_keys=True))
    f.close()

    pass

if __name__ == '__main__':
    main()

