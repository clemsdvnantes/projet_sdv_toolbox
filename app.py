import subprocess

def run_script(script_name, *args):
    """Exécute un script externe avec les arguments donnés."""
    command = ['python3', script_name] + list(args)
    try:
        subprocess.run(command, check=True)
        print(f"Le script {script_name} a été exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {script_name} : {e}")

def main():
    target = input("Veuillez entrer l'adresse IP ou le nom DNS de la cible: ")
    
    # Exécuter le script Nmap
    run_script('nmap_scan.py', target)
    
    # Exécuter le script URL Scan
    run_script('url_scan.py', target)
    
    # Exécuter WPScan
    run_script('wordpress_scan.py', target)
    
    # Résumer les résultats de WPScan
    wpscan_json = f"wpscan_{target.replace('/', '_').replace(':', '_')}.json"
    summary_csv = f"wpscan_{target.replace('/', '_').replace(':', '_')}_summary.csv"
    run_script('summarize_wpscan.py', wpscan_json, summary_csv)
    
    # Exécuter le scan de vulnérabilités avec Wapiti
    run_script('vuln_scan.py', target)
    
    # Résumer les résultats de Wapiti
    wapiti_json = f"wapiti_scan_{target.replace('/', '_').replace(':', '_')}.json"
    wapiti_summary_csv = f"wapiti_scan_{target.replace('/', '_').replace(':', '_')}_summary.csv"
    run_script('summarize_wapiti.py', wapiti_json, wapiti_summary_csv)

if __name__ == "__main__":
    main()
