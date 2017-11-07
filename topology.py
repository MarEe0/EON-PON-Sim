import sim, random

sim.DEBUG = True

# seed
sim.random.seed(13)

# environment
env = sim.simpy.Environment()

# writer
# packet_w = Writer("packet_", start="# id src init_time waited_time freq processed_time\n")

# default values
sim.tg_default_size = lambda x: random.randint(20, 40)
#sim.tg_default_size = lambda x: 50
sim.tg_default_dist = lambda x: 1
sim.ONU_consumption = lambda x: 15
sim.PN_consumption = lambda x: 25
sim.Ant_consumption = lambda x: 7
sim.DBA_IPACT_default_bandwidth = 600

# constants

# topology
antenas = 9
onus = 3
pns = 1
splts = 1
max_freqs = 10

matrix = [
    # Antenas -> ONUs
    [0,9,1000],
    [1,9,1000],
    [2,9,1000],
    [3,10,1000],
    [4,10,1000],
    [5,10,1000],
    [6,11,1000],
    [7,11,1000],
    [8,11,1000],
    # ONUs -> Splitter
    [9,13,1000],
    [10,13,1000],
    [11,13,1000],
    # Splitter -> PN
    [13,12,0]

]

# nodes
nodes = sim.create_topology(env, antenas, onus, pns, splts, matrix, max_freqs)

# rules
print("Begin.")

env.run(until=2)

print("End.")

# consumption
for n in nodes:
	if(isinstance(n, sim.Splitter)):
		continue
	else:
		print(str(n), "had consumption of:", n.consumption())