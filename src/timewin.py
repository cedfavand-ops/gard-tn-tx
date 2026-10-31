from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from . import config as C


def gust_window_utc(D):
    """Jour civil local de demain [00:00, 24:00] en UTC. D = minuit UTC du jour de la prévision."""
    tz = ZoneInfo(C.GUST_TZ)
    day = (D + timedelta(days=1)).date()
    nxt = day + timedelta(days=1)
    s = datetime(day.year, day.month, day.day, tzinfo=tz).astimezone(timezone.utc)
    e = datetime(nxt.year, nxt.month, nxt.day, tzinfo=tz).astimezone(timezone.utc)
    return s, e


def gust_valid_times(D):
    """Échéances horaires (s, e] : VMAX_10M à l'heure t = maximum sur l'heure qui précède."""
    s, e = gust_window_utc(D)
    n = int(round((e - s).total_seconds() / 3600))
    return [s + timedelta(hours=k) for k in range(1, n + 1)]
