import re

EMOTES = (':-) :) :D :] =] =) :} :-D xD XD =D >:[ :-( :( :-[ :[ :{ ;( >:( ' +
          ':\'-( :\'( :\'-) :\') >:O :-O :O :-o :o :* ;-) ;) ;-] ;] ;D ' +
          '>:P :-P :P :-p :p >:\ >:/ :-/ :/ :\ =/ =\ :| :-| >:) >;) >:-) ' +
          '<3 </3').split()

PAIRS = ':: -- () [] == {} <> \'\''.split()
REVERSIBLE_CHARS = dict(PAIRS + list(map(lambda s: s[::-1], PAIRS)))


def _reverse_emote(emote):
    if all(c in REVERSIBLE_CHARS for c in emote):
        return ''.join(REVERSIBLE_CHARS[c] for c in emote[::-1])

    return None


EMOTES = EMOTES + list(filter(None, map(_reverse_emote, EMOTES)))


def get_words(string):
    # Adapted from: http://stackoverflow.com/a/367292/568785
    regex = '(' + '|'.join(map(re.escape, EMOTES)) + r')|[\w\'\-@]+|[.,!?;:]'
    results = re.finditer(regex, string, re.UNICODE | re.IGNORECASE)
    return map(lambda m: m.group(0), results)


def make_sentences(words):
    return ''.join(_join_words(words))


def _join_words(words):
    should_capitalize, space_before = True, False

    for word in words:
        original_word = word

        if _has_i(word) or (should_capitalize and
           not _is_punctuation(original_word)):

            word = _capitalize_first_letter(word)
            should_capitalize = False

        if space_before and original_word not in '.,!?;:':
            word = ' ' + word

        space_before = (original_word != '"')

        if original_word in '.!?':
            should_capitalize = True

        yield word


def _has_i(word):
    return word == 'i' or word.startswith('i\'')


def _is_punctuation(word):
    return word in '.,!?;:'


def _capitalize_first_letter(word):
    if len(word) == 1:
        return word.upper()
    else:
        return word[0].upper() + word[1:]
