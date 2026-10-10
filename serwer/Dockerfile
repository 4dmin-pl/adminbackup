# AdminBackup Server = oficjalny obraz UrBackup Server 2.5.x (przypięty digestem) + marka A.D.M.I.N w panelu WWW.
# Zmieniamy tylko „ramę” panelu (tytuł, logo, nazwa, stopka). Strona „O programie” z licencją AGPL zostaje oryginalna.
FROM uroni/urbackup-server:2.5.x@sha256:fd218c45192fad0d7df7989da2c991264eec0a37a85e33499db419b203e9745f

COPY www/ /tmp/marka/

# entrypoint.sh przy starcie kopiuje /web-backup/* -> /usr/share/urbackup, więc marka musi być w obu miejscach
RUN set -e; for d in /usr/share/urbackup/www /web-backup/www; do \
      cp /tmp/marka/urbackup.png "$d/images/urbackup.png"; \
      cp /tmp/marka/favicon.ico "$d/favicon.ico"; \
      cp /tmp/marka/favicon.ico "$d/images/favicon.ico"; \
      sed -i \
        -e 's|<title>UrBackup - Keeps your data safe</title>|<title>AdminBackup - kopie zapasowe A.D.M.I.N</title>|' \
        -e 's|alt="UrBackup" style="float: left; position: relative; top: -10px;">UrBackup</span>|alt="AdminBackup" style="float: left; position: relative; top: -10px;">AdminBackup</span>|' \
        -e 's|<a href="http://www.urbackup.org" target="_new">www.urbackup.org</a>|<a href="https://4dmin.pl" target="_new">4dmin.pl</a> (oparte na UrBackup, AGPLv3+)|' \
        "$d/index.htm"; \
      grep -q '<title>AdminBackup' "$d/index.htm"; grep -q '>AdminBackup</span>' "$d/index.htm"; grep -q '4dmin.pl</a>' "$d/index.htm"; \
    done; rm -rf /tmp/marka

LABEL org.opencontainers.image.title="AdminBackup Server" \
      org.opencontainers.image.vendor="A.D.M.I.N (4dmin.pl)" \
      org.opencontainers.image.source="https://github.com/4dmin-pl/adminbackup" \
      org.opencontainers.image.licenses="AGPL-3.0-or-later"
