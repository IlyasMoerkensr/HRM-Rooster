"""Lokale server voor het HRM-rooster (alleen eigen netwerk, niets online).

Start met start.bat of:  python server.py [poort]
  - Tv:        http://<ip-van-deze-pc>:8080/
  - Dashboard: http://<ip-van-deze-pc>:8080/admin.html
Optioneel: zet een pincode in het bestand pin.txt, dan is die nodig om op te slaan.
"""
import json
import os
import shutil
import socket
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
SCHEDULE = os.path.join(ROOT, "schedule.json")
BACKUPS = os.path.join(ROOT, "backups")
PIN_FILE = os.path.join(ROOT, "pin.txt")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
MAX_BODY = 512 * 1024


def read_pin():
    try:
        with open(PIN_FILE, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def valid_schedule(data):
    # Nieuw formaat: {"settings": {...}, "days": [...]}; oud formaat: alleen de lijst met dagen
    if isinstance(data, dict):
        if not isinstance(data.get("settings", {}), dict):
            return False
        if not isinstance(data.get("exceptions", []), list):
            return False
        if not isinstance(data.get("substitutions", []), list):
            return False
        data = data.get("days")
    if not isinstance(data, list) or not data:
        return False
    for day in data:
        if not isinstance(day, dict) or not isinstance(day.get("dayIndex"), int):
            return False
        if not isinstance(day.get("classes"), list):
            return False
        for c in day["classes"]:
            if not isinstance(c, dict) or not isinstance(c.get("name"), str) or not isinstance(c.get("time"), str):
                return False
    return True


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # Altijd verse versie, zodat een wijziging direct zichtbaar is
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, status, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/info":
            return self._json(200, {"ok": True, "pinRequired": bool(read_pin())})
        # Server-bestanden en back-ups niet uitdelen
        if path in ("/server.py", "/pin.txt", "/start.bat") or path.startswith("/backups"):
            return self._json(404, {"error": "niet gevonden"})
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/schedule":
            return self._json(404, {"error": "niet gevonden"})
        pin = read_pin()
        if pin and self.headers.get("X-Pin", "") != pin:
            return self._json(401, {"error": "Pincode onjuist"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                raise ValueError("Ongeldige grootte")
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            if not valid_schedule(data):
                raise ValueError("Ongeldig roosterformaat")
        except (ValueError, UnicodeDecodeError) as e:
            return self._json(400, {"error": str(e)})

        os.makedirs(BACKUPS, exist_ok=True)
        if os.path.exists(SCHEDULE):
            shutil.copy2(SCHEDULE, os.path.join(BACKUPS, time.strftime("schedule-%Y%m%d-%H%M%S.json")))
            # Houd de laatste 50 back-ups
            files = sorted(f for f in os.listdir(BACKUPS) if f.startswith("schedule-"))
            for old in files[:-50]:
                os.remove(os.path.join(BACKUPS, old))
        tmp = SCHEDULE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, SCHEDULE)
        return self._json(200, {"ok": True})

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), fmt % args))


def lan_ips():
    ips = set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET):
            ip = info[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except OSError:
        pass
    return sorted(ips) or ["<ip-van-deze-pc>"]


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print("HRM rooster-server draait. Sluit dit venster om te stoppen.\n")
    for ip in lan_ips():
        print(f"  Tv:        http://{ip}:{PORT}/")
        print(f"  Dashboard: http://{ip}:{PORT}/admin.html\n")
    print(f"  Op deze pc: http://localhost:{PORT}/admin.html")
    print("  Pincode:   " + ("ingesteld (pin.txt)" if read_pin() else "geen (maak pin.txt aan om er een te zetten)"))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
