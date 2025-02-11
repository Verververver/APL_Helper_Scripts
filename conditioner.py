def condition(input_filename, output_filename, new_cond, operator, set_iterations=True):
    with open(input_filename) as file:
        apl = file.read()

    new_apl = ""
    perms_count = 1
    for idx, line in enumerate(apl.split("\n")):
        if "action" in line:
            if "if=" in line:
                prefix, conditions = line.split("if=", 1)
                temp_apl = apl.replace(line + "\n", prefix + "if=" + new_cond + operator + "(" + conditions + ")" + "\n#Added Above#\n", 1)
            else:
                temp_apl = apl.replace(line + "\n", line + ",if=" + new_cond + "\n#Added Above#\n", 1)
            for temp_line in temp_apl.split("\n"):
                if "action" in temp_line:
                    temp_apl = temp_apl.replace(temp_line, temp_line.replace("+=/", "="), 1)
                    break
            new_apl = new_apl + temp_apl.replace("mage=", "copy=").replace("copy=\"", "copy=\"CondL" + str(perms_count)) + "\n\n\n"
            perms_count += 1
            print(temp_apl)

    with open(output_filename, "w") as f:
        if set_iterations:
            if perms_count > 60:
                iterations = int(600000 / 60)
            else:
                iterations = int(600000 / perms_count)  # +2 one for idx starts 1 and another for default profile
            f.write("# Profile Count = " + str(perms_count) + "\n")
            f.write("iterations=" + str(iterations) + "\n\n")
        f.write(new_apl)

# Input file name, output filename, what condition you want to test at a specific line, what operator you want, display iterations
condition("apl.simc", "conditioned.simc", "buff.icy_veins.react", "&", set_iterations=True)
