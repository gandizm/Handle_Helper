def match_position(rule,line):
    for i in range(len(rule)):
        if rule[i] == "_":
            continue
        elif rule[i] != line[i]:
            return False
    return True

rule = [1,4,3,4]
line = [1,2,3,4]
print(match_position(rule,line))