import sys
sys.path.append('../')

from utils import DfManager
from config import constants

class Sorter:
    __IF_BLOCKS = constants.IF_BLOCKS
    __R_BLOCKS = constants.REPEAT_BLOCKS

    def __init__(self, project):
        self.__dfM = DfManager(['BlockName', 'Key', 'Field', 'node_id', 'parent_id', 'hash'])
        self.__blocks = project['targets'][1]['blocks']
        self.__sprite = project['targets'][1]
        self.__node_id = 0
        
    
    def to_csv(self, dir_path):
        self.__dfM.to_csv(dir_path)
    
    def sort_blocks(self):
        self.__dfM.add_row([self.__sprite['direction'], self.__sprite['x'], self.__sprite['y'], None, None, None])
        for block_hash, blocks in self.__blocks.items():
            if ('event' in blocks['opcode']):
              self.__write_blocks(block_hash)

        return self.__dfM.get_df
    
    def __get_parent_index(self, block):
        if(block['parent']):
            df = self.__dfM.get_df()
            return df[df['hash'] == block['parent']].index.to_list()[0]
        else:
            return 0
        
    def __categorize_blocks(self, block_name):
        try:
            if("event" in block_name):
                return "EVENT"
            elif(block_name in self.__IF_BLOCKS):
                return "IF"
            elif(block_name in self.__R_BLOCKS):
                return "REPEAT"
            else:
                return "NORMAL"
        except Exception as e:
            print(e)
            
    
    def __write_blocks(self, block_hash):
      try:
          block = self.__blocks[block_hash]
          block_name = block["opcode"]
          category = self.__categorize_blocks(block_name)
          self.__node_id += 1
          match category:
             case "EVENT":
                self.__node_id = 0
                self.__dfM.add_row(['SCRIPT', None, None, self.__node_id, self.__get_parent_index(block), None])
                self.__node_id += 1
                if (block_name == constants.EVENT_KEY_BLOCK):
                    key_name = self.__blocks[block_hash]['fields']['KEY_OPTION'][0]
                    self.__dfM.add_row([block_name, key_name, None, self.__node_id, self.__get_parent_index(block), block_hash])
                else:
                    self.__dfM.add_row([block_name, None, None, self.__node_id, self.__get_parent_index(block), block_hash])
                if(block["next"]):     
                    self.__write_blocks(block['next'])
             case "REPEAT":
                self.__dfM.add_row([block_name, None, None, self.__node_id, self.__get_parent_index(block), block_hash])
                if(block_name == constants.REPEAT_BLOCK):
                  times = int(block["inputs"]["TIMES"][1][1])
                elif(block_name == constants.FOREVER_BLOCK):
                  times = constants.REPEAT_TIMES
                if(block["inputs"]["SUBSTACK"]):    
                  for key in range(times):
                    self.__write_blocks(block["inputs"]["SUBSTACK"][1]) 
             case "IF":
                self.__dfM.add_row([block_name, None, None, self.__node_id, self.__get_parent_index(block), block_hash])
                if(block["inputs"]["SUBSTACK"]):
                  self.__write_blocks(block["inputs"]["SUBSTACK"][1])
             case _:
                if(block["inputs"] != None):
                   self.__dfM.add_row([block_name, None, block['inputs'], self.__node_id, self.__get_parent_index(block), block_hash])
                elif(block["fields"] != None):
                   self.__dfM.add_row([block_name, block["fields"], None, self.__node_id, self.__get_parent_index(block), block_hash])
                else:
                   self.__dfM.add_row([block_name, None, None, self.__node_id, self.__get_parent_index(block), block_hash])
                
                if(block["next"]):
                   self.__write_blocks(block["next"])
      except Exception as e:
          print(e)

