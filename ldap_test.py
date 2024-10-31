from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, Tls
import ssl
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv(dotenv_path=r'C:\Projekte\AUTDOC\.env')

# Variablen aus der .env-Datei lesen
ldap_server = "ldap://ldap.fh-giessen.de"  # Verwende ldap:// für unverschlüsselte Verbindung
ldap_user_dn = os.getenv("LDAP_USER_DN")
ldap_password = os.getenv("LDAP_PASSWORD")
search_base = "dc=fh-giessen-friedberg,dc=de"  # Basis-DN für die Suche
search_filter = "(cn=Katharina Sieben)"  # Filter nur für den gewünschten CN

# Debug-Ausgabe
print("Verbindung zum LDAP-Server herstellen mit:")
print("LDAP_USER_DN:", ldap_user_dn)
print("LDAP_PASSWORD:", "******")  # Passwort aus Sicherheitsgründen nicht anzeigen

# StartTLS hinzufügen für Verschlüsselung auf ldap://
tls_config = Tls(validate=ssl.CERT_NONE)

# Verbindung herstellen
try:
    server = Server(ldap_server, get_info=ALL, tls=tls_config)
    conn = Connection(server, user=ldap_user_dn, password=ldap_password)
    conn.open()
    conn.start_tls()  # StartTLS einschalten für verschlüsselte Verbindung

    conn.bind()  # Verbindung authentifizieren

    # LDAP-Abfrage für die öffentlichen Attribute ausführen
    conn.search(
        search_base,
        search_filter,
        attributes=[
            'cn', 'sn', 'givenName', 'displayname', 'mail', 'uid', 'uidNumber', 'gidNumber', 'ou', 'objectclass', 
            'loginShell', 'homeDirectory', 'shadowExpire', 'shadowInactive', 'shadowLastChange', 
            'shadowMax', 'shadowMin', 'shadowWarning'
        ]
    )

    # Ergebnisse anzeigen
    for entry in conn.entries:
        print(entry)

except Exception as e:
    print("Fehler beim Verbinden oder bei der Abfrage:", e)

finally:
    # Verbindung schließen
    if 'conn' in locals() and conn.bound:
        conn.unbind()
