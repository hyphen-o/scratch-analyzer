import sys
sys.path.append('../')

from utils.env import env

CONTROL_BLOCKS = ["control_repeat", "control_forever", "control_if", "control_if_else", "control_repeat_until", "control_all_at_once", "control_while", "control_for_each"]
REPEAT_BLOCKS =  ["control_forever", "control_repeat"]
COORDINATE_FIELDS = ["STEPS", "DEGREES", "DIRECTION", "X", "Y", "DX", "DY"]
MOVE_FIELDS = ["DX", "DY"]
SET_FIELDS =  ["X", "Y"]
DEGREE_FIELDS = ["DEGREES", "DIRECTION"]
STEP_FIELDS =  ["STEPS"]
BOUND_FIELDS = ["motion_ifonedgebounce"]
WAIT_FIELDS = ["DURATION", "SECS"]

SCRATCH_API_BASE_URL = "https://api.scratch.mit.edu"
SCRATCH_BASE_URL = "https://projects.scratch.mit.edu"

TOKEN_PATH = sys.path[-1] + "/cert/token.json"
FORM_SCOPES = "https://www.googleapis.com/auth/forms.body"
FORM_DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"



