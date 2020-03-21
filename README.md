# iorestoacasa_monitoring

prometheus + grafana = ❤️

## procedura per aggiungere un server

1. inserire una nuova riga nel foglio di calcolo condiviso, ed assicurarsi di inserire tutte le informazioni richieste
2. assicurarsi che Jitsi funzioni (facendo una videochiamata) e che il certificato HTTPS sia valido
3. assicurarsi che le metriche siano esposte su una porta HTTP (non HTTPS) e su /metrics
4. aggiungere le informazioni del nuovo nodo in `targets.json`
5. far partire questo docker-compose di monitoraggio in locale ed assicurarsi che nel file `hosts.json` appaia il nuovo server
6. fare commit e push del repository `iorestoacasa_monitoring`
7. creare un utente grafana con solo username, no email e no invio email, permesso "Viewer", e mandare alla persona in privato il link di invito
8. chiedere a @tapion di fare il deploy sul server del repository `iorestoacasa_monitoring` e `iorestoacasa.work`
