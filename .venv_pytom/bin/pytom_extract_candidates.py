#!/workspaces/fle3d-experiment1/.venv_pytom/bin/python3
import sys
from pytom_tm.entry_points import extract_candidates
if __name__ == '__main__':
    sys.argv[0] = sys.argv[0].removesuffix('.exe')
    sys.exit(extract_candidates())
