import sys, os

try:
    from trex.stl.api import *
except:
    cur_dir = os.path.dirname(__file__)
    trex_path = cur_dir + '/trex-core/scripts/automation/trex_control_plane/interactive'
    sys.path.insert(0, os.path.abspath(trex_path))