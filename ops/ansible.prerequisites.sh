#!/bin/bash

if [ -z "$1" ]; then
  echo "User not specified:"
  echo "    Usage: $0 <USER>"
  exit 1
fi

USER=$1

    
cat <<EOF > /etc/apt/sources.list
deb http://deb.debian.org/debian/ bookworm main contrib non-free
deb-src http://deb.debian.org/debian/ bookworm main contrib non-free
deb http://deb.debian.org/debian-security/ bookworm-security main contrib non-free
deb-src http://deb.debian.org/debian-security/ bookworm-security main contrib non-free
deb http://deb.debian.org/debian/ bookworm-updates main contrib non-free
deb-src http://deb.debian.org/debian/ bookworm-updates main contrib non-free
EOF

apt update && \
apt install -y sudo python3-pip python3-venv qemu-guest-agent rsync

/sbin/usermod -aG sudo $USER

SUDOERS_FILE="/etc/sudoers.d/$USER"
echo "$USER ALL=(ALL) NOPASSWD:ALL" | sudo tee "$SUDOERS_FILE" > /dev/null
chmod 0440 "$SUDOERS_FILE"

mkdir -p /home/$USER/.ssh && chmod 700 /home/$USER/.ssh \
&& echo \
'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDE93KULnEWkHAt5adOdU3JIyIhDsmdpXyxmnqbdhyzpYfxFhFeSFb3UpF3A+SEzaf4AiZRN3NneHkrzAzYJBzJT3V4E4wcDcjX4GmLN9sVMq/o8vEEtQFjvP9tmlCjI9LKnPvk2W6mtcTprik9fHL/rHjoJw59dmjP8qx+ocyIwpIyt6tTfNjxe5l7/4ACuaBYgHMsQbzxKPsr9R+Tt+TDV/I6GB31vS6n6QfCLhBkCYz80tMpTJ0nMLynYZ6dVuV53KAe4d6uHVnvg3jtryqI5RIZowrr9mD0AsaiOS3kFSPIstzQSmosq8imBrkQj9hyymAKIfdfMhZ0wxk9t7R/ pcc@pcc-VirtualBox\n' \
>> /home/$USER/.ssh/authorized_keys \
&& echo \
'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCzrrWxf16V/sRMgutPsvEg4dHJYxjkSTIkydvJnElY4lAxTWC83Bs8D1+T+cf0hbOUR2wuRakigHGKwA0dkYQ28Z7Ui5YmvODcigYmP7D5I5zasWUUNYXRjYn0mxmk4vTC0H8sArjwQ8slO06I9MxVt/Hl+Rdp20UcVseiJYs2LA126YggKK2D6xxU4sekIFZE5rLxqx9HWyAbbZvknf+4kd+byni7gGEpVa5NNvoIQ+LB26PJoegBWnWttEBlFpuCVvGhFX3c9as/BFoh3Qfx12TgOQoTX9KwtDGDFH9602mQ4xj/dWv8/0k/9tkwgThwxb9/hNyrq+sqAG70Ol/J+ZiLB3xkapNSTpK7fjmWyWa6twEeDW2aGsInXqKVgvVve29xmbqSBTXQC2C9dPzH6vr0twLsaubjKN+9Jk0i1gdVlvH2VFg5cR7QCeSoh2m1MUFuEiIkmi/gvI3KCzNH7WvYhssi31qiyENG3TUbv7iKy8z9AyMIAwuDBd3MGfTg2OUnzevzObWh268pTv7u8zlJkSAAKJ6pzl4pZWJleVd6J9JkgxpMYrw0puAZ/BQ+d1LfAddtjttUNkcjYDBOY44UldzCCWroyU14USIpCRz/y5APlBSYmOg0gOYHh3302wFBPl2rNQN8htPp47X1aBuPRKIyLEzd8zBNzTMlRw==' \
>> /home/$USER/.ssh/authorized_keys \
&& chmod 600 /home/$USER/.ssh/authorized_keys \
&& chown -R $USER /home/$USER/.ssh \
&& su - $USER -c "ssh-keygen -t rsa -b 4096"

