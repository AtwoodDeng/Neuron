# Network NeocorticalMicrocircuitry Start
net_NeocorticalMicrocircuitry = nef.Network('NeocorticalMicrocircuitry')

# NeocorticalMicrocircuitry - Nodes
net_NeocorticalMicrocircuitry.make('D', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('E', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=-1.00)
net_NeocorticalMicrocircuitry.make('F', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('G', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=-1.00)
net_NeocorticalMicrocircuitry.make('A', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('B', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=-1.00)
net_NeocorticalMicrocircuitry.make('C', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('L', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=-1.00)
net_NeocorticalMicrocircuitry.make('M', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('N', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('O', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('H', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)
net_NeocorticalMicrocircuitry.make('I', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=-1.00)

net_NeocorticalMicrocircuitry.make_input('Input6')

net_NeocorticalMicrocircuitry.make_input('Input4')
net_NeocorticalMicrocircuitry.make('Q', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=1.00)

net_NeocorticalMicrocircuitry.make_input('Input5')
net_NeocorticalMicrocircuitry.make('P', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=-1.00)

net_NeocorticalMicrocircuitry.make_input('Input2')
net_NeocorticalMicrocircuitry.make('S', 1, 1, tau_rc=0.020, tau_ref=0.002, max_rate=(100.0, 200.0), intercept=(-1.0, 1.0), radius=-1.00)

net_NeocorticalMicrocircuitry.make_input('Input3')

net_NeocorticalMicrocircuitry.make_input('Input1')

# NeocorticalMicrocircuitry - Templates

# NeocorticalMicrocircuitry - Projections
transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('N', 'M', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('B', 'A', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('H', 'F', transform=transform)

transform = [[0.1]]
net_NeocorticalMicrocircuitry.connect('Input2', 'A', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('O', 'L', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('S', 'H', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('E', 'A', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('C', 'H', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('S', 'O', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('A', 'Q', transform=transform)

transform = [[0.1]]
net_NeocorticalMicrocircuitry.connect('Input1', 'A', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('D', 'H', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('H', 'I', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('A', 'E', transform=transform)

transform = [[0.1]]
net_NeocorticalMicrocircuitry.connect('Input2', 'B', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('B', 'C', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('F', 'Q', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('G', 'H', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('E', 'F', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('H', 'O', transform=transform)

transform = [[0.1]]
net_NeocorticalMicrocircuitry.connect('Input6', 'D', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('H', 'N', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('P', 'H', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('L', 'O', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('H', 'E', transform=transform)

transform = [[0.1]]
net_NeocorticalMicrocircuitry.connect('Input4', 'C', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('I', 'H', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('M', 'P', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('G', 'F', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('F', 'O', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('E', 'Q', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('A', 'F', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('P', 'M', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('F', 'S', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('S', 'Q', transform=transform)

transform = [[0.1]]
net_NeocorticalMicrocircuitry.connect('Input3', 'F', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('D', 'G', transform=transform)

transform = [[1.0]]
net_NeocorticalMicrocircuitry.connect('H', 'M', transform=transform)

transform = [[0.1]]
net_NeocorticalMicrocircuitry.connect('Input5', 'H', transform=transform)


# Network NeocorticalMicrocircuitry End

net_NeocorticalMicrocircuitry.add_to_nengo()
