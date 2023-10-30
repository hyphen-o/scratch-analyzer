import sys

sys.path.append("../")

from utils import DfManager, single_to_double
from config import constants


class Sorter:
    __IF_BLOCKS = constants.IF_BLOCKS
    __R_BLOCKS = constants.REPEAT_BLOCKS
    __E_BLOCKS = constants.EVENT_BLOCKS
    __VAR_BLOCKS = constants.VARIABLE_BLOCKS
    __PRO_CALL_BLOCKS = constants.PROCEDURES_CALL

    def __init__(self, project):
        self.__dfM = DfManager(
            ["BlockName", "Key", "Field", "node_id", "parent_id", "hash"]
        )
        self.__blocks = project["targets"][1]["blocks"]
        self.__sprite = project["targets"][1]
        self.__variables = self.__get_variables(project["monitors"])
        self.__node_id = 0

    def to_csv(self, dir_path):
        self.__dfM.to_csv(dir_path)

    def sort_blocks(self):
        self.__dfM.add_row(
            [
                self.__sprite["direction"],
                self.__sprite["x"],
                self.__sprite["y"],
                None,
                None,
                None,
            ]
        )
        for block_hash, block in self.__blocks.items():
            if "event" in block["opcode"]:
                self.__write_blocks(block_hash)

        return self.__dfM.get_df()

    def __get_variables(self, monitors):
        variables = {}
        for monitor in monitors:
            if monitor["opcode"] == "data_variable":
                variables[monitor["id"]] = "0"
        return variables

    def __get_parent_index(self, block):
        if block["parent"]:
            df = self.__dfM.get_df()
            return df[df["hash"] == block["parent"]].index.to_list()[0]
        else:
            return 0

    def __categorize_blocks(self, block_name):
        try:
            if block_name in self.__E_BLOCKS:
                return "EVENT"
            elif block_name in self.__IF_BLOCKS:
                return "IF"
            elif block_name in self.__R_BLOCKS:
                return "REPEAT"
            elif block_name in self.__VAR_BLOCKS:
                return "VARIABLE"
            elif block_name in self.__PRO_CALL_BLOCKS:
                return "CALL"
            else:
                return "NORMAL"
        except Exception as e:
            print(e)

    def __has_forever_block(self, block_hash):
        while True:
            if self.__blocks[block_hash]["opcode"] == constants.FOREVER_BLOCK:
                return True
            if self.__blocks[block_hash]["next"]:
                block_hash = self.__blocks[block_hash]["next"]
                continue
            else:
                return False

    def __get_variable_value(self, input):
        if len(input) == 3:
            if input[1][2] in self.__variables:
                return self.__variables[input[1][2]]
            else:
                return "0"
        else:
            return input[1][1]

    def __write_blocks(self, block_hash):
        try:
            block = self.__blocks[block_hash]
            block_name = block["opcode"]
            category = self.__categorize_blocks(block_name)
            self.__node_id += 1
            match category:
                case "EVENT":
                    self.__node_id = 0
                    self.__dfM.add_row(
                        [
                            "SCRIPT",
                            None,
                            None,
                            self.__node_id,
                            self.__get_parent_index(block),
                            None,
                        ]
                    )
                    self.__node_id += 1
                    if block_name == constants.EVENT_KEY_BLOCK:
                        key_name = self.__blocks[block_hash]["fields"]["KEY_OPTION"][0]
                        self.__dfM.add_row(
                            [
                                block_name,
                                key_name,
                                None,
                                self.__node_id,
                                self.__get_parent_index(block),
                                block_hash,
                            ]
                        )
                    else:
                        self.__dfM.add_row(
                            [
                                block_name,
                                None,
                                None,
                                self.__node_id,
                                self.__get_parent_index(block),
                                block_hash,
                            ]
                        )
                    if block["next"]:
                        self.__write_blocks(block["next"])
                case "REPEAT":
                    self.__dfM.add_row(
                        [
                            block_name,
                            None,
                            None,
                            self.__node_id,
                            self.__get_parent_index(block),
                            block_hash,
                        ]
                    )
                    if block_name == constants.REPEAT_BLOCK:
                        times = int(self.__get_variable_value(block["inputs"]["TIMES"]))
                    elif block_name == constants.FOREVER_BLOCK:
                        times = constants.REPEAT_TIMES
                    if block["inputs"]["SUBSTACK"]:
                        for key in range(times):
                            self.__write_blocks(block["inputs"]["SUBSTACK"][1])
                    if block["next"]:
                        self.__write_blocks(block["next"])
                case "IF":
                    self.__dfM.add_row(
                        [
                            block_name,
                            None,
                            None,
                            self.__node_id,
                            self.__get_parent_index(block),
                            block_hash,
                        ]
                    )
                    if block["inputs"]["SUBSTACK"]:
                        self.__write_blocks(block["inputs"]["SUBSTACK"][1])
                case "VARIABLE":
                    if block_name == constants.SET_VARIABLE:
                        self.__variables[
                            block["fields"]["VARIABLE"][1]
                        ] = self.__get_variable_value(block["inputs"]["VALUE"])
                    elif block_name == constants.CHANGE_VARIABLE:
                        self.__variables[block["fields"]["VARIABLE"][1]] = str(
                            float(self.__variables[block["fields"]["VARIABLE"][1]])
                            + float(self.__get_variable_value(block["inputs"]["VALUE"]))
                        )
                    self.__dfM.add_row(
                        [
                            block_name,
                            None,
                            None,
                            self.__node_id,
                            self.__get_parent_index(block),
                            block_hash,
                        ]
                    )
                    if block["next"]:
                        self.__write_blocks(block["next"])
                case "CALL":
                    procedure_name = block["mutation"]["proccode"]
                    self.__dfM.add_row(
                        [
                            block_name,
                            None,
                            None,
                            self.__node_id,
                            self.__get_parent_index(block),
                            block_hash,
                        ]
                    )
                    for block_hash, block2 in self.__blocks.items():
                        if block2["opcode"] == constants.PROCEDURES_DEFINE:
                            if (
                                self.__blocks[block2["inputs"]["custom_block"][1]][
                                    "mutation"
                                ]["proccode"]
                                == procedure_name
                            ):
                                if block2["next"]:
                                    self.__dfM.add_row(
                                        [
                                            block2["opcode"],
                                            None,
                                            None,
                                            self.__node_id,
                                            self.__get_parent_index(block2),
                                            block_hash,
                                        ]
                                    )
                                    self.__write_blocks(block2["next"])
                                    break
                    if not self.__has_forever_block(block_hash):
                        self.__write_blocks(block["next"])
                case _:
                    if block["inputs"] != None:
                        for key, input in block["inputs"].items():
                            if isinstance(block["inputs"][key][1], list):
                                block["inputs"][key][1][1] = self.__get_variable_value(
                                    input
                                )
                        self.__dfM.add_row(
                            [
                                block_name,
                                None,
                                single_to_double(str(block["inputs"])),
                                self.__node_id,
                                self.__get_parent_index(block),
                                block_hash,
                            ]
                        )
                    elif block["fields"] != None:
                        self.__dfM.add_row(
                            [
                                block_name,
                                single_to_double(str(block["fields"])),
                                None,
                                self.__node_id,
                                self.__get_parent_index(block),
                                block_hash,
                            ]
                        )
                    else:
                        self.__dfM.add_row(
                            [
                                block_name,
                                None,
                                None,
                                self.__node_id,
                                self.__get_parent_index(block),
                                block_hash,
                            ]
                        )

                    if block["next"]:
                        self.__write_blocks(block["next"])
        except Exception as e:
            print(e)
