
def vstack(ma,mb):
	if len(ma) <= 0 :
		return
	if len(mb) <= 0 :
		return
	assert len(ma) == len(mb)

	# print 'vstack',len(ma),len(ma[0]),len(mb),len(mb[0])
	for i in range(len(ma)):
		ma[i].extend(mb[i])
	# print len(ma),len(ma[0])
	return ma

def hstack(ma,mb):
	if len(ma) <= 0 :
		ma = mb
		return
	elif len(mb) <= 0 :
		return
	assert len(ma[0]) == len(mb[0])

	# print 'hstack',len(ma),len(ma[0]),len(mb),len(mb[0])

	ma.extend(mb)

	# print len(ma),len(ma[0])

	return ma
"""
function:
    expend the matrix in sidesway
    e.g.:    A    =>     A0
                         0B
return:
   the new matrix
"""
def side_expend(ma,mb):
	# print 'in side ' , len(ma) , len(ma[0]) , len(mb) , len(mb[0])
	zero1 = zeros(len(mb),len(ma[0]))
	zero2 = zeros(len(ma),len(mb[0]))

	rA = vstack(ma,zero2)
	rB = vstack(zero1,mb)

	res = hstack(rA,rB)

	# print 'in side ', len(res) , len(res[0])
	return res

"""
function:
    get a zero matrix with n rows and m columns
return:
    the zero matrix
"""
def zeros(n,m):
	res = [[0.0 for col in range(m)] for row in range(n)]
	return res

"""
function:
    get a zero matrix with n rows and m columns
return:
    the zero matrix
"""
def ones(n,m):
	res = [[1.0 for col in range(m)] for row in range(n)]
	return res

def mu(ma,mb):
	# print 'in mu()',len(ma),len(ma[0]),len(mb),len(mb[0])

	assert len(ma) > 0 
	assert len(ma[0]) > 0 
	assert len(mb) > 0
	assert len(mb[0]) > 0
	assert len(ma[0]) == len(mb)


	res =  [[0.0 for col in range(len(mb[0]))] for row in range(len(ma))]


	for i in range(len(res)):
		for j in range(len(res[0])):
			for k in range(len(ma[0])):
				res[i][j]=res[i][j]+ma[i][k]*mb[k][j]
	return res

def transpose(m):
	assert len(m) > 0 
	assert len(m[0]) > 0 

	res =  [[0.0 for col in range(len(m))] for row in range(len(m[0]))]

	for i in range(len(res)):
		for j in range(len(res[0])):
			res[i][j] = m[j][i]
	return res

def to_mat(array):
	res =  [[0.0 for col in range(len(array[0]))] for row in range(len(array))]
	for i in range(len(res)):
		for j in range(len(res[0])):
			res[i][j] = array[i][j]
	return res	