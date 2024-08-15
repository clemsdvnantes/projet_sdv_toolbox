import nmap
import csv
import sys

def scan_ports(target):
    nm = nmap.PortScanner()
    nm.scan(target, '1-1024')
    
    output_file = f'nmap_scan_{target}.csv'
    
    try:
        with open(output_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(['Port', 'State', 'Service'])
            
            for host in nm.all_hosts():
                print(f'Scanning host: {host}')
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
                    for port in lport:
                        state = nm[host][proto][port]['state']
                        service = nm[host][proto][port]['name']
                        writer.writerow([port, state, service])
                        print(f'Port {port} is {state} ({service})')

        print(f"Le fichier CSV a été créé avec succès : {output_file}")
    except Exception as e:
        print(f"Erreur lors de la création du fichier CSV : {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 nmap_scan.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    print(f"Lancement du scan Nmap pour la cible : {target}")
    scan_ports(target)
