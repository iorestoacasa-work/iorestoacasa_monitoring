# iorestoacasa_monitoring

prometheus + grafana = ❤️

## procedura per aggiungere un server MM

1. chiedi a @tapion

## procedura per aggiungere un server Jitsi

1. contattare in privato il soggetto e chiedere le seguenti informazioni:
```
ho bisogno di queste informazioni:
- URL del server jitsi
- URL e porta dove sono esposte le metriche
- nome da inserire nei crediti
- URL da inserire nei crediti
- tipo di contributo: azienda / privato / associazione / istituzione
- numero di core
- RAM
- banda disponibile
```
2. inserire una nuova riga nel foglio di calcolo condiviso, ed assicurarsi di inserire tutte le informazioni richieste
3. assicurarsi che Jitsi funzioni (facendo una videochiamata) e che il certificato HTTPS sia valido
4. assicurarsi che le metriche siano esposte su una porta HTTP (non HTTPS) e su /metrics
5. aggiungere le informazioni del nuovo nodo in `jitsi_targets.yml`
6. far partire questo docker-compose di monitoraggio in locale ed assicurarsi che nel file `hosts.json` appaia il nuovo server
7. fare commit e push del repository `iorestoacasa_monitoring`
8. creare un utente grafana con solo username, no email e no invio email, permesso "Viewer", e mandare alla persona in privato il link di invito
9. chiedere a @tapion di fare il deploy sul server del repository `iorestoacasa_monitoring` e `iorestoacasa.work`
