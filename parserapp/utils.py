import io
import os
import re
import nltk
import spacy
import pandas as pd
import docx2txt
from . import constants as cs
import string

from wordsegment import load, segment
load()
from spacy.matcher import Matcher
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords   

def extract_text_from_pdf(pdf_path):
    '''
    Helper function to extract the plain text from .pdf files
    :param pdf_path: path to PDF file to be extracted
    :return: iterator of string of extracted text
    '''
# iterate over all pages of PDF document
    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, 
                                      caching=True,
                                      check_extractable=True):
          # creating a resoure manager instance
            resource_manager = PDFResourceManager()
        # create a file handle
            fake_file_handle = io.StringIO()
        # creating a text converter object
            converter = TextConverter(resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
        # creating a page interpreter
            page_interpreter = PDFPageInterpreter(resource_manager, converter)
            page_interpreter.process_page(page)
 
            text = fake_file_handle.getvalue()
             # extract text
            yield text
 
            # close open handles
            converter.close()
            fake_file_handle.close()

def extract_text_from_doc(doc_path):
    '''
    Helper function to extract plain text from .doc or .docx files
    :param doc_path: path to .doc or .docx file to be extracted
    :return: string of extracted text
    '''
    temp = docx2txt.process(doc_path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)

def extract_text(file_path, extension):
    '''
    Wrapper function to detect the file extension and call text extraction function accordingly
    :param file_path: path of file of which text is to be extracted
    :param extension: extension of file `file_name`
    '''
    text = ''
    if extension == '.pdf':
        for page in extract_text_from_pdf(file_path):
            text += ' ' + page
    elif extension == '.docx' or extension == '.doc':
        text = extract_text_from_doc(file_path)
    return text

def extract_entity_sections(text):
    '''
    Helper function to extract all the raw text from sections of resume
    :param text: Raw text of resume
    :return: dictionary of entities
    '''
    text_split = [i.strip() for i in text.split('\n')]
    # sections_in_resume = [i for i in text_split if i.lower() in sections]
    entities = {}
    key = False
    for phrase in text_split:
        if len(phrase) == 1:
            p_key = phrase
        else:
            p_key = set(phrase.lower().split()) & set(cs.RESUME_SECTIONS)
        try:
            p_key = list(p_key)[0]
        except IndexError:
            pass
        if p_key in cs.RESUME_SECTIONS:
            entities[p_key] = []
            key = p_key
        elif key and phrase.strip():
            entities[key].append(phrase)

def extract_email(text):
    '''
    Helper function to extract email id from text
    :param text: plain text extracted from resume file
    '''
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", str(text))
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

def extract_name(text, matcher):
    email = extract_email(text)
    email = email.rsplit('@', 1)[0]
    email = re.sub (r'([^a-zA-Z ]+?)', ' ', email)
    email = segment(email)
    first_name = string.capwords(email[0])
    last_name = string.capwords(email[-1])
    pattern = [cs.NAME_PATTERN]
    matcher.add('NAME', None, *pattern)
    matches = matcher(text)
    for match_id, start, end in matches:
        span = text[start:end]
        if first_name in span.text:
            return span.text
        elif last_name in span.text:
            return span.text
        elif first_name.upper() in span.text:
            return span.text
        elif last_name.upper() in span.text:
            return span.text
def extract_mobile_number(text):
    phone = re.findall(re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'), text)

    if phone:
        number = ''.join(phone[0])

        if text.find(number) >= 0 and len(number) < 20:
            return number
    return None


def extract_skills(nlp_text, noun_chunks):
    '''
    Helper function to extract skills from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # reading the csv file
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), './staticfiles/skills.csv')) 
    # extract values
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams (example: machine learning)
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_non_technical_skills(nlp_text, noun_chunks):
    '''
    Helper function to extract non technical skills from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), './staticfiles/non_technical_skills.csv')) 
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
    
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()

def extract_education(nlp_text):
    '''
    Helper function to extract education from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: tuple of education degree and year if year if found else only returns education degree
    '''
    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            tex = re.sub(r'[?|$|.|!|,]', r'', tex)
            if tex.upper() in cs.EDUCATION and tex not in cs.STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(cs.YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education

def extract_nationality(nlp_text, noun_chunks):
    '''
    Helper function to extract candidate nationality from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: nationality of candidate
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), './staticfiles/nationality_data.csv')) 
    nation = list(data.columns.values)
    nationality = []
    # check for one-grams
    for token in tokens:
        if token.lower() in nation:
            nationality.append(token)
    
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in nation:
            nationality.append(token)
    return [i.capitalize() for i in set([i.lower() for i in nationality])]

def extract_languages(nlp_text, noun_chunks):
    '''
    Helper function to extract candidate nationality from spacy nlp text
    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: nationality of candidate
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), './staticfiles/languages.csv')) 
    languages = list(data.columns.values)
    languages_spoken = []
    # check for one-grams
    for token in tokens:
        if token.lower() in languages:
            languages_spoken.append(token)
    
    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in languages:
            languages_spoken.append(token)
    return [i.capitalize() for i in set([i.lower() for i in languages_spoken])]

def extract_address(text):
     nlp = spacy.load('en_core_web_sm')
     doc = nlp(text)
     for ent in doc.ents:
         # geopolitical entities
         if ent.label_ in ['LOC', 'GPE']:
             return ent.text

def extract_experience(resume_text):
    '''
    Helper function to extract experience from resume text
    :param resume_text: Plain resume text
    :return: list of experience
    '''
    wordnet_lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # word tokenization 
    word_tokens = nltk.word_tokenize(resume_text)

    # remove stop words and lemmatize  
    filtered_sentence = [w for w in word_tokens if not w in stop_words and wordnet_lemmatizer.lemmatize(w) not in stop_words] 
    sent = nltk.pos_tag(filtered_sentence)

    # parse regex
    cp = nltk.RegexpParser('P: {<NNP>+}')
    cs = cp.parse(sent)
    
    # for i in cs.subtrees(filter=lambda x: x.label() == 'P'):
    #     print(i)
    
    test = []
    
    for vp in list(cs.subtrees(filter=lambda x: x.label()=='P')):
        test.append(" ".join([i[0] for i in vp.leaves() if len(vp.leaves()) >= 2]))

    # Search the word 'experience' in the chunk and then print out the text after it
    x = [x[x.lower().index('experience') + 10:] for i, x in enumerate(test) if x and 'experience' in x.lower()]
    return x

