import re

EMOTES = (':-) :) :D :] =] =) :} :-D xD XD =D >:[ :-( :( :-[ :[ :{ ;( >:( ' +
          ':\'-( :\'( :\'-) :\') >:O :-O :O :-o :o :* ;-) ;) ;-] ;] ;D ' +
          '>:P :-P :P :-p :p >:\ >:/ :-/ :/ :\ =/ =\ :| :-| >:) >;) >:-) ' +
          '<3 </3').split()

# Pairs of characters (ones that can be reversed)
PAIRS = ':: -- () [] == {} <> \'\''.split()
REVERSIBLE_CHARS = dict(PAIRS + list(map(lambda s: s[::-1], PAIRS)))


def _reverse_emote(emote):
    """
    Reverse an emoticon if it is possible to. If not, return None.
    """
    if all(c in REVERSIBLE_CHARS for c in emote):
        return ''.join(REVERSIBLE_CHARS[c] for c in emote[::-1])

    return None


# Final list of all emoticons possible
EMOTES = EMOTES + list(filter(None, map(_reverse_emote, EMOTES)))


def get_words(string):
    """
    Extract all word/emoticon/punctuation tokens froms an english sentence.

    Adapted from: http://stackoverflow.com/a/367292/568785
    """
    regex = '(' + '|'.join(map(re.escape, EMOTES)) + r')|[\w\'\-@]+|[.,!?;:]'
    results = re.finditer(regex, string, re.UNICODE | re.IGNORECASE)
    return map(lambda m: m.group(0), results)


def make_sentences(words):
    """
    Make sentences from word/emoticon/punctuation tokens.
    """
    return ''.join(_join_words(words))


def _join_words(words):
    """
    A naive English language word spacer, which uses basic grammar rules to
    properly space and capitalize words.
    """
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
    """
    Determine if a word is "I" or a contraction with "I".
    """
    return word == 'i' or word.startswith('i\'')


def _is_punctuation(word):
    """
    Determine if a word is a punctuation token.
    """
    return word in '.,!?;:'


def _capitalize_first_letter(word):
    """
    Capitalizes JUST the first letter of a word token.

    Note that str.title() doesn't work properly with apostrophes.
    ex. "john's".title() == "John'S"
    """
    if len(word) == 1:
        return word.upper()
    else:
        return word[0].upper() + word[1:]
