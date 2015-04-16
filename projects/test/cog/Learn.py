import os.path
import sys
import nef
# I make a symlink `trevor` in the nengo directory, pointing to scriptdir
sys.path.append('trevor/nengo')  
from Builder import Builder
from LearnBuilder import LearnBuilder

scriptdir = os.path.expanduser("~/nengo-latest/trevor/nengo")
logdir = os.path.expanduser("~/Programming/cogsci2013/results/")

if False:
    builder = LearnBuilder('channel')
    builder.view(True)
else:
    # name = sys.argv[1]
    # testtype = sys.argv[2]
    name = 'channel'
    testtype = 'one'
    params = Builder.parse_params(sys.argv[3:])
    if testtype == 'full':
        logdir = logdir + "functions-test"
    elif testtype == 'one':
        logdir = logdir + "functions-optimize"
    builder = LearnBuilder(name, testtype, **params)
    builder.make().add_to_nengo()
    # builder.run(name, logdir)
