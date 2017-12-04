# Experiment 1 parameters:
# 100000 units of distance between nodes
# 5 seconds
# 4, 8, 12, 16, 20 RRHs
# Traffic generation: constant 250/s
# Channels: 50 of size 200

# Experiment 2 parameters:
# 100000 units of distance between nodes
# 5 seconds
# 4, 8, 12, 16, 20 RRHs
# Traffic generation: [250-2500]/ [0.5-1.5] s
# Channels: 50 of size 200

# Experiment 3 parameters:
# [5km-10km] distance between nodes
# 15 seconds
# 4, 8, 12, 16, 20 RRHs
# Traffic generation: [614Mb-24.3Gb]/ [1.0-5.0] s
# Channels: 16 of size 6250

import sys, os
sys.path.append("./../")

import matplotlib.pyplot as plt
import numpy as np
import random


# Reading command line arguments
if len(sys.argv) < 4:
    print("Usage: run_plot <topology> <support> <experiment>")
    print("\t<topology>: 'cf' or 'cran'")
    print("\t<support>: 'twdm' or 'eon'")
    print("\t<experiment>: 1, 2 or 3")

topology = sys.argv[1]
support = sys.argv[2]
experiment = int(sys.argv[3])

print("Running experiment {} for {}-{}".format(experiment, topology, support))

# Determining simulator
if support == "eon":
    import elastic as sim
elif support == "twdm":
    import sim
else:
    print("Invalid support: {}".format(support))

sim.DEBUG = False

max_frequencies = 0
# Determining parameters for experiment
if experiment == 1:
    sim.tg_default_size = lambda x: 250
    sim.tg_default_dist = lambda x: 1
    if support == "eon":
        sim.DBA_IPACT_default_bandwidth = 200
        max_frequencies = 50
    elif support == "twdm":
        sim.DBA_IPACT_default_bandwidth = 5000
        max_frequencies = 10
    ONU_bitRate_up = sim.DBA_IPACT_default_bandwidth * 8
    sim.ONU_consumption = lambda x: 15
    sim.PN_consumption = lambda x: 25
    sim.Ant_consumption = lambda x: 7

    max_onus = 20
    onu_step = 4

    run_time = 5

elif experiment == 2:
    sim.tg_default_size = lambda x: random.randint(250,2500)
    sim.tg_default_dist = lambda x: random.uniform(0.5,1.5)
    if support == "eon":
        sim.DBA_IPACT_default_bandwidth = 200
        max_frequencies = 50
    elif support == "twdm":
        sim.DBA_IPACT_default_bandwidth = 5000
        max_frequencies = 10
    ONU_bitRate_up = sim.DBA_IPACT_default_bandwidth * 8
    sim.ONU_consumption = lambda x: 15
    sim.PN_consumption = lambda x: 25
    sim.Ant_consumption = lambda x: 7

    max_onus = 20
    onu_step = 4

    run_time = 5

elif experiment == 3:
    sim.tg_default_size = lambda x: random.randint(614,24300)
    sim.tg_default_dist = lambda x: random.randrange(1.0, 5.0)
    if support == "eon":
        sim.DBA_IPACT_default_bandwidth = 6250
        max_frequencies = 16
    elif support == "twdm":
        sim.DBA_IPACT_default_bandwidth = 10000
        max_frequencies = 10
    ONU_bitRate_up = sim.DBA_IPACT_default_bandwidth * 10
    sim.ONU_consumption = lambda x: 15
    sim.PN_consumption = lambda x: 25
    sim.Ant_consumption = lambda x: 7

    max_onus = 20
    onu_step = 4

    run_time = 15    

else:
    print("Invalid experiment: {}".format(experiment))

