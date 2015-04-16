import nef

net=nef.Network('Test')
net.make('A',50,1)
net.make_input('input',{0: -1, 0.2: -0.5, 0.4:0, 0.6:0.5, 0.8:1.0})
net.connect('input','A')


nodes = net.network.getNodes()
print nodes[0]

log=net.log()
# log.add_spikes('input')
log.add_spikes('A')
net.run(1.0)