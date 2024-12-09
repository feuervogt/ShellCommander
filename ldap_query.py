from ldap3 import Server, Connection, ALL
import getpass

def run_ldap_query():
    """
    Führt eine LDAP-Abfrage durch und gibt die Ergebnisse in der Konsole aus.
    """
    results = []  # Liste zum Speichern der Abfrageergebnisse
    try:
        # Anmeldedaten während der Laufzeit abfragen
        server_address = input("Gib die Serveradresse (z. B. ldap://serveradresse-oder-ip) ein: ")
        domain_user = input("Gib den Benutzernamen im Format DOMAIN\\user ein: ")
        password = getpass.getpass("Gib das Passwort ein (wird nicht angezeigt): ")
        
        # Verbindungsdaten
        server = Server(server_address, get_info=ALL)  # Domain Controller
        conn = Connection(server, user=domain_user, password=password, auto_bind=True)
        
        # Benutzerabfrage
        base_dn = input("Gib den Base-DN ein (z. B. dc=example,dc=com): ")
        search_filter = input("Gib den Suchfilter ein (z. B. (objectclass=person)): ")
        attributes = input("Gib die anzuzeigenden Attribute als kommagetrennte Liste ein (z. B. cn,givenName,sn,mail): ")
        attribute_list = [attr.strip() for attr in attributes.split(',')]  # Attribute als Liste

        conn.search(base_dn, search_filter, attributes=attribute_list)
        
        # Ergebnisse anzeigen
        for entry in conn.entries:
            print(entry)
            results.append(entry)
            
    except Exception as e:
        print(f"Fehler bei der LDAP-Abfrage: {e}")

    return results  # Gibt die Liste der Ergebnisse zurück