def compute_mean_erlang(packets, total_time, total_channels, channel_size, delta=0.1):
    #print("got packets:")
    #for packet in packets:
    #    print("\t",packet)

    # Computes mean erlang from a list of packets
    erlangs = np.zeros(int(total_time/delta))
    for i in range(len(erlangs)):
        current_time = i*delta
        for packet in packets:
            if current_time >= packet["start"] and current_time <= packet["end"]:
                erlangs[i] += ((packet["size"]) / (channel_size))
    #for i in range(len(erlangs)):
    #    print("erlang at {}: {}".format(i*delta, erlangs[i]))
    return erlangs.mean(), erlangs.std()

plot1 = int(max_onus/onu_step) * [0]
plot2 = int(max_onus/onu_step) * [0]
plot3 = int(max_onus/onu_step) * [0]
plot4 = int(max_onus/onu_step) * [0]
plot4e= int(max_onus/onu_step) * [0]
plot5 = int(max_onus/onu_step) * [0]

seeds = [2, 3, 5, 7, 13, 17, 19, 23, 29, 31, 61, 67, 71, 73, 79, 83, 89, 97, 101, 107, 109, 113, 127, 131, 163, 167, 173, 179, 181, 317, 331, 337, 347, 349, 353]
#seeds = [1,2,3,4]
#seeds=[1]

def run_for_seed(s):
    global max_frequencies
    # seed
    sim.random.seed(s)
    lost_req = []
    count_req = []
    duplicated_req = []
    power_consumption = []

    for f in range(onu_step,max_onus+1, onu_step):
        print("Using seed {", s, "} on ONU {", f, "}")
        # override suffix writer
        sim.packet_w = sim.Writer("# id src init_time waited_time freq size processed_time\n")

        # environment
        env = sim.simpy.Environment()

        # topology
        if topology == "cf":
            antenas = f
            onus = f 
            pns = f+1
            splts = 1

            matrix = []
            for z in range(f):
                matrix.append([z, f+z, 100000])
                matrix.append([f+z, 2*f+z, 10])
                matrix.append([2*f+z, 3*f+1, 100000])
            matrix.append([3*f+1, 3*f, 100000])
        elif topology == "cran":
            antenas = f
            onus = f 
            pns = 1
            splts = 1

            matrix = []
            for z in range(f):
                matrix.append([z, f+z, 100000])
                matrix.append([f+z, 2*f+1, 100000])
            matrix.append([2*f+1, 2*f, 100000])
        else:
            print("Invalid topology: {}".format(topology))

        nodes = sim.create_topology(env, antenas, onus, pns, splts, matrix, max_frequencies)

        if topology == "cf":
            # Shut down all local PNs
            for node in nodes[2*f:3*f]:
                node.end()

        # start
        print("\tBegin")
        env.run(until=run_time)
        print("\tEnd")

        total_lost = 0
        total_duplicated = 0
        total_received = 0
        # collecting results
        if support == "eon":
            total_lost = sim.total_lost
            total_duplicated = sim.total_duplicated
            total_received = sim.total_requests
        elif support == "twdm":
            for vm in nodes[len(nodes)-2].DU[0].vms:
                if(type(vm) is sim.DBA_IPACT):
                    total_lost += vm.discarded_requests
                    total_duplicated += vm.duplicated_requests
                    total_received += vm.received_requests


        lost_req.append(total_lost)
        duplicated_req.append(total_duplicated)
        count_req.append(total_received)

        total_consumption = 0
        for vm in nodes:
            if(type(vm) is sim.Splitter):
                continue
            else:
                total_consumption += vm.consumption()
        power_consumption.append(total_consumption)

        sim.packet_w.close()

    # read files, generate graph
    mean_waited_array=[0]
    mean_erlangs = [0]
    std_erlangs = [0]

    for f in sim.output_files:
        file = open(f, "r")
        total = 0
        lines = 0
        packets = []
        for line in file:
            line_sep = line.split(' ')
            if(line_sep[0][0] == "#"):
                continue
            total += float(line_sep[3])
            packets.append({"start": float(line_sep[2]), "size": float(line_sep[5]), "end": float(line_sep[6])})
            lines += 1
        file.close()

        if lines == 0:
            lines = 1
        total = total / lines
        mean_waited_array.append(total)

        mean_erlang, std_erlang = compute_mean_erlang(packets, total_time=run_time, total_channels=max_frequencies, channel_size=sim.DBA_IPACT_default_bandwidth)
        mean_erlangs.append(mean_erlang)
        std_erlangs.append(std_erlang)

    for i in range(len(lost_req)):
        #plot1[i] += lost_req[i] / len(seeds)
        #plot2[i] += (lost_req[i]/(count_req[i] if count_req[i] != 0 else 1)) / len(seeds)
        #plot3[i] += mean_waited_array[i] / len(seeds)
        #plot4[i] += mean_erlangs[i] / len(seeds)
        #plot4e[i]+= std_erlangs[i] / len(seeds)
        #plot5[i] += power_consumption[i] / len(seeds)
        return lost_req, count_req, mean_waited_array, mean_erlangs, std_erlangs, power_consumption

