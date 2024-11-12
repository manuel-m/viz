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
