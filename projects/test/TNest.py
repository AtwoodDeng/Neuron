import nest
import tool.spike as ts
import tool.topology as tt

nest.ResetKernel()

N_dc = 1
N_A = 1
N_B = 1
N_C = 1
T = 1000


drive= nest.Create('dc_generator' , N_dc)

neuronA = nest.Create('iaf_neuron' , N_A )
neuronB = nest.Create('iaf_neuron' , N_B )
neuronC = nest.Create('iaf_neuron' , N_C )

nest.Connect(drive, neuronA )
nest.ConvergentConnect(neuronA, neuronB , weight=[1000.00] , delay=[1.0] )
nest.ConvergentConnect(neuronB, neuronC , weight=[1000.00] , delay=[1.0] )

nest.SetStatus(drive , [{'amplitude':1000.}] )


tt.get_topology_seperate('TNEST','re')

SA = ts.SpikeAnalyzer()

nest.Simulate(T)

SA.CatchTrace('TNEST','re')