import re
import string

def cleanup_words(words):
    result = []
    for word in words:
        word = word.strip(string.punctuation+' ')
        if not word:
            continue
        result.append(word)

    return ' '.join(result)

def clean_names(raw_names):

    pattern = '\W[Dd][\W]*[Bb][\W]*[Aa]\W'

    result = []
    for name in raw_names:
        name_parts = re.split(pattern,name)

        if len(name_parts) > 1:
            name_parts[0] = cleanup_words(re.split(r'[ _]',name_parts[0]))
            name_parts[1] = cleanup_words(re.split(r'[ _]',name_parts[1]))
            result.append((name_parts[0],name_parts[1]))
        else:
            name_parts[0] = cleanup_words(re.split(r'[ _]',name_parts[0]))
            result.append((name_parts[0],None))
    
    return result


RAW_NAMES = [
    'SPV Inc., DBA:    Super Company',
    'Michael Forsky LLC d.b.a F/B Burgers .',
    '*** Youthful You Aesthetics ***',
    'Aruna Indika (dba. NGXess)',
    'Diot SA,  -  D. B. A.     *Diot-Technologies',
    'PERFECT PRIVACY, LLC, d-b-a Perfection',
    'PostgreSQL DB Analytics',
    '/JAYE INC/',
    ' ETABLISSEMENTS SCHEPENS /D.B.A./ ETS_SCHEPENS',
    'DUIKERTRAINING OOSTENDE | D.B.A: D.T.O. '
]

CLEANED_NAME_PAIRS = [
    ('SPV Inc',                 'Super Company'),
    ('Michael Forsky LLC',      'F/B Burgers' ),
    ('Youthful You Aesthetics', None),
    ('Aruna Indika',            'NGXess'),
    ('Diot SA',                 'Diot-Technologies'),
    ('PERFECT PRIVACY LLC',     'Perfection'),
    ('PostgreSQL DB Analytics', None),
    ('JAYE INC',                None),
    ('ETABLISSEMENTS SCHEPENS', 'ETS SCHEPENS'),
    ('DUIKERTRAINING OOSTENDE', 'D.T.O')
]

result = clean_names(RAW_NAMES)

assert clean_names(RAW_NAMES) == CLEANED_NAME_PAIRS
