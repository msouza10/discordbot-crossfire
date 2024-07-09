#!/bin/bash

# Função para logar mensagens
log() {
    local MESSAGE="$1"
    echo "$(date +"%Y-%m-%d %T") - $MESSAGE"
}

# Função para verificar o sucesso de um comando
check_success() {
    if [ $? -ne 0 ]; then
        log "Erro na execução do último comando. Abortando."
        exit 1
    fi
}

log "Início da execução do script."

# Cria o diretório /var/bots se não existir
if [ ! -d /var/bots ]; then
    log "Criando diretório /var/bots."
    sudo mkdir /var/bots
    check_success
fi

# Navega para o diretório /var/bots
cd /var/bots
check_success

# Clona o repositório do bot do GitHub
if [ ! -d discordbot-crossfire ]; then
    log "Clonando repositório do bot."
    git clone https://github.com/msouza10/discordbot-crossfire.git
    check_success
else
    log "O repositório já existe em /var/bots."
fi

# Instala dependências necessárias
log "Atualizando pacotes e instalando dependências."
sudo apt update && sudo apt install -y python3-pip git
check_success

# Instala as dependências Python do projeto
cd /var/bots/discordbot-crossfire
check_success
log "Instalando dependências Python."
pip3 install -r requirements.txt
check_success

# Instala o Google Chrome se não estiver instalado
if ! command -v google-chrome &> /dev/null; then
    log "Instalando Google Chrome."
    sudo apt install -y wget
    check_success
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -P /var/bots
    check_success
    sudo dpkg -i /var/bots/google-chrome-stable_current_amd64.deb
    check_success
    sudo apt-get install -f -y
    check_success
    rm /var/bots/google-chrome-stable_current_amd64.deb
else
    log "Google Chrome já está instalado."
fi

# Cria o arquivo de serviço systemd
SERVICE_FILE="/etc/systemd/system/discordbot.service"

if [ ! -f "$SERVICE_FILE" ]; then
    log "Criando arquivo de serviço systemd."
    sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=Discord Bot
After=network.target

[Service]
User=nobody
WorkingDirectory=/var/bots/discordbot-crossfire
ExecStart=/usr/bin/python3 /var/bots/discordbot-crossfire/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    check_success
else
    log "O arquivo de serviço já existe em /etc/systemd/system."
fi

# Recarrega o systemd para aplicar o novo serviço e inicia o serviço do bot
log "Recarregando systemd e iniciando serviço do bot."
sudo systemctl daemon-reload
check_success
sudo systemctl enable discordbot.service
check_success
sudo systemctl start discordbot.service
check_success

# Verifica o status do serviço para garantir que está funcionando
log "Verificando status do serviço do bot."
sudo systemctl status discordbot.service

log "Execução do script finalizada."
