import re

def split(input_filename, output_filename):
    with open(input_filename) as file:
        apl = file.read()
    new_apl = apl
    # Split by base then first detected parentheses (Left to Right)
    for line in apl.split("\n"):
        if line and "actions." in line and ",if=" in line and "|" in line:
            # Level 0 - Split at base level to simplify conditions
            condition_exps = split_base(line)
            if "(" in condition_exps and ")" in condition_exps and "|" in condition_exps:
                # Level 1 - Handle nested parentheses - Parentheses Depth Search
                new_conditions = split_condition(condition_exps)
            else:
                new_conditions = condition_exps
            new_apl = new_apl.replace(line + "\n", new_conditions, 1)
            print(f"\nReplacing line:\n{line}\nWith:\n{new_conditions}")
    print(new_apl)

    # Data Clean with proper = and +=/
    new_apl = re.sub(r"(actions\.\w+)=(?=\w+\,)", r"\1+=/", new_apl, re.MULTILINE)
    for line in new_apl.split("\n"):
        if "action" in line:
            new_apl = new_apl.replace(line, line.replace("+=/", "="), 1)
            break

    with open(output_filename, "w") as f:
         f.write(new_apl)

def split_base(line):
    level = 0
    new_conditions = ""
    current_string = ""
    line_idx = line.index("if=") + 3
    prefix, condition_exp = line[:line_idx], line[line_idx:]
    for idx, char in enumerate(condition_exp):
        current_string += char
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
        elif char == "|" and level == 0:
            new_conditions += prefix + current_string[:-1] + "\n"
            current_string = ""
            continue
        if idx == len(condition_exp) - 1 and new_conditions and current_string:
            new_conditions += prefix + current_string + "\n"
    if not new_conditions:
        new_conditions = line + "\n"
    return new_conditions


def split_condition(condition_exps):
    new_condition_exps = condition_exps
    for line in [x for x in new_condition_exps.split('\n') if x]:
        new_conditions = ""
        if "|" in line:
            line_idx = line.index("if=") + 3
            prefix, condition_exp = line[:line_idx], line[line_idx:]
            detected_level = get_first_operator_level(condition_exp)
            matched_cond = get_first_split_condition_at_level(condition_exp, detected_level)
            matched_cond = matched_cond.replace("(", "", 1) # Clean starting '('
            matched_cond = re.sub(r"\)$", "", matched_cond)
            for condition in matched_cond.split("|"):
                new_conditions += prefix + condition_exp.replace("(" + matched_cond + ")", condition, 1) + "\n"
            new_condition_exps = new_condition_exps.replace(line + "\n", new_conditions)
    if "|" in new_condition_exps:
        return split_condition(new_condition_exps)
    else:
        new_condition_exps = "\n".join(list(dict.fromkeys(new_condition_exps.split("\n"))))
        return new_condition_exps

def get_first_operator_level(condition_exp):
    level = 0
    detected_level = None
    current_string = ""
    for idx, char in enumerate(condition_exp):
        current_string += char
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
        elif char == "|":
            # Search until first detected level is found
            if not detected_level:
                detected_level = level
                break
    return detected_level

def get_first_split_condition_at_level(condition_exp, detected_level):
    level = 0
    current_string = ""
    op_detected = False
    for idx, char in enumerate(condition_exp):
        if char == "(":
            level += 1
        elif char == ")":
            level -= 1
        elif char == "|":
            op_detected = True
        if level >= detected_level:
            current_string += char
        elif op_detected and ")" in char and level - detected_level == -1:
            current_string += char
            return current_string
        elif level - detected_level == -1 and not op_detected:
            current_string = ""
    return None


# Input and output filename
split(input_filename="apl.simc",
      output_filename="splitter.simc")
