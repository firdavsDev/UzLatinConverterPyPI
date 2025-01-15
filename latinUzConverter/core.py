# -*- coding: utf-8 -*-
"""
Usage:

from converter import LatinUzConverter

converter = LatinUzConverter()

#Transliterate cyrillic text to latin (transliterate method)
text = "Салом, дунё!"
print(converter.transliterate(text, "latin"))

#Transliterate latin text to cyrillic (transliterate method)
text = "Salom, dunyo!"
print(converter.transliterate(text, "cyrillic"))

#Output:
# Salom, dunyo!
# Салом, дунё!

"""

import re

from .letters import (
    CYRILLIC_TO_LATIN,
    CYRILLIC_VOWELS,
    E_WORDS,
    LATIN_TO_CYRILLIC,
    LATIN_VOWELS,
    SOFT_SIGN_WORDS,
    TS_WORDS,
)


class LatinUzConverter:
    """
    Here have 3 methods:

    1. to_latin(text: str) -> str
    2. to_cyrillic(text: str) -> str
    3. transliterate(text:str, to_variant: str) -> str (to_variant can be "latin" or "cyrillic")

    """

    def to_cyrillic(self, text: str) -> str:
        """Transliterate latin text to cyrillic  using the following rules:

        1. ye = е in the beginning of a word or after a vowel
        2. e = э in the beginning of a word or after a vowel
        3. ц exception words
        4. э exception words

        """
        # These compounds must be converted before other letters
        compounds_first = {
            "ch": "ч",
            "Ch": "Ч",
            "CH": "Ч",
            # this line must come before 's' because it has an 'h'
            "sh": "ш",
            "Sh": "Ш",
            "SH": "Ш",
            # This line must come before 'yo' because of it's apostrophe
            "yo‘": "йў",
            "Yo‘": "Йў",
            "YO‘": "ЙЎ",
        }
        compounds_second = {
            "yo": "ё",
            "Yo": "Ё",
            "YO": "Ё",
            # 'ts': 'ц', 'Ts': 'Ц', 'TS': 'Ц',  # No need for this, see TS_WORDS
            "yu": "ю",
            "Yu": "Ю",
            "YU": "Ю",
            "ya": "я",
            "Ya": "Я",
            "YA": "Я",
            "ye": "е",
            "Ye": "Е",
            "YE": "Е",
            # different kinds of apostrophes
            "o‘": "ў",
            "O‘": "Ў",
            "oʻ": "ў",
            "Oʻ": "Ў",
            "g‘": "ғ",
            "G‘": "Ғ",
            "gʻ": "ғ",
            "Gʻ": "Ғ",
        }
        beginning_rules = {
            "ye": "е",
            "Ye": "Е",
            "YE": "Е",
            "e": "э",
            "E": "Э",
        }
        after_vowel_rules = {
            "ye": "е",
            "Ye": "Е",
            "YE": "Е",
            "e": "э",
            "E": "Э",
        }
        exception_words_rules = {
            "s": "ц",
            "S": "Ц",
            "ts": "ц",
            "Ts": "Ц",
            "TS": "Ц",  # but not tS
            "e": "э",
            "E": "э",
            "sh": "сҳ",
            "Sh": "Сҳ",
            "SH": "СҲ",
            "yo": "йо",
            "Yo": "Йо",
            "YO": "ЙО",
            "yu": "йу",
            "Yu": "Йу",
            "YU": "ЙУ",
            "ya": "йа",
            "Ya": "Йа",
            "YA": "ЙА",
        }

        # standardize some characters
        # the first one is the windows string, the second one is the mac string
        text = text.replace("ʻ", "‘")

        def replace_soft_sign_words(m):
            word = m.group(1)
            if word.isupper():
                result = SOFT_SIGN_WORDS[word.lower()].upper()
            elif word[0].isupper():
                result = SOFT_SIGN_WORDS[word.lower()]
                result = result[0].upper() + result[1:]
            else:
                result = SOFT_SIGN_WORDS[word.lower()]
            return result

        for word in SOFT_SIGN_WORDS:
            text = re.sub(r"\b(%s)" % word, replace_soft_sign_words, text, flags=re.U)

        def replace_exception_words(m):
            """Replace ц (or э) only leaving other characters unchanged"""
            return "%s%s%s" % (
                m.group(1)[: m.start(2)],
                exception_words_rules[m.group(2)],
                m.group(1)[m.end(2) :],
            )

        # loop because of python's limit of 100 named groups
        for word in list(TS_WORDS.keys()) + list(E_WORDS.keys()):
            text = re.sub(r"\b(%s)" % word, replace_exception_words, text, flags=re.U)

        # compounds
        text = re.sub(
            r"(%s)" % "|".join(compounds_first.keys()),
            lambda x: compounds_first[x.group(1)],
            text,
            flags=re.U,
        )

        text = re.sub(
            r"(%s)" % "|".join(compounds_second.keys()),
            lambda x: compounds_second[x.group(1)],
            text,
            flags=re.U,
        )

        text = re.sub(
            r"\b(%s)" % "|".join(beginning_rules.keys()),
            lambda x: beginning_rules[x.group(1)],
            text,
            flags=re.U,
        )

        text = re.sub(
            r"(%s)(%s)" % ("|".join(LATIN_VOWELS), "|".join(after_vowel_rules.keys())),
            lambda x: "%s%s" % (x.group(1), after_vowel_rules[x.group(2)]),
            text,
            flags=re.U,
        )

        text = re.sub(
            r"(%s)" % "|".join(LATIN_TO_CYRILLIC.keys()),
            lambda x: LATIN_TO_CYRILLIC[x.group(1)],
            text,
            flags=re.U,
        )

        return text

    def to_latin(self, text: str) -> str:
        """Transliterate cyrillic text to latin using the following rules:
        1. ц = s at the beginning of a word.
        ц = ts in the middle of a word after a vowel.
        ц = s in the middle of a word after consonant (DEFAULT in CYRILLIC_TO_LATIN)
            цирк = sirk
            цех = sex
            федерация = federatsiya
            функция = funksiya
        2. е = ye at the beginning of a word or after a vowel.
        е = e in the middle of a word after a consonant (DEFAULT).
        3. Сентябр = Sentabr, Октябр = Oktabr
        """
        beginning_rules = {"ц": "s", "Ц": "S", "е": "ye", "Е": "Ye"}
        after_vowel_rules = {"ц": "ts", "Ц": "Ts", "е": "ye", "Е": "Ye"}

        text = re.sub(
            r"(сент|окт)([яЯ])(бр)",
            lambda x: "%s%s%s"
            % (x.group(1), "a" if x.group(2) == "я" else "A", x.group(3)),
            text,
            flags=re.IGNORECASE | re.U,
        )

        text = re.sub(
            r"\b(%s)" % "|".join(beginning_rules.keys()),
            lambda x: beginning_rules[x.group(1)],
            text,
            flags=re.U,
        )

        text = re.sub(
            r"(%s)(%s)"
            % ("|".join(CYRILLIC_VOWELS), "|".join(after_vowel_rules.keys())),
            lambda x: "%s%s" % (x.group(1), after_vowel_rules[x.group(2)]),
            text,
            flags=re.U,
        )

        text = re.sub(
            r"(%s)" % "|".join(CYRILLIC_TO_LATIN.keys()),
            lambda x: CYRILLIC_TO_LATIN[x.group(1)],
            text,
            flags=re.U,
        )

        return text

    def transliterate(self, to_variant: str) -> str:
        """
        Transliterate text to the desired variant

        :param to_variant: str (can be "latin" or "cyrillic")

        :return: str
        """
        try:
            if to_variant == "cyrillic":
                text = self.to_cyrillic(text)
            elif to_variant == "latin":
                text = self.to_latin(text)
            else:
                raise ValueError("to_variant should be 'latin' or 'cyrillic'")
            return text
        except Exception as e:
            raise f"Error occurred: {e}"
