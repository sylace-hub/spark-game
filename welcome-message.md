Pour modifier le message d'accuiel d'Amazon :
```console
$ nano /etc/motd
```

## /etc/ssh/sshrc
Ce petit utilitaire va ajouter une légère surcouche à ssh pour qu'il exécute en script à la connexion à n'importe quel serveur. Il se comporte exactement comme un ~/bashrc distant, ce qui est plutôt cool.

Récupérer l'IP connectée en SSH :
```console
$ echo $SSH_CLIENT
```

```console
$ nano /etc/ssh/sshrc
```

```bash
#!/bin/sh

SSH_CLIENT_RESPONSE=`echo $SSH_CLIENT`
SPLITTED_LINE=(${SSH_CLIENT_RESPONSE// / })
IP_ADDRESS=${SPLITTED_LINE[0]}

# Usage : ./associate-ips.sh 98.38.393.23 ips.txt
LINE=`grep -hr ${IP_ADDRESS} /etc/ip-table.txt`
SPLITTED_LINE=(${LINE// / })
echo Bonjour ${SPLITTED_LINE[@]:1:10} !
```

```console
$ chmod 755 /etc/ssh/sshrc
```

```console
$ /etc/ip-table.txt
97.273.383 MAHMOUD
98.38.393.23 MALIKA
77.153.149.37 HAMID BACHKOU
123.0.9.12 MICHEL
91.172.99.190 LAMRANI
```

```console
$ chmod 644 /etc/ip-table.txt
```
