import json
from typing import Dict, List, Tuple
from pathlib import Path
from pypinyin import Style, pinyin

data_dir = Path(__file__).parent / "data"
idiom_path = data_dir / "idioms.txt"
answer_path = data_dir / "answers.json"
ranged_path = data_dir / "ranged.txt"

# def get_answers() -> List[Any]:
#     with answer_path.open("r", encoding="utf-8") as f:
#         answers: List[Dict[str, str]] = json.load(f)
#         # answer = random.choice(answers)
#         return answers

# def random_idiom() -> Tuple[str, str]:
# answer["word"], answer["explanation"]

# fmt: off
# 声母
INITIALS = [
    "zh", "z", "y", "x", "w", "t", "sh", "s", "r", "q", "p",
    "n", "m", "l", "k", "j", "h", "g", "f", "d", "ch", "c", "b"
]
# 韵母
FINALS = [
    "ün", "üe", "üan", "ü", "uo", "un", "ui", "ue", "uang",
    "uan", "uai", "ua", "ou", "iu", "iong", "ong", "io", "ing",
    "in", "ie", "iao", "iang", "ian", "ia", "er", "eng", "en",
    "ei", "ao", "ang", "an", "ai", "u", "o", "i", "e", "a"
]


# fmt: on

def get_pinyin(idiom: str) -> Tuple[List[Tuple[str, str, str]], List]:
    pys = pinyin(idiom, style=Style.TONE3, v_to_u=True)
    # [['wei2'], ['bian1'], ['san1'], ['jue2']]
    pys_without_tone = []
    results = []
    for p in pys:
        py = p[0]
        if py[-1].isdigit():
            tone = py[-1]
            py = py[:-1]
        else:
            tone = ""
        initial = ""

        pys_without_tone.append(py)

        for i in INITIALS:
            if py.startswith(i):
                initial = i
                break
        # 疑问：如何区分声母中的h？
        final = ""
        for fin in FINALS:
            if py.endswith(fin):
                final = fin
                break
        results.append((initial, final, tone))  # 声母，韵母，声调
    return results, pys_without_tone


with answer_path.open("r", encoding="utf-8") as f:
    answers: List[Dict[str, str]] = json.load(f)

# for answer in answers:
#     answer_results, answer_pys = get_pinyin(answer["word"])
#     # print(answer_results)
#     answer_initials = []
#     answer_finals = []
#     answer_tones = str()
#
#     for each in answer_results:
#         answer_initials.append(each[0])
#         answer_finals.append(each[1])
#         answer_tones += each[2]
#     print(
#         answer_tones + ',' + ' '.join(answer_finals) + ',' + ' '.join(answer_initials) + ',' + ' '.join(
#             answer_pys) + ',' + answer["word"])
#     # print(get_pinyin(answer["word"]))

with open(ranged_path, 'w', encoding='utf-8') as file:
    for answer in answers:
        answer_results, answer_pys = get_pinyin(answer["word"])
        # print(answer_results)
        answer_initials = []
        answer_finals = []
        answer_tones = str()

        for each in answer_results:
            answer_initials.append(each[0])
            answer_finals.append(each[1])
            answer_tones += each[2]
        file.write(answer_tones + ',' + ' '.join(answer_finals) + ',' + ' '.join(answer_initials) + ',' + ' '.join(
            answer_pys) + ',' + answer["word"] + '\n')
        # print(
        #     answer_tones + ',' + ' '.join(answer_finals) + ',' + ' '.join(answer_initials) + ',' + ' '.join(
        #         answer_pys) + ',' + answer["word"])
        # print(get_pinyin(answer["word"]))
