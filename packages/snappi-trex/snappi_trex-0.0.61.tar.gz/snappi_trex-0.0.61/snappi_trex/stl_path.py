import sys, os

try:
    from trex.stl.api import *
except:
    trex_path = './snappi_trex/trex-core/scripts/automation/trex_control_plane/interactive'
    sys.path.insert(0, os.path.abspath(trex_path))
