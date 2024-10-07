
DEVPI_PORT=4040

sudo useradd -m -s /bin/bash devpi
sudo -iu devpi python3 -m venv venv

# install server
sudo -iu devpi bash -c "source venv/bin/activate\
&& pip install devpi-server devpi-web devpi-client\
&& mkdir -p ./devpi-server\
&& devpi-gen-config --port $DEVPI_PORT --serverdir $(pwd)/devpi-server --host 0.0.0.0\
&& devpi-init --serverdir ./devpi-server"


sudo cat > /etc/systemd/system/devpi.service <<EOF
[Unit]
Description=Devpi Server
Requires=network-online.target
After=network-online.target

[Service]
Restart=on-success
ExecStart=/home/devpi/venv/bin/devpi-server --port $DEVPI_PORT --serverdir /home/devpi/devpi-server --host 0.0.0.0
User=devpi

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable devpi.service
sudo systemctl start devpi.service

