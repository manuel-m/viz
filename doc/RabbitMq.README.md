```bash
#check rabbitmq connection
tcpdump -i any -n -vv -s 0 -c 100 -W 100 -A port 5672
```