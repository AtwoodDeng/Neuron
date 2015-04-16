#######
# 拓扑结构数据表示
#######

输出文件
- [ModelName]_edge.csv
- [ModelName]_node.csv

[ModelName]_edge.csv:
   该文件代表了模型中各边的信息，每行代表一条边的信息，每个行由四个数组成，分别表示：
   ['source' , 'target' , 'weight' , 'delay']
   'source' => 源节点的global_id
   'target' => 目标节点的global_id
   'weight' => 边的权重
   'delay' => 传输延迟


[ModelName]_node.csv:
   该文件代表了模型中各节点的信息，每行代表一个节点的信息，每个行由若干个数组成，分别表示：
   ['global_id' , 'element_type', 'model' （, 'V_reset' , 'V_th' , 'E_L' , 'C_m'）]
   'global_id' => 节点的全局id
   'element_type' => 节点的类型（常见的为'neuron','simulator','recorder'）
   'model' => 节点使用的模型(如'spike_detecter,iaf_cond_exp')
   普通节点只包含上述三个信息，神经元节点（element_type == 'neuron')还包含生物学信息：
   'V_reset' => Reset Potential
   'V_th' => Threshold
   'V_m' => Membrane potential
   'E_L' => Resting potential
   'C_m' => Capacitance
   另外还有其他信息，详见
   http://www.nest-initiative.org/Variables_and_parameter_names

   