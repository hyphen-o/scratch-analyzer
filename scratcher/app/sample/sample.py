import sys
sys.path.append('../../')

from prjman import ProjectManager

id = 00000000
PM = ProjectManager(id)
print(PM.get_blocks())