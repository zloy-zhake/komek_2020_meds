import re
from typing import List
from fuzzywuzzy import process, fuzz

# smartness levels:
SIMPLE_MATCHING: int = 0
FUZZY_WUZZY_MATCING: int = 1
NER: int = 2
NER_AND_FUZZY_WUZZY_MATCING: int = 3

# regex'ы для токенизации
ENGLISH = "abcdefghijklmnopqrstuvwxyz"
KAZAKH = "аәбвгғдеёжзийкқлмнңоөпрстуұүфхһцчшщъыіьэюя"
LETTERS_RE = f"[{ENGLISH}{KAZAKH}]"
NON_LETTERS_RE = f"[^{ENGLISH}{KAZAKH}]"

# набор букв для очистки
LETTERS_SET = set(f"{ENGLISH}{KAZAKH}")


def get_shortest_medication_name_len() -> int:
    """TODO:
    """
    with open(file="./data/medications.txt", mode="r") as f:
        return min(len(x.strip()) for x in f)


SHORTES_MEDICATION_NAME_LEN = get_shortest_medication_name_len()


def get_medications_set() -> set:
    """TODO:
    """
    with open(file="./data/medications.txt") as f:
        result_set = {line.strip() for line in f}

    return result_set


MEDICATIONS_SET = get_medications_set()


def simple_tokenize(text: str) -> str:
    """TODO:
    """
    matches = [
        match
        for match in re.finditer(
            pattern=f"{LETTERS_RE}{NON_LETTERS_RE}", string=text
        )
    ]
    for match in matches[::-1]:
        text = text[: match.start() + 1] + " " + text[match.end() - 1 :]

    matches = [
        match
        for match in re.finditer(
            pattern=f"{NON_LETTERS_RE}{LETTERS_RE}", string=text
        )
    ]
    for match in matches[::-1]:
        text = text[: match.start() + 1] + " " + text[match.end() - 1 :]

    result = re.sub(pattern=" +", repl=" ", string=text)

    return result


def preprocess_clean_str_to_list(text: str) -> List[str]:
    """TODO:
    """
    # lowercase
    proc_text = text.strip().lower()

    # токенизация
    proc_text = simple_tokenize(text=proc_text)

    # ограничение по длине
    proc_text_list = [
        token
        for token in proc_text.split()
        if len(token) >= SHORTES_MEDICATION_NAME_LEN
    ]

    # удаление не-слов
    result = [
        token
        for token in proc_text_list
        if len(set(token).intersection(LETTERS_SET)) > 0
    ]

    return result


def get_medications_list_from_text(
    text: str, smartness: int = SIMPLE_MATCHING
) -> List[str]:
    """TODO:
    """
    preprocessed_words = preprocess_clean_str_to_list(text=text)
    result_meds: List[str] = list()

    if smartness == SIMPLE_MATCHING:
        result_meds = list(
            MEDICATIONS_SET.intersection(set(preprocessed_words))
        )

    elif smartness == FUZZY_WUZZY_MATCING:
        for word in preprocessed_words:
            search_res = process.extractOne(
                query=word, choices=MEDICATIONS_SET, scorer=fuzz.token_set_ratio
            )
            if search_res and search_res[1] > 86:
                if search_res[0] not in result_meds:
                    result_meds.append(search_res[0])

    elif smartness == NER:
        pass

    elif smartness == NER_AND_FUZZY_WUZZY_MATCING:
        pass

    return result_meds
