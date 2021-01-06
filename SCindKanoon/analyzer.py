import re
import regex
import pymongo
import string 
import datefinder
import spacy

nlp = spacy.load('en_core_web_sm')

client = pymongo.MongoClient("mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["SCdata"]
col = db["SCdata01"]

sal_re_indicators = ['Shri', 'Sh\.', 'Sh', 'Mr\.', 'Mr', 'Miss', 'Ms\.', 'Ms', 'Mrs\.', 'Ms', 'Dr\.', 'Dr']

section_re_indicators = ['s\.', 'section', 'rule', 'article', 'chapter', 'clause', 'paragraph', 'explanation']

law_re_indicators = ['Act', 'Statute', 'Rules', 'Regulations', 'Reference', 'Constitution', 'Circular', 'Notice', 'Notification']

case_re_indicators = ['v', 'v\.', 'vs', 'vs\.', 'Vs', 'Vs\.', 'versus', 'Versus']

counsel_petitioner_re_indicators = ['for(\s+)(the)?(\s+)((appellant(s?))|(petitioner(s?)))(\.?)']

counsel_respondent_re_indicators = ['for(\s+)(the)?(\s+)respondent(s?)(\.?)']

list_stop = ['of', 'for', 'the', 'and', 'under', '\.', ',', '\(', '\)', '\-']

list_stop_regex = '('+'|'.join(list_stop)+')'

first_cap_regex = '([A-Z]\S*\s*('+list_stop_regex+'*\s*'+'([A-Z]|\d)\S*\s*)+)'

law_regex_no_words = first_cap_regex+'(((,|of)\s+)?(\d)*\s*)*'


def find_assoc_law(text):
    return re.match(law_regex_no_words, text)

def find_first_set_cap_words(str_in):
    m = re.findall(first_cap_regex, str_in)
    if m:
        if len(m) > 0:
            return m[0][0]
    return None

def find_last_set_cap_words(str_in):
    m = re.findall(first_cap_regex, str_in)
    if m:
        if len(m) > 0:
            return m[-1][0]
    return None

def extend_dict(dict_a, dict_b):
    for k in dict_b:
        if k in dict_a:
            dict_a[k].extend(dict_b[k])
        else:
            dict_a[k] = dict_b[k][:]

def get_salutation_regexp(sal_re_indicators):
    re_sal_str = '('+'|'.join(sal_re_indicators)+')'
    salutation_regexp = re_sal_str+'(\s+)'
    print (salutation_regexp)
    return salutation_regexp

def get_section_regexp(section_indicators):
    re_section_str = '('+'|'.join(section_indicators)+')'
    section_regexp = '(((\s|,|\.)+)'+re_section_str+'(\s+)(\S+)(\s?))((of|in)\s+(the\s+)?)?'
    print (section_regexp)
    return section_regexp

def get_law_regexp(law_re_indicators):
    return '('+'|'.join(law_re_indicators)+')'

def get_case_regexp(case_indicators):
    re_case_str = '('+'|'.join(case_indicators)+')'
    case_regexp = '(\s+)'+re_case_str+'(\s+)'
    print (case_regexp)
    return case_regexp

def get_counsel_regexp(counsel_indicators):
    re_counsel_str = '('+'|'.join(counsel_indicators)+')'
    counsel_regexp = '(\s+)'+re_counsel_str
    print (counsel_regexp)
    return counsel_regexp

def find_laws(law_dict, sent_text, law_regexp):
    sent_laws = []
    for m in re.finditer(law_regex_no_words, sent_text):
        law = m.group(0).strip()
        if re.search(law_regexp, law):
            if law not in law_dict:
                law_dict[law] = []
            sent_laws.append((law, m.start(), m.end()))
    return sent_laws
        
def find_section_and_law(law_dict, sent_text, section_regexp, law_regexp, law_prev, sent_laws):
    curr_idx = -1
    if len(sent_laws) > 0:
        curr_idx = 0
    for m in re.finditer(section_regexp, sent_text, re.IGNORECASE):
        if curr_idx >= 0:
            while curr_idx < len(sent_laws) and m.start() > sent_laws[curr_idx][2]:
                law_prev = sent_laws[curr_idx][0]
                curr_idx += 1
        section_str = m.group(1).strip()
        if m.group(6):
            assoc_law = find_assoc_law(sent_text[m.end():])
            if assoc_law: 
                curr_law = assoc_law.group(0).strip()
                if re.search(law_regexp, curr_law):
                    law_prev = curr_law
                else:
                    section_str += ', '+curr_law
        if len(law_prev) > 0 and law_prev not in law_dict:
            law_dict[law_prev] = []
        if len(law_prev) > 0:
            law_dict[law_prev].append(section_str)
    if len(sent_laws) > 0:
        law_prev = sent_laws[-1][0]
    return law_prev

def normalize_person_set(set_persons, sal_regexp):
    new_set_persons = set()
    for person in set_persons:
        person = re.sub(sal_regexp, '', person)
        new_set_persons.add(person)
    return new_set_persons
            
def find_case(sent_text, case_regexp):
    list_cases = []
    last_case = ''
    for m in re.finditer(case_regexp, sent_text):
        first_case = find_last_set_cap_words(sent_text[:m.start()])
        if first_case and ' and ' in first_case and first_case.strip() == last_case.strip():
            curr = first_case.split(' and ')
            try:
                past_case_split = list_cases[-1].split(mid)
                list_cases[-1] = past_case_split[0]+mid+curr[0]
            except:
                #print "oops case"
                pass
            first_case = curr[1]
        mid = m.group(0)
        last_case = find_first_set_cap_words(sent_text[m.end():])
        if first_case and mid and last_case:
            list_cases.append(first_case.strip()+mid+last_case.strip())
        else:
            print (first_case, mid, last_case)
    return list_cases
        
def find_counsel(sent_text, start, end):
    counsels = set()
    sent_text_split = re.split(',\s?', sent_text[start:end])
    if 'and' in sent_text_split[-1]:
        sent_text_split[-1] = re.split('\s?and\s', sent_text_split[-1])
    if '&' in sent_text_split[-1]:
        sent_text_split[-1] = re.split('\s?&\s', sent_text_split[-1])
    final_phrase_list = []
    for sublist in sent_text_split:
        if len(sublist) > 0:
            if type(sublist) is list:
                for item in sublist:
                    if len(item) > 0:
                        final_phrase_list.append(item)
            else:
                final_phrase_list.append(sublist)
    for phrase in final_phrase_list:
        phrase_doc = nlp(phrase)
        if len(phrase_doc.ents) > 0:
            last_ent = phrase_doc.ents[-1]
            if last_ent.label_ == 'PERSON' and phrase.endswith(last_ent.text) and len(last_ent.text.split()) > 1:
                counsels.add(last_ent.text)
            else:
                m = find_last_set_cap_words(phrase)
                if m and len(m.split()) > 1:
                    counsels.add(m)
        else:
            m = find_last_set_cap_words(phrase)
            if m and len(m.split()) > 1:
                counsels.add(m)
    return counsels

def remove_stop(text):
    text = text.lower()
    text = re.sub(list_stop_regex, ' ', text)
    text = re.sub(' +', ' ', text)
    return text.strip()

def combine_laws(law_dict):
    init_keys = list(law_dict.keys())
    mapping = {}
    for law in init_keys:
        law_norm = remove_stop(law)
        if law_norm in law_dict:
            if mapping[law_norm][1] < len(law_dict[law]):
                mapping[law_norm] = (law, len(law_dict[law]))
            law_dict[law_norm].extend(law_dict[law])
        else:
            mapping[law_norm] = (law, len(law_dict[law]))
            law_dict[law_norm] = law_dict[law][:]
        del law_dict[law]
    new_keys = list(law_dict.keys())
    for law in new_keys:
        law_dict[mapping[law][0]] = law_dict.pop(law)
        
def repr_laws(law_dict):
    str_laws_with_sections = ""
    for law in law_dict:
        str_laws_with_sections += law+':'
        str_laws_with_sections += '|'.join(law_dict[law]) + ';'
    return str_laws_with_sections[:-1]

def handler(signum, frame):
    print ("Forever is over!")
    raise Exception()

def find_petitioner(petitioner, txt):
    if len(petitioner) == 0:
        try:
            
            petitioner = re.search('((([A-Z](\S*)(\s?))|(and(\s?))|(&(\s?)))+)((\.)+)(\s?)(Appellant|APPELLANT)', txt).group(1)
        except Exception as exc:
            
            print ("oops petitioner")
            petitioner = ''
    return petitioner




sal_regexp = get_salutation_regexp(sal_re_indicators)
section_regexp = get_section_regexp(section_re_indicators)
law_regexp = get_law_regexp(law_re_indicators)
case_regexp = get_case_regexp(case_re_indicators)
counsel_petitioner_regexp = get_counsel_regexp(counsel_petitioner_re_indicators)
counsel_respondent_regexp = get_counsel_regexp(counsel_respondent_re_indicators)
for doc in col.find():
    print ('...')
    url = (doc['url'])
    law_dict = {}
    case_list = []
    petitioner_counsel = set()
    respondent_counsel = set()
    para_text = doc['judgement_text']
    try:
        doc_nlp = nlp(para_text)
        law_prev = ''
        for sent in doc_nlp.sents:
            txt_lower = sent.text.lower()
            sent_laws = find_laws(law_dict, sent.text, law_regexp)
            if re.search(section_regexp, sent.text, re.IGNORECASE):
                law_prev = find_section_and_law(law_dict, sent.text, section_regexp, law_regexp, law_prev, sent_laws)
            else:
                if len(sent_laws) > 0:
                    law_prev = sent_laws[-1][0]
            if re.search(case_regexp, sent.text):
                case_list.extend(find_case(sent.text, case_regexp))
            start = 0
            for m in re.finditer(counsel_petitioner_regexp, sent.text, re.IGNORECASE):
                if m:
                    petitioner_counsel |= find_counsel(sent.text, start, m.start())
                    start = m.end()
            start = 0
            for m in re.finditer(counsel_respondent_regexp, sent.text, re.IGNORECASE):
                if m:
                    respondent_counsel |= find_counsel(sent.text, start, m.start())
                    start = m.end()
    except:
        print ("oops parsing")
    petitioner_counsel = normalize_person_set(petitioner_counsel, sal_regexp)
    respondent_counsel = normalize_person_set(respondent_counsel, sal_regexp)
    combine_laws(law_dict)
    col.update_one({"url": url},{"$set": {"petitioner_counsel":list(petitioner_counsel)}}, False, True)
    col.update_one({"url": url},{"$set": {"respondent_counsel":list(respondent_counsel)}}, False, True)
    col.update_one({"url": url},{"$set": {"provisions_referred":repr_laws(law_dict)}}, False, True)
    col.update_one({"url": url},{"$set": {"cases_referred":case_list}}, False, True)
    # generate provisions, cases, both counsels
    # add generated fields into existing document

