# Home_server

## Ansible

```bash
ansible-playbook -i ansible/inventories/home_server/hosts ansible/deploy.yml
```

## Rsync

```bash
rsync -av ~/git/Home_server/server/ hoel@192.168.1.34:/opt/server && \
ssh hoel@192.168.1.34 sudo systemctl restart server
```

## Rsync & Flash hub

```bash
rsync -av ~/git/nRF24_hub/* hoel@192.168.1.34:nRF24_hub && \
ssh hoel@192.168.1.34 sudo systemctl stop server && \
ssh hoel@192.168.1.34 /home/hoel/.platformio/penv/bin/platformio \
run -d ~/nRF24_hub --target upload --upload-port /dev/ttyAMA0 && \
ssh hoel@192.168.1.34 sudo systemctl start server
```

## Test fio & shield

```bash
curl -sSf 192.168.1.34:6000/fio
curl -sSf 192.168.1.34:6000/shield
```
