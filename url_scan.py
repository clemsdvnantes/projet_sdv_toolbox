import csv
import sys
import subprocess

def find_web_ports(csv_file):
    web_ports = []
    try:
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                port = row[0]
                service = row[2]
                if 'http' in service:  # Checking for HTTP/HTTPS services
                    web_ports.append(port)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV Nmap : {e}")
    
    return web_ports

def scan_urls_with_gobuster(target, port):
    protocol = "https" if port == "443" else "http"
    url_base = f"{protocol}://{target}:{port}"
    output_file = f'gobuster_scan_{target}_{port}.csv'
    
    print(f"Exécution de Gobuster sur : {url_base}")
    
    try:
        # Commande Gobuster
        gobuster_command = [
            'gobuster', 'dir',
            '-u', url_base,
            '-w', '/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt',
            '-o', output_file,
            '-q'
        ]
        
        subprocess.run(gobuster_command)
        print(f"Le fichier CSV des résultats Gobuster a été créé : {output_file}")
        
    except Exception as e:
        print(f"Erreur lors de l'exécution de Gobuster : {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 url_scan.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    nmap_csv = f'nmap_scan_{target}.csv'
    
    print(f"Analyse du fichier Nmap pour les ports web : {nmap_csv}")
    web_ports = find_web_ports(nmap_csv)
    
    if not web_ports:
        print("Aucun port web détecté.")
        sys.exit(0)
    
    print(f"Ports web détectés : {web_ports}")
    
    for port in web_ports:
        scan_urls_with_gobuster(target, port)

if __name__ == "__main__":
    main()
