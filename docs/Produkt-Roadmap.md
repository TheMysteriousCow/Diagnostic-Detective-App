# Produkt-Roadmap
Diese Roadmap zeigt die geplanten Entwicklungsschritte für unsere App zur Berechnung und zum bewussten Umgang mit Koffein.
Die Funktionen wurden nach Priorität und Nutzermehrwert in mehrere aufeinanderfolgende Versionen gegliedert.
Jede Version ist funktionsfähig und erweiterbar.

## Version 1.0 - Einfaches Login-System erstellen (MVP Basis)
Login-System:
- Benutzername & Passwort
- Mehrere Nutzer: Nutzung durch verschiedene Personen
- Datensicherung: Speicherung der Daten pro Nutzer
Technisches Setup:
- Grundstruktur der App (Navigation, Seiten) (ca.20min)
- Einrichten von .streamlit/secrets.toml (ca.15min)   # Hemer das so??
- Erste einfache Datenstruktur erstellen (ca.15min)
- Veröffentlichung der App

Diese Version bildet die Basis der App und ermöglicht erste Tests.

## Version 2.0 - Calculator - MVP (Minimal Viable Product)
Eingaben:
- Auswahl der verschiedenen koffeinhaltigen Getränken (z. B. Kaffee, Energy Drink, Mate) (ca.20min)
- Eingabe der konsumierten Menge (ml) (ca.10min)
- Eingabe des Zeitpunkts der Einnahme (ca.10min)
Berechnung:
- Berechnung des aktuellen Koffeinlevels im Körper (ca.30min)
- Berechnung basierend auf der Halbwertszeit von Koffein (ca.30min)

Ausgabe:
- Anzeige des verbleibenden Koffeins (ca.15min)
- Erste einfache Rückmeldung mit Text (ca.15min)

Ziel: Funktionierender Kern der App, Berechnung von Koffein im Körper

## Version 3.0 - Erweiterung: Verlauf (History)
Datenspeicherung:
- Speicherung der eingegebenen Koffeinwerte (ca.20min)
Übersicht:
- Darstellung der Werte in Tabellenform (ca.30min)
- Zugriff auf vergangene Einträge (60min)
Analyse:
- Sortierung nach Datum und Zeit (Timestamp) (ca.30min)

Ziel: langfristiges Tracking des Konsums

## Version 4.0 - Erweiterung: Benutzerprofil
Profilseite (Your Profile):
- Name, Alter, Gewicht  (ca.15min)
- Geschlecht (ca.15min)
- Sprache (ca.15min) # Machemer das??
Zusätzliche Daten (Additional Data):
- Medikamenteneinnahme (ca.20min)
- weitere relevante Faktoren (z.B Grunderkrankungen, Allergien) (ca.20min)
Personalisierung:
- Anpassung der Berechnung basierung auf Nutzerdatem (z.B Gewicht) (ca.60min)

Ziel: individuellere und genauere Ergebnisse

## Version 5.0 - Erweiterung: Empfehlungen (Recommendations)
Visualisierung:
- Darstellung in Form einer Kurve (z. B. Peak, Abbau, Müdigkeit) (ca.45min)
Empfehlungs-System: (ca.45min)
Anzeige von Zuständen wie:
- „Peak“
- „I can't fall asleep“
- „I feel tired“

Interaktive Auswahl:
- Nutzer kann auswählen, wie er sich fühlt (ca.20min)
- passende Empfehlungen werden angezeigt (ca.30min)
Detailseiten (z. B. „I can’t fall asleep“):
- konkrete Tipps zur Verbesserung (ca.30min)
- Hinweise zum Umgang mit zu viel Koffein (ca.30min)

Ziel: Nutzer versteht seinen Koffeinzustand besser und direkte Hilfe bei Problemen (hoher Nutzermehrwert) 

## Version 6.0 - Erweiterung: Alternativen
Auswahl alternative Getränke:
- mit Koffein (z. B. Guarana, Matcha) (ca.15min)
- ohne Koffein (z. B. Kräutertee, Wasser) (ca.15min)
Empfehlungen je nach Situation:
- z. B. bei Müdigkeit oder Schlafproblemen (ca.30min)
Informationsbereich:
- kurze Beschreibung der Alternativen (ca.20min)

Ziel: bewusster Konsum statt nur Berechnung

# Version 6.5 - Erweiterung: Farbcodierte Alternativen
Alternativen nach Farben sortieren:
- Grün = Gesunde Alternative
- Gelb = Weniger gesunde Alternative
- Rot = Ungesunde Alternative

Ziel: Schnelle, intuitive Bewertung von Alternativen für bewussteren Konsum

### Optional  Weiterführende Ideen (nicht Teil des aktuellen Zeitrahmens)
Diese weiterführenden Ideen zeigen das Potenzial der App und mögliche Ausbaustufen, die im Rahmen dieses Projekts nicht umgesetzt werden, aber zukünftige Weiterentwicklungen ermöglichen.

Verknüpfung mit Fachpersonen:
- Weiterleitung zu Ernährungsberater:innen oder medizinischen Fachstellen

Ziel: Unterstützung bei starkem Koffeinkonsum oder gesundheitlichen Problemen

Soziale Funktionen:
- Verbindung mit Freund:innen
- gegenseitiges Teilen des Koffeinkonsums

Ziel: Unterstützung im Alltag, Wir-Gefühl erzeugen
  
Spielerische Elemente:
- Belohnungssystem (z. B. Punkte, Levels)

Ziel: Motivation und Durchhaltevermögen fördern


