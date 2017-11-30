import elastic as sim, random, numpy as np

sim.DEBUG = True

# seed
sim.random.seed(13)

# environment
env = sim.simpy.Environment()

# writer
# packet_w = Writer("packet_", start="# id src init_time waited_time freq processed_time\n")

# default values
sim.tg_default_size = lambda x: random.randint(40, 80)
#sim.tg_default_size = lambda x: 50
sim.tg_default_dist = lambda x: random.uniform(0.9, 1.1)
sim.ONU_consumption = lambda x: 15
sim.PN_consumption = lambda x: 25
sim.Ant_consumption = lambda x: 7
sim.slot_default_bandwidth = 60

# constants

# topology
antenas = 1
onus = 1
pns = 1
splts = 1
max_freqs = 16

matrix = []
for z in range(antenas):
    matrix.append([z, antenas+z, 1000])
    matrix.append([antenas+z, 2*antenas+1, 1000])
matrix.append([2*antenas+1, 2*antenas, 1000])


sim.packet_w = sim.Writer("# id src init_time waited_time freq processed_time\n")

# nodes
nodes = sim.create_topology(env, antenas, onus, pns, splts, matrix, max_freqs)

# rules
print("Begin.")

env.run(until=3)

print("End.")
sim.packet_w.close()

# bandwidth
total_req = sim.total_requests
lost_req = sim.total_lost
duplicated_req = sim.total_duplicated
print("Requests lost: {} ({:.2f}%). Requests duplicated: {} ({:.2f}%)".format(lost_req, (lost_req*100/total_req), duplicated_req, (duplicated_req*100/total_req)))

file = open(sim.output_files[0], "r")
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

mean_erlang, std_erlang = compute_mean_erlang(packets, total_time=3, total_channels=max_freqs, channel_size=sim.slot_default_bandwidth)

print("Mean wait: {:.4f}. Mean erlang: {:.2f} +/- {:.2f}".format(total, mean_erlang, std_erlang))

# consumption
for n in nodes:
	if(isinstance(n, sim.Splitter)):
		continue
	else:
		print(str(n), "had consumption of:", n.consumption())