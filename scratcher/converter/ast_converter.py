import json

from config import constants


class AstConverter:
    __C_BLOCKS = constants.CONTROL_BLOCKS

    def __init__(self, project):
        self.__project = project
        self.__ast = {"type": "Scratch", "sprites": []}

    def get_ast(self, path=""):
        self.__project_to_ast()
        if path:
            with open(path, "w") as json_file:
                json.dump(self.__ast, json_file)

        ast = self.__ast

        return ast

    def __has_nextblock(self, block):
        if block["next"]:
            return True
        else:
            return False

    def __children_to_ast(self, hash):
        children_ast = []
        block = {}
        while True:
            block = self.__blocks[hash]
            block_ast = self.__block_to_ast(block)
            children_ast.append(block_ast)
            print("children")
            if self.__has_nextblock(block):
                hash = block["next"]
                continue
            else:
                break

        return children_ast

    def __block_to_ast(self, block):
        block_ast = {
            "name": block["opcode"],
        }
        if block in self.__C_BLOCKS:
            if block == "control_if_else":
                for key in ["SUBSTACK", "SUBSTACK2"]:
                    if key in block["inputs"]:
                        block_ast.update(
                            {key: self.__children_to_ast(block["inputs"][key][1])}
                        )
            else:
                if "SUBSTACK" in block["inputs"]:
                    block_ast.update(
                        {"SUBSTACK": self.__children_to_ast(block["inputs"][key][1])}
                    )
        else:
            block_ast.update({"inputs": block["inputs"]})

        return block_ast

    def __sprite_to_ast(self, hash):
        sprite_ast = []
        block = {}
        while True:
            block = self.__blocks[hash]
            block_ast = self.__block_to_ast(block)
            sprite_ast.append(block_ast)
            print("sprite")
            if self.__has_nextblock(block):
                hash = block["next"]
                continue
            else:
                break

        return sprite_ast

    def __project_to_ast(self):
        for sprite_data in self.__project["targets"]:
            sprite_name = sprite_data["name"]
            json_blocks = sprite_data["blocks"]
            self.__blocks = json_blocks
            # ステージは無視
            for hash, block in self.__blocks.items():
                if block["topLevel"] == True:
                    sprite_ast = self.__sprite_to_ast(hash)

                    self.__ast["sprites"].append(
                        {"name": sprite_name, "blocks": sprite_ast}
                    )
