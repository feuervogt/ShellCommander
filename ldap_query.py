from ldap3 import Server, Connection, ALL

def run_ldap_query():
    """
    Führt eine LDAP-Abfrage durch und gibt die Ergebnisse in der Konsole aus.
    """
    results = [] # Liste zum Speichern der Abfrageergebnisse
    try:
        # Verbindungsdaten
        server = Server('ldap://deenswts03', get_info=ALL)  # Domain Controller
        conn = Connection(server, user='DOMAIN\\user', password='hier kommt was rein', auto_bind=True)
        
        # Benutzerabfrage
        conn.search('dc=example,dc=com', '(objectclass=person)', attributes=['cn', 'givenName', 'sn', 'mail'])
        
        # Ergebnisse anzeigen
        for entry in conn.entries:
            print(entry)
    except Exception as e:
        print(f"Fehler bei der LDAP-Abfrage: {e}")

    return results # Gibt die Liste der Ergebnisse zurück
