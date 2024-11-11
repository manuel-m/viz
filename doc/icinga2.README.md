

https://icinga.com/docs/icinga-2/2.11/doc/02-installation/

**icinga2 check**
```

https://github.com/jpfluger/examples/blob/master/ubuntu-14.04/icinga2-server.md

# icinga service running 
systemctl status icinga2
journalctl -u icinga2 
icinga2 --version (r2.14.2-1)

# check conf errors
icinga2 daemon -C 

# activated features
icinga2 feature list

sudo -u nagios /usr/lib*/nagios/plugins/check_ping -4 -H 127.0.0.1 -c 5000,100% -w 3000,80%


# check if icinga2 web
curl -u root:<passwd> http://localhost:5665/v1/objects/hosts

# check icinga2 snmp command
/etc/icinga2/conf.d/commands.conf

```

/etc/snmp/snmpd.conf
```
# memory
view   systemonly  included   .1.3.6.1.4.1.2021.4
# cpu load
view   systemonly  included   .1.3.6.1.4.1.2021.10
# cpu
view   systemonly  included   .1.3.6.1.4.1.2021.11
```

/etc/icinga2/conf.d/snmp-server.conf
```
object Host "snmp-server" {
  import "generic-host"
  address = "127.0.0.1"
  vars.snmp_community = "public"  
  vars.os = "Linux"  
  check_command = "hostalive"
}

apply Service "snmp-cpu-load" {
  import "generic-service"
  check_command = "snmp"
  vars.snmp_oid = "1.3.6.1.4.1.2021.10.1.3.1" 
  vars.snmp_community = host.vars.snmp_community
  assign where host.name == "snmp-server"
}

apply Service "snmp-ram-usage" {
  import "generic-service"
  check_command = "snmp"

  vars.snmp_oid = "1.3.6.1.4.1.2021.4.6.0" 
  vars.snmp_community = host.vars.snmp_community

  assign where host.name == "snmp-server"
}
```

/etc/icinga2/conf.d/commands.conf  
v2
```
object CheckCommand "snmp" {
  import "plugin-check-command"
  command = [ PluginDir + "/check_snmp" ]

  arguments = {
    "-C" = "$snmp_community$"
    "-H" = "$address$"
    "-o" = "$snmp_oid$"
    "-P" = "$snmp_version$"
  }

  vars.snmp_community = "public"
  vars.snmp_version = "2c"
}
```


v3
```
object CheckCommand "snmpv3" {
    import "plugin-check-command"
    command = [ PluginDir + "/check_snmp" ]

    arguments = {
        "-H" = "$address$"
        "-P" = "$snmp_version$"
        "-v" = "3"
        "--login" = "$snmpv3_user$"
        "--protocol" = "$snmpv3_auth_protocol$"
        "--authpassword" = "$snmpv3_auth_password$"
        "--privprotocol" = "$snmpv3_priv_protocol$"
        "--privpassword" = "$snmpv3_priv_password$"
        "-l" = "$snmpv3_security_level$"
        "-o" = "$snmp_oid$"
    }

    vars.snmp_version = "3"
    vars.snmpv3_security_level = "authPriv"
}
```


postgresql
```
sudo -u postgres psql -c "CREATE DATABASE <icinga2db>;"
sudo -u postgres psql -c "CREATE USER <icinga2db> WITH PASSWORD '<passwd>';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE <icinga2db> TO <icinga2db>;"

sudo -u postgres psql -c "CREATE DATABASE <icingaweb2>;"
sudo -u postgres psql -c "CREATE USER <icingaweb2user> WITH PASSWORD '<passwd>';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE <icingaweb2> TO <icingaweb2user>;"
```

**Troubleshooting**

**snmp cpu optimisation**

