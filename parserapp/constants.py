import re
from nltk.corpus import stopwords

NAME_PATTERN      = [{'POS': 'PROPN'}, {'POS': 'PROPN'}] #pos part of speech #proper noun


# Education (Upper Case Mandatory)
EDUCATION   = ['BE','B.E.', 'B.E', 'BS', 'B.SC','C.A.','C.A.','B.COM','B. COM','M. COM', 'M.COM','M. COM .',
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 'HONORS', 'COMPUTER SCIENCE'
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH',
            'PHD', 'PHD', 'PH.D', 'PH.D.','MBA','MBA','Statistics', 'POST-GRADUATE','5 YEAR INTEGRATED MASTERS','MASTERS',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')#first number chai + 1-9 dekhi start vayera 0-9 samma end vayeko number chai extract garcha

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'#a-z 

NUMBER            = r'\d+'#hold integer value


# For finding date ranges
MONTHS_SHORT      = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
MONTHS_LONG       = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'
MONTH             = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'#combining
YEAR              = r'(((20|22)(\d{2})))'#extract 

STOPWORDS         = set(stopwords.words('english'))#remove stopwords

RESUME_SECTIONS = [
                    'accomplishments',
                    'experience',
                    'education',
                    'interests',
                    'projects',
                    'professional experience',
                    'publications',
                    'skills',
                ]