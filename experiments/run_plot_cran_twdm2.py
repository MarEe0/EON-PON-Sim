# Experiment 2 parameters:
# C-RAN, 100000 units of distance between nodes
# 5 seconds
# 4, 8, 12, 16, 20 RRHs
# Traffic generation: [250-2500]/ [0.5-1.5] s
# Channels: 10 of size 5000
import sys, os
sys.path.append("./../")

import sim
import matplotlib.pyplot as plt
import numpy as np
import random

sim.DEBUG = False

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

# seed
sim.random.seed(13)

# default values
sim.tg_default_size = lambda x: random.randint(250,2500)
sim.tg_default_dist = lambda x: random.uniform(0.5,1.5)
sim.DBA_IPACT_default_bandwidth = 5000
ONU_bitRate_up = sim.DBA_IPACT_default_bandwidth * 8
sim.ONU_consumption = lambda x: 15
sim.PN_consumption = lambda x: 25
sim.Ant_consumption = lambda x: 7

max_onus = 20
onu_step = 4

run_time = 5

plot1 = int(max_onus/onu_step) * [0]
plot2 = int(max_onus/onu_step) * [0]
plot3 = int(max_onus/onu_step) * [0]
plot4 = int(max_onus/onu_step) * [0]
plot4e= int(max_onus/onu_step) * [0]
plot5 = int(max_onus/onu_step) * [0]

seeds = [2, 3, 5, 7, 13, 17, 19, 23, 29, 31, 61, 67, 71, 73, 79, 83, 89, 97, 101, 107, 109, 113, 127, 131, 163, 167, 173, 179, 181, 317, 331, 337, 347, 349, 353]
#seeds = [1,2,3,4]
#seeds=[1]

for s in seeds:
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
        antenas = f
        onus = f 
        pns = 1
        splts = 1
        max_frequencies = 10

        matrix = []
        for z in range(f):
            matrix.append([z, f+z, 100000])
            matrix.append([f+z, 2*f+1, 100000])
        matrix.append([2*f+1, 2*f, 100000])

        nodes = sim.create_topology(env, antenas, onus, pns, splts, matrix, max_frequencies)

        # start
        print("\tBegin")
        env.run(until=run_time)
        print("\tEnd")

        total_lost = 0
        total_duplicated = 0
        total_received = 0
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

        total = total / lines
        mean_waited_array.append(total)

        mean_erlang, std_erlang = compute_mean_erlang(packets, total_time=run_time, total_channels=max_frequencies, channel_size=sim.DBA_IPACT_default_bandwidth)
        mean_erlangs.append(mean_erlang)
        std_erlangs.append(std_erlang)

    for i in range(len(lost_req)):
        plot1[i] += lost_req[i] / len(seeds)
        plot2[i] += (lost_req[i]/(count_req[i] if count_req[i] != 0 else 1)) / len(seeds)
        plot3[i] += mean_waited_array[i] / len(seeds)
        plot4[i] += mean_erlangs[i] / len(seeds)
        plot4e[i]+= std_erlangs[i] / len(seeds)
        plot5[i] += power_consumption[i] / len(seeds)

results_file = open(os.path.join("results", "cran_twdm2.txt") ,"w")
results_file.write("n_ONUS\tLost_req\tLost_pct\tAvg_wait\terlang\terlang_std\tpower\n")
for n_onu, lost_req, lost_pct, avg_wait, erlang, erlang_std, power in zip(range(onu_step,max_onus+1, onu_step), plot1, plot2, plot3, plot4, plot4e, plot5):
    results_file.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(n_onu, lost_req, lost_pct, avg_wait, erlang, erlang_std, power))

results_file.close()

plt.plot(range(onu_step,max_onus+1, onu_step), plot1, 'g.-')
plt.ylabel('Number of Requests Lost')
plt.xlabel("Number of ONUs")
plt.savefig('plots/cran_twdm2_lost_req.png', bbox_inches='tight')
plt.clf()

plt.plot(range(onu_step,max_onus+1, onu_step), plot2, 'b.-')
plt.ylabel('Percentage of Requests Lost')
plt.xlabel("Number of ONUs")
plt.savefig('plots/cran_twdm2_lost_pct.png', bbox_inches='tight')
plt.clf()

plt.plot(range(onu_step,max_onus+1, onu_step), plot3, 'r.-')
plt.ylabel('Average waited time (s)')
plt.xlabel("Number of ONUs")
plt.savefig('plots/cran_twdm2_avg_wait.png', bbox_inches='tight')
plt.clf()

plt.errorbar(range(onu_step,max_onus+1, onu_step), plot4, plot4e, None, 'c.-')
plt.ylabel('Mean bandwidth usage (erlangs)')
plt.xlabel("Number of ONUs")
plt.savefig('plots/cran_twdm2_erlang.png', bbox_inches='tight')
plt.clf()

plt.plot(range(onu_step,max_onus+1, onu_step), plot5, 'b.-')
plt.ylabel('Total power consumption (mWh)')
plt.xlabel("Number of ONUs")
plt.savefig('plots/cran_twdm2_power.png', bbox_inches='tight')
plt.clf()

print("Finished")
