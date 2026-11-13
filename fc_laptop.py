"""Sistem pakar Forward Chaining: penyebab laptop lambat atau panas.
Jalankan: python fc_laptop.py kb_laptop.json
Python 3.8+
"""
import json
import sys
 
 
def muat_kb(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
 
 
def syarat_terpenuhi(aturan, memori):
    ada = [j in memori for j in aturan["jika"]]
    return all(ada) if aturan["mode"] == "dan" else any(ada)
 
 
def cari_fakta_dasar(aturan_list):
    """Fakta yang tidak pernah jadi hasil aturan -> ditanyakan ke user."""
    hasil = {a["maka"] for a in aturan_list}
    dasar = []
    for a in aturan_list:
        for j in a["jika"]:
            if j not in hasil and j not in dasar:
                dasar.append(j)
    return dasar
 
 
def forward_chaining(aturan_list, fakta_awal):
    memori = set(fakta_awal)
    asal = {}      # fakta turunan -> aturan penghasilnya
    log = []
    siklus = 0
    while True:
        cocok = [a for a in aturan_list
                 if syarat_terpenuhi(a, memori) and a["maka"] not in memori]
        if not cocok:
            siklus += 1
            log.append(f"Siklus {siklus}: tidak ada aturan baru, berhenti")
            break
        r = cocok[0]
        siklus += 1
        memori.add(r["maka"])
        asal[r["maka"]] = r
        log.append(f"Siklus {siklus}: {r['id']} -> {r['maka']}")
    return memori, asal, log
 
 
def tulis_alasan(fakta, asal, memori, indent=1, keluar=None, sudah=None):
    keluar = [] if keluar is None else keluar
    sudah = set() if sudah is None else sudah
    r = asal.get(fakta)
    if r is None or fakta in sudah:
        return keluar
    sudah.add(fakta)
    dipakai = [j for j in r["jika"] if j in memori]
    keluar.append("  " * indent + f"{fakta}  <- {r['id']} ({', '.join(dipakai)}) [{r['sumber']}]")
    for j in dipakai:
        tulis_alasan(j, asal, memori, indent + 1, keluar, sudah)
    return keluar
 
 
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "kb_laptop.json"
    kb = muat_kb(path)
    aturan = kb["aturan"]
 
    print(kb["judul"])
    print("Jawab y/t.")
    ya = []
    for i, fakta in enumerate(cari_fakta_dasar(aturan), 1):
        jawab = ""
        while jawab not in ("y", "t"):
            try:
                jawab = input(f"{i}. Apakah {fakta}? (y/t) > ").strip().lower()
            except EOFError:
                jawab = "t"
        if jawab == "y":
            ya.append(fakta)
 
    print()
    print("Fakta awal:", ", ".join(ya) if ya else "(tidak ada)")
    print()
    memori, asal, log = forward_chaining(aturan, ya)
    for baris in log:
        print(baris)
    print()
 
    dipakai_sbg_syarat = {j for a in aturan for j in a["jika"]}
    akhir = [f for f in asal if f not in dipakai_sbg_syarat]
 
    if akhir:
        print("Kesimpulan:")
        for f in akhir:
            print(f"  - {f}")
        print("Alasan:")
        for f in akhir:
            for baris in tulis_alasan(f, asal, memori):
                print(baris)
    else:
        print("Kesimpulan: tidak ada kesimpulan dari fakta yang diberikan.")
        print("Alasan: tidak ada aturan yang syaratnya terpenuhi sampai ke saran.")
    print()
    print("Catatan:", kb["batas"])
 
 
if __name__ == "__main__":
    main()
 