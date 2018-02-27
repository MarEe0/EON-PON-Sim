onus = ['4','8','12','16','20']
experiments = [3,5,10]
supports = ["eon","twdm"]
results = [(":.5f", 3), (":.2f", 4), (":.4f", 2)]

for onu in onus:
    print("  \multirow{{6}}{{*}}{{{}}} & ".format(onu), end="")
    for experiment in experiments:
        if experiment != 3:
            print("  & ", end="")
        print("\multirow{{2}}{{*}}{{{}}} & ".format(experiment), end="")
        for support in supports:
            if support == "twdm": print("  & & ", end="")
            else: print("   ", end="")
            print("{} & ".format(support.upper()), end="")
            for result in results:
                file = open("cran_{}{}.txt".format(support, experiment))
                for line in file:
                    if line.split('\t')[0] == onu:
                        if result[1] == 3:
                            print("{:.5f} & ".format(float(line.split('\t')[result[1]])), end="")
                        if result[1] == 4:
                            print("{:.2f} & ".format(float(line.split('\t')[result[1]])), end="")
                        if result[1] == 2:
                            print("{:.4f} ".format(float(line.split('\t')[result[1]])), end="")
            print("\\\\")
        print("  \cline{2-6}")
    print(" \hline")
