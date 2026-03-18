import pandas as pd
from datetime import datetime, date


def caffeine_remaining(dose_mg, hours_since, half_life_h):
    """
    Berechnet den verbleibenden Koffeinwert im Körper.

    Formel:
    Rest = Dosis * 0.5^(Zeit / Halbwertszeit)
    """
    if half_life_h <= 0:
        return 0.0

    return dose_mg * (0.5 ** (hours_since / half_life_h))


def get_default_values():
    """
    Standard-Koffeinwerte pro 250 ml.
    """
    return {
        "Kaffee": 95,
        "Espresso": 60,
        "Energy Drink": 80,
        "Red Bull": 80,
        "NOCCO": 180,
        "Mate": 80,
        "Matcha": 70,
        "Schwarzer Tee": 45,
        "Eigener Wert": 0
    }


def find_caffeine_zero_time(dose_mg, horizon, half_life):
    """
    Sucht die erste Stunde, ab der weniger als 0.5 mg Koffein vorhanden sind.
    """
    for h in range(1, horizon + 1):
        if caffeine_remaining(dose_mg, h, half_life) < 0.5:
            return h
    return None


def create_chart_data(dose_mg, horizon, half_life):
    """
    Erstellt die Daten für das Liniendiagramm.
    """
    data = []

    for h in range(horizon + 1):
        remaining = caffeine_remaining(dose_mg, h, half_life)
        data.append({
            "Stunden": h,
            "Koffein (mg)": remaining
        })

    return pd.DataFrame(data).set_index("Stunden")


def create_history_row(drink, taken_at, dose_mg, half_life, caffeine_zero_time, horizon):
    """
    Erstellt eine neue Zeile für den Verlauf.
    """
    if caffeine_zero_time is not None:
        zero_datetime = taken_at + pd.Timedelta(hours=caffeine_zero_time)
        kein_koffein_text = f"nach {caffeine_zero_time} Stunde(n), um {zero_datetime.strftime('%H:%M')} Uhr"
    else:
        kein_koffein_text = f"nicht innerhalb von {horizon} Stunden"

    return {
        "Getränk": drink,
        "Wann eingenommen": taken_at.strftime("%d.%m.%Y %H:%M"),
        "Koffeinmenge zu Beginn (mg)": round(dose_mg, 1),
        "Halbwertszeit (h)": half_life,
        "Kein Koffein mehr": kein_koffein_text
    }


def calculate_caffeine_data(drink, dose_mg, intake_time, horizon, half_life):
    """
    Hauptfunktion:
    Berechnet alle Daten und gibt EIN Dictionary zurück,
    damit der Code in views kurz bleibt.
    """
    now = datetime.now()
    taken_at = datetime.combine(date.today(), intake_time)

    hours_since = (now - taken_at).total_seconds() / 3600
    if hours_since < 0:
        hours_since = 0

    current = caffeine_remaining(dose_mg, hours_since, half_life)
    caffeine_zero_time = find_caffeine_zero_time(dose_mg, horizon, half_life)
    df = create_chart_data(dose_mg, horizon, half_life)
    new_row = create_history_row(
        drink=drink,
        taken_at=taken_at,
        dose_mg=dose_mg,
        half_life=half_life,
        caffeine_zero_time=caffeine_zero_time,
        horizon=horizon
    )

    if caffeine_zero_time is not None:
        zero_datetime = taken_at + pd.Timedelta(hours=caffeine_zero_time)
        kein_koffein_text = f"nach {caffeine_zero_time} Stunde(n), um {zero_datetime.strftime('%H:%M')} Uhr"
    else:
        kein_koffein_text = f"nicht innerhalb von {horizon} Stunden"

    return {
        "current": current,
        "taken_at": taken_at,
        "hours_since": hours_since,
        "caffeine_zero_time": caffeine_zero_time,
        "df": df,
        "new_row": new_row,
        "kein_koffein_text": kein_koffein_text
    }