import itertools
import random

from pathlib import Path
from re import M

from bomisspell.utils import build_syl, get_syls, parse_syl, from_yaml
from bomisspell.sgnon_jung import get_sngon_jug_options
from bomisspell.mingzhi import get_mingzhi_options
from bomisspell.yang_jug import get_yang_jug_options

def get_misspelled_opt(syl_parts, mingzhi_mapping={}):
    """Return all the combination of misspelled syllable by shuffeling sngonjug, yangjug and replacing mingzhi by its similar pronounciation

    Args:
        syl_parts (dict): consit of all the possible component of a syllable which are sngonjug, mingzhi, jesjug and yangjug

    Returns:
        list: misspelled options of the syllable
    """
    if not mingzhi_mapping:
        mingzhi_mapping_path  = Path(__file__).parent / "resources/mingzhi_mapping.yaml"
        mingzhi_mapping = from_yaml(mingzhi_mapping_path.read_text(encoding='utf-8'))
    options = []
    options += get_sngon_jug_options(syl_parts)
    options += get_mingzhi_options(syl_parts, mingzhi_mapping)
    options += get_yang_jug_options(syl_parts)
    options.append(build_syl(syl_parts))
    return options

def shuffel_syl(misspelled_syls):
    misspelled_words = []
    for misspelled_option in list(itertools.product(*misspelled_syls)):
        misspelled_words.append("".join(misspelled_option))
    return misspelled_words

def get_misspelled_word(word, mingzhi_mapping = {}):
    misspelled_syls = []
    misspelled_words = []
    if not mingzhi_mapping:
        mingzhi_mapping_path  = Path(__file__).parent / "resources/mingzhi_mapping.yaml"
        mingzhi_mapping = from_yaml(mingzhi_mapping_path.read_text(encoding='utf-8'))
    syls = get_syls(word)
    for syl in syls:
        syl_parts = parse_syl(syl)
        misspelled_syls.append(get_misspelled_opt(syl_parts, mingzhi_mapping))
    if misspelled_syls:
        misspelled_words = shuffel_syl(misspelled_syls)
    else:
        misspelled_words.append(word)
    return misspelled_words
