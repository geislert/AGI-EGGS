"""
AGI-EGG Backend Prototype
=========================

This script provides a minimal backend implementation for the AGI-EGG
framework. It ingests text files, stores fragments in an SQLite database,
calculates a simple spin score and applies a "3-D" timestamp model.

The goal is to demonstrate how a future backend might organize data for
use by the HTML/JS command post interface.
"""

import os
import re
import time
import json
import sqlite3
from dataclasses import dataclass, asdict
from datetime import datetime

DB_FILE = "agi_egg_data.db"
AGE_OF_UNIVERSE_SEC = 13.8e9 * 365.25 * 24 * 3600
PLANCK_TIME = 5.391e-44

DOMAIN_POLICIES = {
    "default": [re.compile(r"exploit\s+vulnerability", re.I)],
    "medical": [re.compile(r"unauthorized\s+experiments", re.I)],
    "legal": [re.compile(r"warrantless\s+surveillance", re.I)],
    "military": [re.compile(r"biological\s+weapon", re.I)],
}

@dataclass
class Timestamp3D:
    quantum: float
    classical: str
    cosmological: float

@dataclass
class Fragment:
    content: str
    source: str
    source_type: str
    timestamp: Timestamp3D
    weight: float = 0.5
    purity: float = 0.5
    utility: float = 0.5
    dimension: float = 0.5


def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS fragments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            source TEXT,
            source_type TEXT,
            ts_quantum REAL,
            ts_classical TEXT,
            ts_cosmological REAL,
            weight REAL,
            purity REAL,
            utility REAL,
            dimension REAL,
            spin_score REAL
        )"""
    )
    conn.commit()
    conn.close()


def apply_3d_timestamp() -> Timestamp3D:
    now = time.time()
    return Timestamp3D(
        quantum=(now * 1e-18) % PLANCK_TIME,
        classical=datetime.utcnow().isoformat(),
        cosmological=now / AGE_OF_UNIVERSE_SEC,
    )


def compute_spin_score(f: Fragment) -> float:
    metrics = [f.weight, f.purity, f.utility, f.dimension]
    base = sum(m * m for m in metrics) ** 0.5
    age_days = (time.time() - datetime.fromisoformat(f.timestamp.classical).timestamp()) / (
        24 * 3600
    )
    decay = 0.5 ** (age_days / 90)
    return base * decay


def ethics_check(domain: str, content: str) -> bool:
    patterns = DOMAIN_POLICIES.get(domain, DOMAIN_POLICIES["default"])
    return not any(p.search(content) for p in patterns)


def ingest_file(path: str, source_type: str, domain: str = "default") -> int:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    chunks = [text[i : i + 1500] for i in range(0, len(text), 1500)]
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    count = 0
    for chunk in chunks:
        if not ethics_check(domain, chunk):
            continue
        frag = Fragment(
            content=chunk,
            source=os.path.basename(path),
            source_type=source_type,
            timestamp=apply_3d_timestamp(),
        )
        spin = compute_spin_score(frag)
        c.execute(
            """INSERT INTO fragments
               (content, source, source_type, ts_quantum, ts_classical,
                ts_cosmological, weight, purity, utility, dimension, spin_score)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                frag.content,
                frag.source,
                frag.source_type,
                frag.timestamp.quantum,
                frag.timestamp.classical,
                frag.timestamp.cosmological,
                frag.weight,
                frag.purity,
                frag.utility,
                frag.dimension,
                spin,
            ),
        )
        count += 1
    conn.commit()
    conn.close()
    return count


def list_fragments(limit: int = 5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        "SELECT source, ts_classical, spin_score, substr(content, 1, 40) FROM fragments ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = c.fetchall()
    conn.close()
    for r in rows:
        print(f"[{r[1]}] ({r[2]:.2f}) {r[0]}: {r[3]}...")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AGI-EGG backend prototype")
    sub = parser.add_subparsers(dest="cmd")

    ingest = sub.add_parser("ingest", help="ingest a text file")
    ingest.add_argument("file")
    ingest.add_argument("--type", default="user_upload")
    ingest.add_argument("--domain", default="default")

    list_cmd = sub.add_parser("list", help="list stored fragments")
    list_cmd.add_argument("--n", type=int, default=5)

    args = parser.parse_args()
    init_db()

    if args.cmd == "ingest":
        n = ingest_file(args.file, args.type, args.domain)
        print(f"Ingested {n} fragments from {args.file}")
    elif args.cmd == "list":
        list_fragments(args.n)
    else:
        parser.print_help()
