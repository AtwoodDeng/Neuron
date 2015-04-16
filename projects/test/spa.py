import nengo
import nengo.spa as spa

dimensions = 32
model = spa.SPA()
with model:
     model.state1 = spa.Buffer(dimensions=dimensions)                            
     model.state2 = spa.Buffer(dimensions=dimensions)                            
     model.output = spa.Buffer(dimensions=dimensions)                            
                                                                                 
     model.bg = spa.BasalGanglia(spa.Actions('0.5 --> output=state1*state2'))    
     model.thal = spa.Thalamus(model.bg)           