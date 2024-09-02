# py-monitor-docker
Send current process CPU usage via Telegram bot

# Installation
```sh 
git clone https://github.com/Gotoro/py-monitor-docker.git
cd py-monitor-docker
```
Put your @BotFather token into `secrets.txt`
```sh
docker build -t python-monitoring .
docker run --detach --name "py-monitor-container" -v /proc:/host-proc python-monitoring:latest
```
Use `/status` in bot to see the CPU usage of top 5 processes.

![image](https://github.com/user-attachments/assets/6cb31636-1c59-409b-8736-aa14457bcca5)
