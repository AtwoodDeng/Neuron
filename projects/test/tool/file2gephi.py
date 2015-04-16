import sys

SEP_WORD = ','
RETURN = '\n'

"""
function:
  transform the node file to a gephi node file(.csv)
parament:
  node_file: the file of node
"""
def node2gephi(node_file,out_file=''):
	print '===== begin node 2 gephi ====='
	__MC_DICT__ = dict()
	fin = open(node_file,'r')
	if out_file == '':
		out_file = node_file[0:len(node_file)-4]+'_gephi.csv'

	fout = open(out_file,'w+')
	fout.write('Id,Label,Modularity Class'+RETURN)

	for in_line in fin.readlines():
		words = in_line.split(',')
		_id = words[0]
		label = ''
		MC = ''

		id_class = ''
		if words[1] == 'neuron':
			id_class = words[10]
			label = words[10].strip('\n').strip('\r')+_id

		if words[1] == 'simulator':
			id_class = words[4]
			label = words[4].strip('\n').strip('\r')

		if not(id_class =='' ):
			if not( id_class in __MC_DICT__.keys()):
				__MC_DICT__[id_class]=len(__MC_DICT__)
			MC = str(__MC_DICT__[id_class])

		fout.write(_id+SEP_WORD+label+SEP_WORD+MC+RETURN)

	fin.close()
	fout.close()
	print '===== end node 2 gephi ====='

"""
function:
  transform the edge file to a gephi edge file(.csv)
parament:
  node_file: the file of edge
"""
def edge2gephi(edge_file,out_file=''):
	fin = open(edge_file,'r')
	if out_file == '':
		out_file = edge_file[0:len(edge_file)-4]+'_gephi.csv'

	fout = open(out_file,'w+')
	fout.write('Source,Target,Type,Weight'+RETURN)

	for in_line in fin.readlines():
		words = in_line.split(',')
		if len(words) <= 0:
			continue
		source = words[0]
		target = words[1]
		_type = 'Directed'
		weight = words[2]

		fout.write(source+SEP_WORD+target+SEP_WORD+_type+SEP_WORD+weight+RETURN)

	fin.close()
	fout.close()

if __name__ =='__main__':
	node2gephi(sys.argv[1])
	edge2gephi(sys.argv[2])