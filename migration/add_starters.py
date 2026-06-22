#!/usr/bin/env python3
"""add_starters.py — fix boards reading "0 projects" that actually have a demo.

- Adds a "Python Lite SDK" starter sample-card for each board whose
  iotc-python-lite-sdk-demos folder had no example subfolders (so it was only a
  quickstart resource before, not a listing).
- Expands existing SDK listings to reference boards whose samples weren't linked.
"""
import os, csv

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
LITE = "https://github.com/avnet-iotconnect/iotc-python-lite-sdk-demos/tree/main/"

# short name, Part Number, folder, full name, topics
STARTERS = [
    ("Arduino UNO Q", "ARDUINO-UNO-Q", "arduino-uno-q", "Arduino UNO Q", "mpu"),
    ("PIC64GX Curiosity", "CURIOSITY-PIC64GX1000-KIT", "microchip-pic64gx1000", "Microchip PIC64GX Curiosity Kit", "mpu"),
    ("S32G GoldBox", "S32G-VNP-GLDBOX", "nxp-s32g-vnp-gldbox3", "NXP S32G GoldBox", "mpu"),
    ("MaaXBoard 8M", "AES-MC-SBC-IMX8M-G", "tria-maaxboard-8m", "Avnet MaaXBoard 8M", "mpu"),
    ("MaaXBoard 8ULP", "AES-MAAXB-8ULP-SK-G", "tria-maaxboard-8ulp", "Avnet MaaXBoard 8ULP", "mpu"),
    ("RZ/G3E EVK", "RZ-G3E-EVK", "renesas-rzg3e-evk", "Renesas RZ/G3E Evaluation Kit", "mpu, edge-ai"),
]
# add boards to existing SDK listings (board samples exist but weren't linked)
EXPAND = {
    "/IOTCONNECT C SDK for Azure RTOS": ["ATSAME54-XPRO", "AES-MC-SBC-IMXRT1176-G"],
    "/IOTCONNECT DA16K SDK": ["DA16600MOD-DEVKT"],
    "ModusToolbox Basic Example": ["CY8CPROTO-062S3-4343W"],
}

p = os.path.join(DATA, "listings.csv")
rows = list(csv.reader(open(p, newline="", encoding="utf-8")))
H = rows[0]; idx = {c: H.index(c) for c in H}
names = {r[idx["Name"]].strip().lower() for r in rows[1:]}

# expand existing listings' Boards
for r in rows[1:]:
    nm = r[idx["Name"]].strip()
    if nm in EXPAND:
        have = [b.strip() for b in r[idx["Boards"]].split(",") if b.strip()]
        for b in EXPAND[nm]:
            if b not in have: have.append(b)
        r[idx["Boards"]] = ", ".join(have)

# append starter cards
added = 0
for short, pn, folder, full, topics in STARTERS:
    name = f"{short} — Python Lite SDK"
    if name.lower() in names:
        continue
    row = [""] * len(H)
    row[idx["Name"]] = name
    row[idx["Type"]] = "sample"
    row[idx["Status"]] = "beta"
    row[idx["Repo"]] = "iotc-python-lite-sdk-demos"
    row[idx["Languages"]] = "Python"
    row[idx["Topics"]] = topics
    row[idx["Boards"]] = pn
    row[idx["Description"]] = (f"Get started with the /IOTCONNECT Python Lite SDK on the {full}: "
                               "stream telemetry, receive cloud commands and run OTA updates from a Python app.")
    row[idx["Link"]] = LITE + folder
    row[idx["Include"]] = "yes"
    rows.append(row); added += 1

csv.writer(open(p, "w", newline="", encoding="utf-8"), lineterminator="\n").writerows(rows)
print(f"added {added} starter cards; expanded {len(EXPAND)} SDK listings")
