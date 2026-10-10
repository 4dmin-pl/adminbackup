# AdminBackup — kopie zapasowe A.D.M.I.N

AdminBackup to [UrBackup](https://www.urbackup.org) (kopie plików i obrazów dysków przez sieć) z marką
**A.D.M.I.N (4dmin.pl), by Karol Wojewski**. Licencja: AGPL-3.0-or-later, tak jak oryginał.

## Pobieranie
| Co | Link |
|---|---|
| Klient Windows (MSI, x64) | https://github.com/4dmin-pl/adminbackup/releases/latest/download/AdminBackup-x64.msi |
| Serwer (Docker, amd64/arm64) | `ghcr.io/4dmin-pl/adminbackup-server:2.5` |

Instalacja klienta bez pytań (np. przez GPO/RMM):
```
msiexec /i AdminBackup-x64.msi /qn
```

### Konfiguracja bez udziału klienta
- **Serwer w tej samej sieci LAN** — nic nie trzeba: klient sam znajduje serwer i jest dodawany automatycznie.
- **Serwer zdalny (internet)** — połóż plik `adminbackup.ini` w tym samym folderze co `AdminBackup-x64.msi`
  (wzór: `adminbackup-wzor.ini` w każdym wydaniu). Instalator skopiuje go jako `initial_settings.cfg`, usługa przy
  pierwszym starcie wczyta ustawienia i **usunie plik** (razem z kluczem). Dane (nazwa komputera + klucz) z panelu
  serwera klienta: *Status → Dodaj nowego klienta internetowego*. Plik działa tylko przy pierwszej instalacji
  (gdy klient nie ma jeszcze ustawień). Z archiwum ZIP najpierw wypakuj oba pliki — uruchomienie MSI z podglądu ZIP
  nie widzi pliku obok.

Serwer:
```
docker run -d --name adminbackup-server --restart unless-stopped \
  -v /srv/adminbackup/db:/var/urbackup -v /srv/adminbackup/backups:/backups \
  --network host ghcr.io/4dmin-pl/adminbackup-server:2.5
```
Panel: `http://<serwer>:55414`.

> **Ważne:** w panelu serwera wyłącz *Ustawienia → Klient → Automatycznie aktualizuj klientów*.
> Aktualizacje z serwera to oficjalne instalatory UrBackup — nadpisałyby markę AdminBackup.
> Nowe wersje klienta wydajemy tutaj (GitHub Releases).

## Jak to jest zbudowane
- **Klient** (`.github/workflows/klient.yml`): oficjalny MSI UrBackup (weryfikowany SHA-256) → rozpakowanie →
  `brand.py klient` (ikony statusu, logo, tłumaczenia „UrBackup”→„AdminBackup”, info.txt) → `installer/adminbackup.wxs`
  (WiX 5, polski instalator, katalog `Program Files\AdminBackup`). **Binarki nie są zmieniane** — ich oryginalne
  podpisy cyfrowe zostają ważne. Wewnętrzne nazwy plików i usługi (`UrBackupClientBackend`) zostają, bo program
  odwołuje się do nich na sztywno.
- **Serwer** (`serwer/Dockerfile`, `.github/workflows/serwer.yml`): oficjalny obraz `uroni/urbackup-server:2.5.x`
  (przypięty digestem) + marka w panelu WWW (tytuł, logo, nazwa, stopka). Strona „O programie” z licencją zostaje oryginalna.
- `installer/adminbackup.wxs` powstał z `urbackup_frontend_wx/urbackup.wxs` (konwersja WiX 3→5, nazwy, nowe GUID-y,
  biblioteki VC++ obok programu zamiast niepublicznego modułu scalającego, poprawka `lang\sv`→`lang\sb`).
- Grafiki: `grafika/*.svg` (wspólne z AdminDesk) → `brand.py`.

Wydanie: tag `vX.Y.Z-N` (np. `v2.5.32-1`) → GitHub Release z MSI i `SHA256SUMS.txt`.

## Źródła i licencja
Oryginalny kod: https://github.com/uroni/urbackup_backend, https://github.com/uroni/urbackup_frontend_wx
(© Martin Raiber / Infscape UG, AGPL-3.0-or-later). Zmiany marki: to repozytorium (AGPL-3.0-or-later, plik `LICENSE`).
