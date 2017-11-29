import elastic as sim, random

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

# consumption
for n in nodes:
	if(isinstance(n, sim.Splitter)):
		continue
	else:
		print(str(n), "had consumption of:", n.consumption())