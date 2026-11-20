"""Extract per-packet Voice end-to-end delay (voEndToEndDelay:vector on node[*].app[0])
from OMNeT++ .vec files, using the .vci index to seek only to the relevant blocks.
Same vector selection as kpi_dashboard parse_vec_metrics (DelayMetric::Vo).

usage: extract_vo.py OUT.npz RESULTS_DIR [RESULTS_DIR ...]
"""
import re
import sys
from pathlib import Path

import numpy as np

APP0 = re.compile(r"^Scenario\.node\[\d+\]\.app\[0\]$")


def vo_delays(vci: Path) -> np.ndarray:
    ids, blocks = set(), []
    with open(vci) as fh:
        for line in fh:
            p = line.split()
            if not p:
                continue
            if p[0] == "vector":
                if p[3] == "voEndToEndDelay:vector" and APP0.match(p[2]):
                    ids.add(p[1])
            elif p[0] in ids:
                blocks.append((p[0], int(p[1]), int(p[2])))
    vals = []
    with open(vci.with_suffix(".vec"), "rb") as fh:
        for vid, off, length in blocks:
            fh.seek(off)
            for raw in fh.read(length).decode().splitlines():
                q = raw.split()
                if len(q) >= 4 and q[0] == vid:
                    v = float(q[3])
                    if np.isfinite(v):
                        vals.append(v)
    return np.asarray(vals)


def main():
    out = sys.argv[1]
    data = {}
    for d in sys.argv[2:]:
        tag = Path(d).parent.name.replace("veins_inet_", "")
        for vci in sorted(Path(d).glob("*.vci")):
            key = f"{tag}/{vci.stem}"
            data[key] = vo_delays(vci)
            print(f"{key}: n={data[key].size}", flush=True)
    np.savez_compressed(out, **data)


if __name__ == "__main__":
    main()
