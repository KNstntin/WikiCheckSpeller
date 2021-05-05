import bz2
import os
import sys
import xml.etree.ElementTree as ET
from tqdm import tqdm
import wget


DIR_PATH = sys.path[0] + "\\"


class SpellChecker:
    _russian_letters = set('йцукеёнгшщзхъфывапролджэячсмитьбю')

    def _strip_tag_name(self, t):
        idx = t.rfind("}")
        if idx != -1:
            t = t[idx + 1:]
        return t

    def _process_string(self, string):
        new_s = list()
        check_flag = False
        for x in string:
            x = x.lower()
            if x in self._russian_letters:
                new_s.append(x)
                check_flag = True
            elif check_flag:
                new_s.append(' ')
                check_flag = False
        return (''.join(new_s)).split()

    def save_dictionary(self, path):
        with open(path, 'w', encoding='utf-8') as f:
            for x in tqdm(self.dictionary, desc='Making the dictionary file'):
                f.write(x + '\n')

    def __init__(self, path_dictionary=DIR_PATH + 'dictionary.txt'):
        try:
            with open(path_dictionary, 'r', encoding='utf-8') as f:
                self.dictionary = set(x[:-1] for x in f.readlines())
        except (OSError, IOError):
            print('Downloading zip file... ')
            url = "https://dumps.wikimedia.org/ruwiki/20210420/ruwiki-20210420-pages-articles-multistream.xml.bz2"
            wget.download(url, DIR_PATH + "ruwiki.xml.bz2")
            with open(DIR_PATH + "ruwiki.xml", 'wb') as new_file,\
                    bz2.BZ2File(DIR_PATH + "ruwiki.xml.bz2", 'rb') as file:
                for data in tqdm(iter(lambda: file.read(100 * 1024), b''), total=241546, desc='Unzipping process'):
                    new_file.write(data)
            os.remove(DIR_PATH + "ruwiki.xml.bz2")
            events = ("start", "end")
            s = set()
            for event, elem in tqdm(ET.iterparse(DIR_PATH + "ruwiki.xml", events=events),
                                    desc='Processing wiki', total=157382804):
                tname = self._strip_tag_name(elem.tag)
                if event == 'end' and (tname == 'title' or tname == 'text'):
                    s |= set(self._process_string(str(elem.text)))
                elem.clear()
            self.dictionary = s
            os.remove(DIR_PATH + "ruwiki.xml")
            self.save_dictionary(DIR_PATH + "dictionary.txt")

    def check(self, sentence):
        for word in self._process_string(sentence):
            if word not in self.dictionary:
                return False
        return True
