# HRM Rooster – lokaal, niets online

Alles draait op je eigen pc in je eigen wifi/netwerk. Er gaat niets naar internet of GitHub.

| Bestand | Wat het doet |
|---|---|
| `start.bat` | Start de lokale server (dubbelklikken) |
| `server.py` | De server zelf (serveert de pagina's en slaat het rooster op) |
| `index.html` | Het scherm voor de tv |
| `admin.html` | Het dashboard waarmee je het rooster aanpast |
| `schedule.json` | Het rooster (wordt door het dashboard bijgewerkt) |
| `backups/` | Wordt automatisch gemaakt: bij elke keer opslaan een kopie van de vorige versie (laatste 50) |

## Gebruik

1. **Start de server:** dubbelklik op `start.bat`. Er opent een zwart venster met de adressen, bijvoorbeeld:
   ```
   Tv:        http://192.168.1.25:8080/
   Dashboard: http://192.168.1.25:8080/admin.html
   ```
   Laat dat venster open staan (sluiten = server stopt). Je hebt Python nodig (is al geïnstalleerd als `python --version` werkt).
2. **Tv:** open op de Google TV (Fully Kiosk Browser of Chrome) het *Tv*-adres. Het scherm haalt elke 2 minuten het nieuwste rooster op.
3. **Dashboard:** open het *Dashboard*-adres op je pc of telefoon (zelfde wifi). Pas lessen aan en klik bovenaan op **Opslaan**. Binnen 2 minuten staat het op de tv.

Tip: geef de pc in je router een vast IP-adres (DHCP-reservering), anders kan het adres na een herstart veranderen en moet je het op de tv opnieuw invullen.

## Pincode (optioneel)

Wil je dat niet iedereen op je wifi het rooster kan aanpassen? Maak naast `server.py` een bestand `pin.txt` met alleen je pincode erin (bijv. `4821`). Het dashboard vraagt er dan één keer om bij het opslaan. Verwijder het bestand om de pincode uit te zetten.

## Het dashboard

- Kies een dag (Ma t/m Zo) en pas tijd, lesnaam, instructeur en soort (icoon/kleur) aan.
- *Op groot scherm (virtueel)* = les op het tv-scherm in de zaal.
- Toevoegen, dupliceren, verwijderen, en *Kopieer deze dag naar…* voor dagen die hetzelfde zijn.
- Meer dan 5 lessen op één dag past niet netjes op het tv-scherm; het dashboard waarschuwt.
- Fout gemaakt? Kopieer een oudere versie uit `backups/` over `schedule.json`.

## Automatisch starten met Windows (optioneel)

Wil je dat de server vanzelf start als de pc aan gaat? Druk `Win + R`, typ `shell:startup` en zet daar een snelkoppeling naar `start.bat`.

## Goed om te weten

- De pc moet aan staan en op hetzelfde netwerk zitten als de tv, anders blijft de tv het laatst geladen rooster tonen (en bij een herstart van de tv het ingebouwde reserve-rooster).
- Windows vraagt de eerste keer om toegang via de firewall voor Python: kies **Privénetwerk toestaan**.
- Dubbelklik je `index.html` zonder server, dan zie je alleen het ingebouwde reserve-rooster.
- De pagina `247/index.html` (openingstijden) is een los bestand en zit niet in dit dashboard.