high cpu load:
- snmpcachd
- update interval / services.conf
```
apply Service "snmp-cpu" {
    ...
    check_interval = 5m  
    retry_interval = 1m  
    ...
}
```
- dependency check
```
apply Dependency "ping-dependency" for (service => config in host.vars.services) to Service {
    parent_service_name = "ping"
    disable_checks = true
    assign where service.name != "ping"
}
```
- max cpu concurrency (/etc/icinga2/icinga2.conf)
```
max_concurrent_checks = 100
```
- snmp traps (snmptrapd to avoid polling) 
- group script as CheckCommand
```
#!/bin/bash
HOST=$1
COMMUNITY=$2
cpu=$(snmpget -v2c -c $COMMUNITY $HOST 1.3.6.1.4.1.2021.11.10.0)
mem=$(snmpget -v2c -c $COMMUNITY $HOST 1.3.6.1.4.1.2021.4.6.0)
echo "CPU Load: $cpu"
echo "Memory Usage: $mem"
```

**snmpcachd**

snmpcachd.conf
```
[global]
cache_time = 60  # cache time in seconds

[ept1]
host = <ip1>
community = <community>
oids = 1.3.6.1.2.1.1.3.0, 1.3.6.1.4.1.2021.11.10.0  

[ept2]
host = <ip2>
community = <community>
oids = 1.3.6.1.2.1.1.3.0, 1.3.6.1.4.1.2021.4.6.0  
```

/etc/icinga2/conf.d/commands.conf
```
object CheckCommand "snmp_cache_check" {
    import "plugin-check-command"
    command = [ PluginDir + "/check_snmp" ]

    arguments = {
        "-H" = "127.0.0.1"
        "-P" = "2c"
        "-C" = "public"
        "-o" = "$snmp_oid$"
    }

    vars.snmp_cache_host = "127.0.0.1"  
    vars.snmp_cache_community = "public"
}
```


/etc/icinga2/conf.d/hosts.conf
```
object Host "equipement1" {
    import "generic-host"
    address = "192.168.1.10"
    vars.snmp_cache_host = "127.0.0.1"
}
```

/etc/icinga2/conf.d/services.conf
```
apply Service "snmp-uptime-cached" {
    import "generic-service"
    check_command = "snmp_cache_check"
    vars.snmp_oid = "1.3.6.1.2.1.1.3.0"  
    assign where host.name == "eqpt1"
}

apply Service "snmp-cpu-cached" {
    import "generic-service"
    check_command = "snmp_cache_check"
    vars.snmp_oid = "1.3.6.1.4.1.2021.11.10.0"  
    assign where host.name == "eqpt1"
}
```

**group script as CheckCommand **

check_snmpcachd.sh 
```
#!/bin/bash

# Script pour interroger plusieurs OID depuis SNMP Cache Daemon (snmpcachd)
HOST="127.0.0.1"          
COMMUNITY="<community>"        
CACHE_TIME=60 

OIDS=(
    "1.3.6.1.2.1.1.3.0"  
    "1.3.6.1.4.1.2021.11.10.0"
    "1.3.6.1.4.1.2021.4.6.0"
)

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <OID_GROUP>"
    exit 3
fi

OID_GROUP=$1

# Fonction pour exécuter une requête SNMP sur un OID donné
function check_oid {
    local oid=$1
    snmpget -v2c -c $COMMUNITY $HOST $oid | awk -F': ' '{print $2}'
}

case $OID_GROUP in
    uptime)
        result=$(check_oid "1.3.6.1.2.1.1.3.0")
        echo "Uptime: $result"
        ;;
    cpu)
        result=$(check_oid "1.3.6.1.4.1.2021.11.10.0")
        echo "CPU Load: $result"
        ;;
    memory)
        result=$(check_oid "1.3.6.1.4.1.2021.4.6.0")
        echo "Memory Available: $result"
        ;;
    all)
        uptime=$(check_oid "1.3.6.1.2.1.1.3.0")
        cpu=$(check_oid "1.3.6.1.4.1.2021.11.10.0")
        memory=$(check_oid "1.3.6.1.4.1.2021.4.6.0")
        echo "Uptime: $uptime | CPU Load: $cpu | Memory Available: $memory"
        ;;
    *)
        echo "Unknown OID group: $OID_GROUP"
        exit 3
        ;;
esac
```

/etc/icinga2/conf.d/commands.conf
```
object CheckCommand "check_snmp_cache_group" {
    import "plugin-check-command"
    command = [ "/usr/local/bin/check_snmpcachd.sh" ]

    arguments = {
        "-g" = {
            value = "$oid_group$"
            description = "Group of OIDs to check (uptime, cpu, memory, or all)"
            required = true
        }
    }
    vars.oid_group = "all"  # all OIDs par défaut
}
```

