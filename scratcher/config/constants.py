import sys
sys.path.append('../')

from utils.env import env

REPEAT_TIMES = 30

#ブロック，フィールドの定義
EVENT_BLOCKS = ["event_whenflagclicked", "event_whenkeypressed", "event_whenthisspriteclicked", "event_whenbackdropswitchesto", "event_whengreaterthan", "event_whenbroadcastreceived", "event_broadcast", "event_broadcastandwait"]
CONTROL_BLOCKS = ["control_repeat", "control_forever", "control_if", "control_if_else", "control_repeat_until", "control_all_at_once", "control_while", "control_for_each"]
IF_BLOCKS = ["control_if", "control_if_else"]
REPEAT_BLOCKS =  ["control_forever", "control_repeat"]
COORDINATE_FIELDS = ["STEPS", "X", "Y", "DX", "DY", "DURATION", "SECS"]
MOVE_FIELDS = ["DX", "DY"]
SET_FIELDS =  ["X", "Y"]
DEGREE_FIELDS = ["DEGREES", "DIRECTION"]
STEP_FIELDS =  ["STEPS"]
BOUND_FIELDS = ["motion_ifonedgebounce"]
WAIT_FIELDS = ["DURATION", "SECS"]
REPEAT_BLOCK = "control_repeat"
FOREVER_BLOCK = "control_forever"
EVENT_KEY_BLOCK = "event_whenkeypressed"

#パス
COORDINATE_PATH = sys.path[-1] + "/out/coorfinate_final/"
COORDINATE_LIST_PATH = sys.path[-1] + "out/coordinate_looped"
TOKEN_PATH = sys.path[-1] + "/cert/token.json"


#URL，トークン
SCRATCH_API_BASE_URL = "https://api.scratch.mit.edu"
SCRATCH_BASE_URL = "https://projects.scratch.mit.edu"

FORM_SCOPES = "https://www.googleapis.com/auth/forms.body"
FORM_DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"



