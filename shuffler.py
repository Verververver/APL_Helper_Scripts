import re

# Assumes no duplicate lines
# Designed so that it allows comments inbetween, hopefully

def shuffle(input_filename, output_filename, action_line_idx=1, set_iterations=True, max_iterations=600000, profile_sets=60):
    with open(input_filename) as file:
        apl = file.read()

    # Get action idx then clean from new apl
    actions_apl = [s for s in apl.split("\n") if "actions." in s]
    shuffle_line = actions_apl[action_line_idx-1]
    new_apl = apl.replace(shuffle_line + "\n", "")
    if "+=/" not in shuffle_line:
        eql_idx = shuffle_line.find("=")
        shuffle_line = shuffle_line[:eql_idx] + '+' + shuffle_line[eql_idx] + '/' + shuffle_line[eql_idx + 1:]

    # Perform shuffle
    perms = ""
    action_idx = 1
    perms_count = 0

    for idx, line in enumerate(new_apl.split("\n")):
        print(line)
        if "actions." in line:
            temp_apl = new_apl
            temp_apl = re.sub(r"{0}(\n|$)".format(re.escape(line)), shuffle_line + f"\n#---Line moved above to Line{action_idx}---#\n" + line + "\n", temp_apl)
            temp_apl = re.sub(r"(actions\.\w+)=(?=\w+\,)", r"\1+=/", temp_apl)
            for temp_line in temp_apl.split("\n"):
                if "actions." in temp_line:
                    temp_apl = temp_apl.replace(temp_line, temp_line.replace("+=/", "="), 1)
                    break
            if temp_apl != apl:
                perms = perms + ("\n\n" + temp_apl.replace("mage=", "copy=", 1).replace("copy=\"", "copy=\"L" + str(action_line_idx) + "toL" + str(action_idx) + "|", 1))
                perms_count += 1
            action_idx += 1
            # print(perms)

        # Forcefully add last line since list removed original line so count is off by 1
        if action_idx == len(actions_apl):
            temp_apl = new_apl
            temp_apl = re.sub(r"{0}(\n|$)".format(re.escape(line)), line + "\n" + shuffle_line + f"\n#---Line moved above to Line{action_idx}---#\n",
                              temp_apl)
            temp_apl = re.sub(r"(actions\.\w+)=(?=\w+\,)", r"\1+=/", temp_apl)
            for temp_line in temp_apl.split("\n"):
                if "actions." in temp_line:
                    temp_apl = temp_apl.replace(temp_line, temp_line.replace("+=/", "="), 1)
                    break
            if temp_apl != apl:
                perms = perms + ("\n\n" + temp_apl.replace("mage=", "copy=", 1).replace("copy=\"", "copy=\"L" + str(action_line_idx) + "toL" + str(action_idx) + "|", 1))
                perms_count += 1
            action_idx += 1
            # print(perms)

    with open(output_filename, "w") as f:
        if set_iterations:
            if perms_count > profile_sets:
                iterations = int(max_iterations / profile_sets)
            else:
                iterations = int(max_iterations / perms_count)  # +2 one for idx starts 1 and another for default profile
            f.write("# Profile Count = " + str(perms_count) + "\n")
            f.write("iterations=" + str(iterations) + "\n\n")
        f.write(perms)


shuffle(input_filename="apl.simc",
        output_filename=r"shuffled.simc",
        action_line_idx=1,
        set_iterations=True,
        max_iterations=320000000,
        profile_sets=200)