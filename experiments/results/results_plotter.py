import numpy as np
import matplotlib.pyplot as plt
import itertools

experiments = [3,5,10]
supports = ["eon", "twdm", "both"]
results = [("Average wait", 3), ("Mean bandwidth usage", 4), ("Percentage of requests blocked", 2)]
marker = itertools.cycle(('v', '^', 's', 'o', '*', 'D')) 

# Plotting average wait for TWDM
for experiment in experiments:
    file = "cran_twdm{}.txt".format(experiment)
    n_onus = []
    wait = []
    first_line = True
    for line in open(file):
        if first_line:
            first_line = False
            continue
        n_onus.append(int(line.split('\t')[0]))
        wait.append(float(line.split('\t')[3]))

    plt.plot(n_onus, wait, marker=next(marker), label="TWDM-{}".format(experiment))

plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Average wait for TWDM")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Average wait (s)")
plt.savefig("Average wait for TWDM.png")
plt.clf()

# Plotting average wait for EON
for experiment in experiments:
    file = "cran_eon{}.txt".format(experiment)
    n_onus = []
    wait = []
    first_line = True
    for line in open(file):
        if first_line:
            first_line = False
            continue
        n_onus.append(int(line.split('\t')[0]))
        wait.append(float(line.split('\t')[3]))

    plt.plot(n_onus, wait, marker=next(marker), label="EON-{}".format(experiment))

plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Average wait for EON")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Average wait (s)")
plt.savefig("Average wait for EON.png")
plt.clf()

# Plotting average wait for both
for support in ["eon", "twdm"]:
    for experiment in experiments:
        file = "cran_{}{}.txt".format(support, experiment)
        n_onus = []
        wait = []
        first_line = True
        for line in open(file):
            if first_line:
                first_line = False
                continue
            n_onus.append(int(line.split('\t')[0]))
            wait.append(float(line.split('\t')[3]))

        plt.plot(n_onus, wait, marker=next(marker), label="{}-{}".format(support.upper(), experiment))

plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Average wait")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Average wait (s)")
plt.savefig("Average wait.png")
plt.clf()

#--------------------------------------------------------
# Plotting Mean bandwidth usage for TWDM
for experiment in experiments:
    file = "cran_twdm{}.txt".format(experiment)
    n_onus = []
    wait = []
    first_line = True
    for line in open(file):
        if first_line:
            first_line = False
            continue
        n_onus.append(int(line.split('\t')[0]))
        wait.append(float(line.split('\t')[4]))

    plt.plot(n_onus, wait, marker=next(marker), label="TWDM-{}".format(experiment))

#plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Mean bandwidth usage for TWDM")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Mean bandwidth usage (erlang)")
plt.savefig("Mean bandwidth usage for TWDM.png")
plt.clf()

# Plotting Mean bandwidth usage for EON
for experiment in experiments:
    file = "cran_eon{}.txt".format(experiment)
    n_onus = []
    wait = []
    first_line = True
    for line in open(file):
        if first_line:
            first_line = False
            continue
        n_onus.append(int(line.split('\t')[0]))
        wait.append(float(line.split('\t')[4]))

    plt.plot(n_onus, wait, marker=next(marker), label="EON-{}".format(experiment))

#plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Mean bandwidth usage for EON")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Mean bandwidth usage (erlang)")
plt.savefig("Mean bandwidth usage for EON.png")
plt.clf()

# Plotting Mean bandwidth usage for both
for support in ["eon", "twdm"]:
    for experiment in experiments:
        file = "cran_{}{}.txt".format(support, experiment)
        n_onus = []
        wait = []
        first_line = True
        for line in open(file):
            if first_line:
                first_line = False
                continue
            n_onus.append(int(line.split('\t')[0]))
            wait.append(float(line.split('\t')[4]))

        plt.plot(n_onus, wait, marker=next(marker), label="{}-{}".format(support.upper(), experiment))

#plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Mean bandwidth usage")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Mean bandwidth usage (erlang)")
plt.savefig("Mean bandwidth usage.png")
plt.clf()


#--------------------------------------------------------
# Plotting Percentage of Lost Packets for TWDM
for experiment in experiments:
    file = "cran_twdm{}.txt".format(experiment)
    n_onus = []
    wait = []
    first_line = True
    for line in open(file):
        if first_line:
            first_line = False
            continue
        n_onus.append(int(line.split('\t')[0]))
        wait.append(float(line.split('\t')[2]))

    plt.plot(n_onus, wait, marker=next(marker), label="TWDM-{}".format(experiment))

#plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Percentage of Lost Packets for TWDM")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Lost packets (%)")
plt.savefig("Percentage of Lost Packets for TWDM.png")
plt.clf()

# Plotting Percentage of Lost Packets for EON
for experiment in experiments:
    file = "cran_eon{}.txt".format(experiment)
    n_onus = []
    wait = []
    first_line = True
    for line in open(file):
        if first_line:
            first_line = False
            continue
        n_onus.append(int(line.split('\t')[0]))
        wait.append(float(line.split('\t')[2]))

    plt.plot(n_onus, wait, marker=next(marker), label="EON-{}".format(experiment))

#plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Percentage of Lost Packets for EON")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Lost packets (%)")
plt.savefig("Percentage of Lost Packets for EON.png")
plt.clf()

# Plotting Percentage of Lost Packets for both
for support in ["eon", "twdm"]:
    for experiment in experiments:
        file = "cran_{}{}.txt".format(support, experiment)
        n_onus = []
        wait = []
        first_line = True
        for line in open(file):
            if first_line:
                first_line = False
                continue
            n_onus.append(int(line.split('\t')[0]))
            wait.append(float(line.split('\t')[2]))

        plt.plot(n_onus, wait, marker=next(marker), label="{}-{}".format(support.upper(), experiment))

#plt.yscale('log')
plt.grid(True, "major")
plt.grid(True, "minor", linestyle='dotted')
plt.title("Percentage of Lost Packets")
plt.legend()
plt.xlabel("Number of ONUs")
plt.xticks(n_onus)
plt.ylabel("Lost packets (%)")
plt.savefig("Percentage of Lost Packets.png")
plt.clf()