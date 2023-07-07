import sys
sys.path.append('../')

from utils import DfManager

class Sorter:
    # 座標情報を格納しているキー名
    __MOVE = ['STEPS', 'DEGREES', 'DIRECTION', 'X', 'Y', 'DX', 'DY']
    # 待機時間情報を格納しているキー名
    __WAIT = ['DURATION', 'SECS']

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
              self.__write_event_block(block_hash)

        return self.__dfM.get_df
    
    def __get_parent_index(self, block):
        if(block['parent']):
            print(block['parent'])
            df = self.__dfM.get_df()
            return df[df['hash'] == block['parent']].index
        else:
            return 0
        
    def __identify_blocks(self, block_hash):
        try:
            block = self.__blocks[block_hash]
            if (block['inputs'] != None):
                    for key in block['inputs']:
                        # 制御ブロックor条件付きブロックの場合その中身も見る
                        if (key == 'SUBSTACK' or key == 'CONDITION'):
                            self.__write_blocks(block['inputs'][str(key)][1])
                        # 条件ブロックの中身を見る
                        if (key == 'KEY_OPTION' and block['inputs']['KEY_OPTION'][1] != None):
                            self.__write_blocks(block['inputs'][str(key)][1], key)
            # 次のブロックを見る
            if (block['next'] != None):
                self.__write_blocks(block['next'])
        except Exception as e:
            print('1')
            print(e)
            
    
    def __write_blocks(self, block_hash, field_name = None):
      try:
          block = self.__blocks[block_hash]
          block_name = block['opcode']

          self.__node_id += 1
          flg = False
          if(field_name):
              self.__dfM.add_row([block_name, block['fields'][field_name][0], None, self.__node_id, self.__get_parent_index(block), block_hash])
          else:
              if (block['inputs'] == "{{}}"):
                  self.__dfM.add_row([block_name, None, None, self.__node_id, self.__get_parent_index(block), block_hash])
              else:
                  for key in block['inputs']:
                      if (key in self.__MOVE or key in self.__WAIT):
                          self.__dfM.add_row([block_name, None, block['inputs'], self.__node_id, self.__get_parent_index(block), block_hash])
                          flg = True
                          break
                  if not flg:
                      self.__dfM.add_row([block_name, None, None, self.__node_id, self.__get_parent_index(block), block_hash])

          self.__identify_blocks(block_hash)
      except Exception as e:
          print('2')
          print(e)
    
    def __write_event_block(self, block_hash):
    # 次のブロックがあるか確認
      try:
          if (self.__blocks[block_hash]['next'] != None):
              block = self.__blocks[block_hash]
              block_name = block['opcode']
              # CSVファイルにブロック情報を書き込む

              self.__dfM.add_row(['SCRIPT', None, None, self.__node_id, self.__get_parent_index(block), None])

              self.__node_id += 1
              if (block_name == 'event_whenkeypressed'):
                  key_name = self.__blocks[block_hash]['fields']['KEY_OPTION'][0]
                  self.__dfM.add_row([block_name, key_name, None, self.__node_id, self.__get_parent_index(block), block_hash])
              else:
                  self.__dfM.add_row([block_name, None, None, self.__node_id, self.__get_parent_index(block), block_hash])
              
              self.__write_blocks(self.__blocks[block_hash]['next'])
      except Exception as e:
          print('3')
          print(e)  

