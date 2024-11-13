# systemd


```
[Service]
CPUQuota=30%
# default is 1024
CPUShares=512

MemoryLimit=1G
```

```
# show all cpu shares
systemctl show --all --property=CPUShares --no-pager
systemd-cgls --cpu

# scoped subprocess
systemd-run --scope -p CPUQuota=20% /path/to/commands
```


```
#!/bin/bash

start_time=$(date +%s.%N)  
./mybinary            
end_time=$(date +%s.%N)    

elapsed=$(echo "$end_time - $start_time" | bc)  # Calcul du temps écoulé
echo "Temps d'exécution : $elapsed secondes"
```
