def condition(input_filename, output_filename, new_condition, operator, set_iterations=True, max_iterations=600000, profile_sets=60):
    with open(input_filename) as file:
        apl = file.read()

    new_apl = ""
    perms_count = 1
    for idx, line in enumerate(apl.split("\n")):
        if "action" in line:
            if "if=" in line:
                prefix, conditions = line.split("if=", 1)
                temp_apl = apl.replace(line + "\n", prefix + "if=" + new_condition + operator + "(" + conditions + ")" + "\n#Added Above#\n", 1)
            else:
                temp_apl = apl.replace(line + "\n", line + ",if=" + new_condition + "\n#Added Above#\n", 1)
            for temp_line in temp_apl.split("\n"):
                if "action" in temp_line:
                    temp_apl = temp_apl.replace(temp_line, temp_line.replace("+=/", "="), 1)
                    break
            new_apl = new_apl + temp_apl.replace("mage=", "copy=").replace("copy=\"", "copy=\"CondL" + str(perms_count)) + "\n\n\n"
            perms_count += 1
            print(temp_apl)

    with open(output_filename, "w") as f:
        if set_iterations:
            if perms_count > profile_sets:
                iterations = int(max_iterations / profile_sets)
            else:
                iterations = int(max_iterations / perms_count)  # +2 one for idx starts 1 and another for default profile
            f.write("# Profile Count = " + str(perms_count) + "\n")
            f.write("# iterations=" + str(iterations) + "\n\n")
        f.write(new_apl)


condition(input_filename="apl.simc",
          output_filename="conditioned.simc",
          new_condition="buff.icy_veins.react",
          operator="&",
          set_iterations=True,
          max_iterations=320000000,
          profile_sets=200)