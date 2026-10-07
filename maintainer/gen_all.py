import gen_batch1, gen_batch2, gen_batch3, gen_batch4
from genlib import save_manifest, MANIFEST
save_manifest()
from collections import Counter
print(Counter(e["topic"] for e in MANIFEST))
print("total:", len(MANIFEST))
