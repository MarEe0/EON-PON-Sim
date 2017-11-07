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
sim.tg_default_dist = lambda x: 0.1
sim.ONU_consumption = lambda x: 15
sim.PN_consumption = lambda x: 25
sim.Ant_consumption = lambda x: 7
sim.DBA_IPACT_default_bandwidth = 60

# constants

# topology
antenas = 2
onus = 1
pns = 1
splts = 1
max_freqs = 10

matrix = [
    # Antenas -> ONUs
    [0,2,10000000],
    [1,2,10000000],
    # ONUs -> Splitter
    [2,4,10000000],
    # Splitter -> PN
    [4,3,0]

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