"""python -m src.run [--demo] [--res 150] [--out site] [--force-inversion 1]"""
import argparse, os, shutil
from datetime import datetime, timezone
from .grid import Grid
from .static import get_static
from .icon import demo_icon, fetch_icon, day_start
from .forecast import compute
from .render import write_all
from .archive import record_forecast


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="données ICON synthétiques (sans réseau)")
    ap.add_argument("--res", type=int, default=150, choices=[70, 150])
    ap.add_argument("--out", default="site")
    ap.add_argument("--force-inversion", type=float, default=None)
    ap.add_argument("--now", default=None, help="ISO UTC, pour rejouer un autre instant")
    a = ap.parse_args()

    now = datetime.fromisoformat(a.now).replace(tzinfo=timezone.utc) if a.now else datetime.now(timezone.utc)
    D = day_start(now)
    grid = Grid(a.res)
    os.makedirs(a.out, exist_ok=True)
    dem, mask, hp = get_static(grid, demo=a.demo)
    icon = demo_icon(now) if a.demo else fetch_icon(now)
    tn, tx, info = compute(icon, dem, mask, hp, grid, D, a.force_inversion)
    write_all(a.out, grid, tn, tx, mask, icon, info, D)
    record_forecast(D, icon, grid, tn, tx, info, dem, demo=a.demo)
    shutil.copy("web/index.html", f"{a.out}/index.html")
    print(f"OK run={icon.run:%Y-%m-%d %H}Z inversion={info['inversion']:.2f} "
          f"Tn[{tn[mask].min():.1f},{tn[mask].max():.1f}] Tx[{tx[mask].min():.1f},{tx[mask].max():.1f}] "
          f"ECOSTRESS={info['ecostress_cover']:.0%}")


if __name__ == "__main__":
    main()
