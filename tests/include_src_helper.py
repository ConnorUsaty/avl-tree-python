""" So that I don't have to do relative pathing on my import, i.e. 'from ..src'. This is why CMake and C++ is better. """

import sys
from pathlib import Path

# add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
