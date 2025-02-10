def linetrimmer(input_filename, output_filename, set_iterations=False):
    with open(input_filename) as file:
        apl = file.read()

    new_apl = ""
    perms_count = 1
    for line in apl.split("\n"):
        if line and "action" in line:
            temp_apl = apl.replace(line, "# " + line + "\n" + "# Disabled line above")

            for temp_line in temp_apl.split("\n"):
                if "action" in temp_line and not "# action" in temp_line:
                    temp_apl = temp_apl.replace(temp_line, temp_line.replace("+=/", "="))
                    break
            new_apl = new_apl + temp_apl.replace("mage=", "copy=").replace("copy=\"", "copy=\"TrimL" + str(perms_count) + "|") + "\n\n"
            perms_count += 1

    with open(output_filename, "w") as f:
        if set_iterations:
            if perms_count > 60:
                iterations = int(600000 / 60)
            else:
                iterations = int(600000 / perms_count)  # +2 one for idx starts 1 and another for default profile
            f.write("# Profile Count = " + str(perms_count) + "\n")
            f.write("iterations=" + str(iterations) + "\n\n")
        f.write(new_apl)

linetrimmer("apl.simc", "lineTrimmed.simc", set_iterations=True)