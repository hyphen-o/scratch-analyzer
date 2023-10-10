from dotenv import load_dotenv
import os

# .envファイルの内容を読み込見込む
load_dotenv()

def env(var):
  return os.environ[var]