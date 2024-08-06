from pathlib import Path
import re


def match_line(include_rules, exclude_rules, line, include_rule_digits, include_rule_vowels, include_rule_consonants):
    # 提取行中的数字、韵母和声母部分
    line_parts = line.split(',')
    line_digits = line_parts[0]
    line_vowels = line_parts[1].split(' ')  # ranged韵母之间用空格分隔
    line_consonants = line_parts[2].split(' ')  # ranged声母之间用空格分隔

    # 检查数字部分是否匹配，考虑未知数下划线
    if not re.match(f"^{include_rule_digits[0].replace('_', '.')}$", line_digits):
        return False
    if len(include_rule_digits) == 2:
        if not match_elements(include_rule_digits[1].split(' '), line_digits):
            return False
    line_digits_left = pop_out_position(include_rule_digits[0], line_digits)
    # pop out

    # 检查韵母部分是否匹配，考虑可能的空格和顺序
    line_vowels_left = line_vowels
    if len(include_rules) > 1:
        if not is_all_empty_strings(include_rule_vowels[0].split(' ')):
            if not match_elements(include_rule_vowels[0].split(' '), line_vowels):
                return False
        if len(include_rule_vowels) == 2:
            line_vowels_left = pop_out_position(include_rule_vowels[1].split(' '), line_vowels)
            # pop out
            if not match_position(include_rule_vowels[1].split(' '), line_vowels):
                return False

    # 检查声母部分是否匹配，考虑可能的空格和顺序
    line_consonants_left = line_consonants
    if len(include_rules) > 2:
        if not is_all_empty_strings(include_rule_consonants[0].split(' ')):
            if not match_elements(include_rule_consonants[0].split(' '), line_consonants):
                return False
        if len(include_rule_consonants) == 2:
            line_consonants_left = pop_out_position(include_rule_consonants[1].split(' '), line_consonants)
            # pop out
            if not match_position(include_rule_consonants[1].split(' '), line_consonants):
                return False

    # 只要rule_left里有 在排除列表的里 的，就return False
    if any(digit in exclude_rules for digit in line_digits_left):
        return False
    if any(vowel in exclude_rules for vowel in line_vowels_left):
        return False
    if any(consonant in exclude_rules for consonant in line_consonants_left):
        return False
    # 如果所有部分都匹配，则返回True
    return True


# 匹配元素
def match_elements(rule, line):
    # 使用all()函数和列表推导式来检查rule中的所有元素是否都在line中
    return all(element in line for element in rule)


# 匹配位置
def match_position(rule, line):
    for i in range(len(rule)):
        if rule[i] == "_":
            continue
        elif rule[i] != line[i]:
            return False
    return True


def is_all_empty_strings(lst):
    # 使用all()函数和列表推导式检查列表中的所有元素是否都是空字符串
    return all(element == '' for element in lst)


def pop_out_position(in_rule, line):
    left_line = []
    for i in range(4):
        if in_rule[i] != line[i]:
            left_line.append(line[i])
    return left_line


data_dir = Path(__file__).parent / "data"
# idiom_path = data_dir / "idioms.txt"
# answer_path = data_dir / "answers.json"
ranged_path = data_dir / "ranged.txt"
# 注意：e.g.而的er是韵母，所以声母是空着的

with open(ranged_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
rules = input("示例： 2___/3 4,u i/uan i _ u,q l y f/q _ y f#1,m   可不带#。").split('#')
include_rules = rules[0].split(',')
include_rule_digits = include_rules[0].split('/')
include_rule_vowels = None  # 初始化为 None
include_rule_consonants = None  # 初始化为 None
if len(include_rules) > 1:
    include_rule_vowels = include_rules[1].split('/')  # 从第一个规则元素获取韵母/定位韵母
if len(include_rules) > 2:
    include_rule_consonants = include_rules[2].split('/')  # 从第二个规则元素获取声母/定位声母
# 目前还没做单字和拼音整体搜索，但数据预留好了可以轻松实现

exclude_rules = []
if len(rules) == 2:
    exclude_rules = rules[1].split(',')
"""
注意：如果第二/三/四个是灰的要排除，目前只能在*第一个已经确定位置*的情况下排除一次（目前没有做出现次数的规则）
"""
# 遍历行列表，检查是否有匹配的行
matched_line = None
for line in lines:
    if match_line(include_rules, exclude_rules, line, include_rule_digits, include_rule_vowels,
                  include_rule_consonants):
        matched_line = line
        print(line)
        print(line[-5:])