/etc/icinga2/conf.d/services.conf

```
apply Service "snmp-uptime-cached" {
    import "generic-service"
    check_command = "check_snmp_cache_group"
    vars.oid_group = "uptime"  
    assign where host.name == "eqpt1"
}

apply Service "snmp-cpu-cached" {
    import "generic-service"
    check_command = "check_snmp_cache_group"
    vars.oid_group = "cpu"  
    assign where host.name == "eqpt1"
}

apply Service "snmp-memory-cached" {
    import "generic-service"
    check_command = "check_snmp_cache_group"
    vars.oid_group = "memory"  
    assign where host.name == "eqpt1"
}

apply Service "snmp-all-cached" {
    import "generic-service"
    check_command = "check_snmp_cache_group"
    vars.oid_group = "all"  
    assign where host.vars.snmp_cache == true
}
```

**group script as CheckCommand (with auth)**

check_snmpcachd_v3.s

```
#!/bin/bash

HOST="127.0.0.1"          
CACHE_TIME=60             

USERNAME="snmpuser"       
AUTH_PROTOCOL="SHA"       
AUTH_PASSWORD="auth_pass" 
PRIV_PROTOCOL="AES"       
PRIV_PASSWORD="priv_pass" 

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <OID_GROUP>"
    exit 3
fi

OID_GROUP=$1

function check_oid {
    local oid=$1
    snmpget -v3 -l authPriv -u $USERNAME -a $AUTH_PROTOCOL -A $AUTH_PASSWORD -x $PRIV_PROTOCOL -X $PRIV_PASSWORD -Ovq -c $HOST $oid
}

case $OID_GROUP in
    uptime)
        result=$(check_oid "1.3.6.1.2.1.1.3.0")
        echo "Uptime: $result"
        ;;
    cpu)
        result=$(check_oid "1.3.6.1.4.1.2021.11.10.0")
        echo "CPU Load: $result"
        ;;
    memory)
        result=$(check_oid "1.3.6.1.4.1.2021.4.6.0")
        echo "Memory Available: $result"
        ;;
    all)
        uptime=$(check_oid "1.3.6.1.2.1.1.3
```

/etc/icinga2/conf.d/commands.conf
```
object CheckCommand "check_snmp_cache_group_v3" {
    import "plugin-check-command"
    command = [ "/usr/local/bin/check_snmpcachd_v3.sh" ]

    arguments = {
        "-g" = {
            value = "$oid_group$"
            description = "Group of OIDs to check (uptime, cpu, memory, or all)"
            required = true
        }
    }

    vars.snmpv3_user = "snmpuser"       
    vars.snmpv3_auth_protocol = "SHA"   
    vars.snmpv3_auth_password = "auth_pass" 
    vars.snmpv3_priv_protocol = "AES"   
    vars.snmpv3_priv_password = "priv_pass" 
    vars.oid_group = "all" 
}
```

/etc/icinga2/conf.d/commands.conf
```
apply Service "snmp-uptime-cached-v3" {
    import "generic-service"
    check_command = "check_snmp_cache_group_v3"
    vars.oid_group = "uptime"  
    assign where host.name == "eqpt1"
}

apply Service "snmp-cpu-cached-v3" {
    import "generic-service"
    check_command = "check_snmp_cache_group_v3"
    vars.oid_group = "cpu"  
    assign where host.name == "eqpt1"
}

apply Service "snmp-memory-cached-v3" {
    import "generic-service"
    check_command = "check_snmp_cache_group_v3"
    vars.oid_group = "memory"  
    assign where host.name == "eqpt1"
}
```

/etc/icinga2/conf.d/commands.conf
```
object Host "equipement1" {
    import "generic-host"
    address = "<ip1>"
    vars.snmp_cache = true

    vars.snmpv3_user = "snmpuser"
    vars.snmpv3_auth_protocol = "SHA"
    vars.snmpv3_auth_password = "auth_pass"
    vars.snmpv3_priv_protocol = "AES"
    vars.snmpv3_priv_password = "priv_pass"
}
```