import datefinder
from datetime import datetime
from flashtext import KeywordProcessor
import re

def extract_duration(text):
    date_pairs = []
    matches = datefinder.find_dates(text, source=True, index=True)

    matched_dates = []
    for item in matches:
        matched_dates.append(item)

    for i in range(len(matched_dates) - 1):
        if len(matched_dates[i][1]) < 4 or len(matched_dates[i + 1][1]) < 4:
            continue

        index_1 = matched_dates[i][2][1]
        index_2 = matched_dates[i + 1][2][0]

        if index_2 < (index_1 + 5):
            date_pairs.append((round(((matched_dates[i + 1][0] - matched_dates[i][0]).days / 365.0), 2),
                               matched_dates[i][1], matched_dates[i + 1][1], matched_dates[i][2][0],
                               matched_dates[i + 1][2][1]))

        elif "present" in text[index_1: index_1 + 10].lower():
            date_pairs.append((round(((datetime.now() - matched_dates[i][0]).days / 365.0), 2), matched_dates[i][1],
                               "present", matched_dates[i][2][0],
                               index_1 + text[index_1: index_1 + 10].lower().find("present") + 7))

    if len(matched_dates) > 0:
        item = matched_dates[-1]
        index_1 = item[2][1]
        index_2 = item[2][0]

        if "present" in text[index_1: index_1 + 10].lower():
            date_pairs.append((round(((datetime.now() - item[0]).days / 365.0), 2), item[1], "present", item[2][0],
                               index_1 + text[index_1: index_1 + 10].lower().find("present") + 7))

    return date_pairs

stopwords = set(["'ll", "'ve", 'a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'apr', 'april', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'aug', 'august', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'buy', 'by', 'c', 'ca', 'came', 'can', "can't", 'cannot', 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'dec', 'december', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'feb', 'feburary', 'feeling', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'friday', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'getty', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', "i'll", "i've", 'id', 'ie', 'if', 'im', 'images', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', "it'll", 'itd', 'its', 'itself', 'j', 'jan', 'january', 'jul', 'july', 'jun', 'june', 'just', 'k', 'keep', 'keeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'limit', 'line', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'mar', 'march', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'monday', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'nov', 'november', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'oct', 'october', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'rice', 'right', 'run', 's', 'said', 'same', 'saturday', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'sell', 'selves', 'sent', 'sep', 'september', 'seven', 'several', 'shall', 'shares', 'she', "she'll", 'shed', 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stock', 'stop', 'strong', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sunday', 'sup', 'sure', "t's", 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", "that've", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', "there'll", "there've", 'thereafter', 'thereby', 'thered', 'therefore', 'therein', 'thereof', 'therere', 'theres', 'thereto', 'thereupon', 'these', 'they', "they'll", "they've", 'theyd', 'theyre', 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thursday', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'tuesday', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', 'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', "we'll", "we've", 'wed', 'wednesday', 'welcome', 'went', 'were', 'werent', 'what', "what'll", 'whatever', 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', "who'll", 'whod', 'whoever', 'whole', 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', "you'll", "you've", 'youd', 'your', 'youre', 'yours', 'yourself', 'yourselves', 'z'])

def find_discipline(tmp_str):
    punctuation = set([".", ",", ";", "(", "-"])
    pun_regex = re.compile(r"[\w']+|[.,!?;(-]")
    token_list = pun_regex.findall(tmp_str)

    discipline_list = []
    try:
        if (token_list[0] == "of") or (token_list[0] == "in") or (token_list[0] == "degree" and token_list[1] == "in"):
            i = 1 if (token_list[0] == "in" or token_list[0] == "of") else 2
            token_len = len(token_list)
            while (i < token_len) and (token_list[i] not in punctuation) and (token_list[i] not in stopwords):
                if token_list[i].isalpha() == False:
                    discipline_list = []
                    break
                discipline_list.append(token_list[i].capitalize())
                if len(discipline_list) == 2:
                    break
                i = i + 1
    except:
        pass

    if len(discipline_list) == 0:
        discipline_list = ["NA"]

    return discipline_list

def find_educational_qualifications(text):
    keywords_deg = KeywordProcessor()

    diploma_list = ["diploma"]
    bachelor_list = ["bachelor", "bachelor's", "bachelors"]
    master_list = ["master", "master's", "masters"]
    phd_list = ["phd", "ph d", "p.h.d", "ph.d", "ph. d", "doctorate"]

    for item in diploma_list:
        keywords_deg.add_keyword(item, ("Diploma", "NA"))

    for item in bachelor_list:
        keywords_deg.add_keyword(item, ("Bachelor", "NA"))

    for item in master_list:
        keywords_deg.add_keyword(item, ("Master", "NA"))

    for item in phd_list:
        keywords_deg.add_keyword(item, ("PhD", "NA"))

    identified_edu = keywords_deg.extract_keywords(text, span_info=True)

    edu_list = []
    for item in identified_edu:
        start_pos = item[2] + 1
        end_pos = start_pos + 100
        t_len = len(text)
        if end_pos > t_len:
            end_pos = t_len
        tmp_str = text[start_pos:end_pos].lower()
        discipline_list = find_discipline(tmp_str)
        edu_list.append((item[0] + (" ".join(discipline_list),)))

    b_reg = re.compile(r"\bB[.]?\s?[A-Z][A-Z]?[a-z]*\b")
    b_list = [(i.group(), i.span()) for i in b_reg.finditer(text)]

    b_list_full = []
    for item in b_list:
        start_pos = item[1][1] + 1
        end_pos = start_pos + 100
        t_len = len(text)
        if end_pos > t_len:
            end_pos = t_len
        tmp_str = text[start_pos:end_pos].lower()
        discipline_list = find_discipline(tmp_str)

        b_list_full.append(("Bachelor", item[0].replace('.', '').replace(' ', ''), " ".join(discipline_list)))

    m_reg = re.compile(r"\bM[.]?\s?[A-Z][A-Z]?[a-z]*\b")
    m_list = [(i.group(), i.span()) for i in m_reg.finditer(text)]

    m_list_full = []
    for item in m_list:
        start_pos = item[1][0] + 1
        end_pos = start_pos + 100
        t_len = len(text)
        if end_pos > t_len:
            end_pos = t_len
        tmp_str = text[start_pos:end_pos].lower()
        discipline_list = find_discipline(tmp_str)

        m_list_full.append(("Master", item[0].replace('.', '').replace(' ', ''), " ".join(discipline_list)))

    edu_filtered = []
    if len(b_list_full) > 0:
        for item in edu_list:
            if item[0] != "Bachelor":
                edu_filtered.append(item)

    if len(m_list_full) > 0:
        for item in edu_list:
            if item[0] != "Master":
                edu_filtered.append(item)

    edu_filtered = sorted(list(set(edu_list + b_list_full + m_list_full)))

    return_list = []
    for item in edu_filtered:
        if item[1] != "NA" and item[2] != "NA":
            return_list.append(item[0] + ", " + item[1] + ", " + item[2])
        elif item[1] != "NA":
            return_list.append(item[0] + ", " + item[1])
        elif item[2] != "NA":
            return_list.append(item[0] + ", " + item[2])
        else:
            return_list.append(item[0])

    return return_list