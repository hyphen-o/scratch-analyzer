import sys

sys.path.append("../../")

from api import scratch_client

#２回派生した作品
sample_id = 971467755
#１回派生した作品
sample_id2 = 971457785
#リミックスしていない作品
sample_id3 = 732248801
PM = scratch_client.get_remix_parent(sample_id)
if PM:
  print("parent_id: " + str(PM["parent_id"]))
  print("deep: " + str(PM["deep"]))
