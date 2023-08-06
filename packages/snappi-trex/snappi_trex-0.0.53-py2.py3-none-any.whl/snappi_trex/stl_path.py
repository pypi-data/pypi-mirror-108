import sys, os

cur_dir = os.path.dirname(__file__)



trex_path = './trex-core/scripts/automation/trex_control_plane/interactive'
sys.path.insert(0, os.path.abspath(trex_path))
print(os.path.abspath(trex_path))
