from flashtext import KeywordProcessor
import collections
import os


def remove_punctuations(text):
    punc = '!"$%&\'()*,./:;<=>?@[\\]^_`{|}~'
    for ch in punc:
        text = text.replace(ch, '')
    return text


def preprocess_jd(text):
    text = remove_punctuations(text)
    return text


def generate_skills(text):
    try:
        df_skills = pd.read_csv("csv/skills.csv", header=None)
        skill_list = df_skills[0].tolist()

        for i, item in enumerate(skill_list):
            skill_list[i] = skill_list[i].replace('_', ' ')

        df_synon = pd.read_csv("csv/synon.csv")
        keys = df_synon["digital_product"].tolist()
        synon_keys = df_synon["keyword"].tolist()

        for i in range(len(keys)):
            keys[i] = keys[i].lower()
            synon_keys[i] = synon_keys[i].lower()

        keyword_processor = KeywordProcessor()
        for item in skill_list:
            keyword_processor.add_keyword(item)
        text = preprocess_jd(text)
        all_skills = keyword_processor.extract_keywords(text)

        for i, item in enumerate(all_skills):
            if item in keys:
                all_skills[i] = synon_keys[keys.index(item)]

        count_dict = collections.Counter(all_skills)
        return count_dict
    except:
        return None