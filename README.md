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

## Nieuwe mogelijkheden in het dashboard

- **Live voorbeeld** bovenaan: je ziet het tv-scherm direct meeveranderen terwijl je bewerkt, ook vóór je opslaat. Je kunt een andere dag kiezen en de mededeling testen.
- **Icoon per les:** kies uit 60 iconen (dumbbell, trofee, vuur, muziek, enz.). Zonder keuze geldt het standaardicoon van de soort.
- **Kleur per les:** kleurkiezer of een van de snelkeuzes. Dit kleurt het icoonvlak in het dagoverzicht en het bolletje in het weekrooster.
- **Hoofdkleuren van het scherm:** twee kleuren bepalen titels, randen, tijden en markeringen. Met één klik terug naar de standaard.
- **Les laten vervallen:** vink “Vervallen” aan. Op het scherm staat de les doorgestreept met “Vervallen” en telt hij niet meer mee als volgende of lopende les.
- **Mededeling:** een grote melding over het hele scherm die om de zoveel seconden even verschijnt (tekst, icoon, kleur, hoe vaak, hoe lang, optioneel t/m een datum).

- **Uitzonderingen per datum** (tabblad *Uitz.* naast de dagen): zet een feestdag of afwijkend rooster klaar voor één specifieke datum. Drie soorten: *Gesloten*, *Andere lessen* (vervangt die dag; met een knop om het gewone rooster over te nemen) en *Extra lessen erbij*. Met een optionele tekst die op het scherm bij de dag staat. Na de datum is het vanzelf weer het gewone rooster; verlopen uitzonderingen kun je met één knop opruimen.
- **Automatisch “morgen”:** zijn alle lessen van vandaag voorbij, dan toont het linkerpaneel vanzelf de lessen van morgen (titel “MORGEN”, zonder aftellers). Is vandaag een gesloten dag, dan blijft de melding de hele dag staan.

- **Eenmalige wijziging van een les:** bij elke les staat een knop **↻ Eenmalig wijzigen**. Kies de datum en vul in wat anders is: vervangende instructeur, andere naam of tijd, of “Les vervalt op deze datum”. Alleen op die datum; daarna is het weer normaal. Op het scherm staat de instructeur dan in geel met “vervanging”. Je vindt ze ook onder het tabblad *Uitz.*
- **Eerstvolgende les groot in beeld:** een grote kaart met een aftelklok boven de lijst (aan/uit en vanaf hoeveel minuten ervoor in te stellen). Afgelopen lessen worden een dunne regel, zodat er ruimte blijft voor wat nog komt.
- **Klok en datum** rechtsboven bij het weekrooster (uit te zetten onder *Extra's op het scherm*).

Let op: na het updaten van `server.py` (die accepteert nu ook de instellingen) moet je de server herstarten. Op Linux: `sudo systemctl restart rooster`.

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

- De poort is standaard 8080. Een andere poort kies je met `python server.py 9123`.
- De pc moet aan staan en op hetzelfde netwerk zitten als de tv, anders blijft de tv het laatst geladen rooster tonen (en bij een herstart van de tv het ingebouwde reserve-rooster).
- Windows vraagt de eerste keer om toegang via de firewall voor Python: kies **Privénetwerk toestaan**.
- Dubbelklik je `index.html` zonder server, dan zie je alleen het ingebouwde reserve-rooster.
- De pagina `247/index.html` (openingstijden) is een los bestand en zit niet in dit dashboard.