from multiprocessing import Pool

with Pool(processes = 16) as pool:
    results = pool.map(run_for_seed, seeds)

for seed_result in results:
    lost_req, count_req, mean_waited_array, mean_erlangs, std_erlangs, power_consumption = seed_result
    for i in range(len(lost_req)):
        plot1[i] += lost_req[i] / len(seeds)
        plot2[i] += (lost_req[i]/(count_req[i] if count_req[i] != 0 else 1)) / len(seeds)
        plot3[i] += mean_waited_array[i] / len(seeds)
        plot4[i] += mean_erlangs[i] / len(seeds)
        plot4e[i]+= std_erlangs[i] / len(seeds)
        plot5[i] += power_consumption[i] / len(seeds)

results_file = open(os.path.join("results", "{}_{}{}.txt".format(topology, support, experiment)) ,"w")
results_file.write("n_ONUS\tLost_req\tLost_pct\tAvg_wait\terlang\terlang_std\tpower\n")
for n_onu, lost_req, lost_pct, avg_wait, erlang, erlang_std, power in zip(range(onu_step,max_onus+1, onu_step), plot1, plot2, plot3, plot4, plot4e, plot5):
    results_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(n_onu, lost_req, lost_pct, avg_wait, erlang, erlang_std, power))

results_file.close()

plt.plot(range(onu_step,max_onus+1, onu_step), plot1, 'g.-')
plt.ylabel('Number of Requests Lost')
plt.xlabel("Number of ONUs")
plt.savefig('plots/{}_{}{}_lost_req.png'.format(topology, support, experiment), bbox_inches='tight')
plt.clf()

plt.plot(range(onu_step,max_onus+1, onu_step), plot2, 'b.-')
plt.ylabel('Percentage of Requests Lost')
plt.xlabel("Number of ONUs")
plt.savefig('plots/{}_{}{}_lost_pct.png'.format(topology, support, experiment), bbox_inches='tight')
plt.clf()

plt.plot(range(onu_step,max_onus+1, onu_step), plot3, 'r.-')
plt.ylabel('Average waited time (s)')
plt.xlabel("Number of ONUs")
plt.savefig('plots/{}_{}{}_avg_wait.png'.format(topology, support, experiment), bbox_inches='tight')
plt.clf()

plt.errorbar(range(onu_step,max_onus+1, onu_step), plot4, plot4e, None, 'c.-')
plt.ylabel('Mean bandwidth usage (erlangs)')
plt.xlabel("Number of ONUs")
plt.savefig('plots/{}_{}{}_erlang.png'.format(topology, support, experiment), bbox_inches='tight')
plt.clf()

plt.plot(range(onu_step,max_onus+1, onu_step), plot5, 'b.-')
plt.ylabel('Total power consumption (W)')
plt.xlabel("Number of ONUs")
plt.savefig('plots/{}_{}{}_power.png'.format(topology, support, experiment), bbox_inches='tight')
plt.clf()


print("Finished")
