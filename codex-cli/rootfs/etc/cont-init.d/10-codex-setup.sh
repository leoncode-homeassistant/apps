#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -euo pipefail

if ! bashio::config.has_value 'authorized_keys'; then
    bashio::exit.nok 'At least one public SSH key is required.'
fi

install -d -m 0700 /data/ssh
install -d -m 0700 /data/codex
install -d -m 0755 /workspace

rm -f /data/ssh/authorized_keys
while IFS= read -r key; do
    printf '%s\n' "${key}" >> /data/ssh/authorized_keys
done <<< "$(bashio::config 'authorized_keys')"
chmod 0600 /data/ssh/authorized_keys

if [[ ! -e /root/.ssh ]]; then
    ln -s /data/ssh /root/.ssh
fi
if [[ ! -e /root/.codex ]]; then
    ln -s /data/codex /root/.codex
fi

ln -sfn /homeassistant /config
ln -sfn /homeassistant /workspace/homeassistant
ln -sfn /backup /workspace/backup
ln -sfn /share /workspace/share

password="$(head -c 48 /dev/urandom | base64 | tr -d '\n')"
printf 'root:%s\n' "${password}" | chpasswd
unset password

mcp_url="$(bashio::config 'ha_mcp_url')"
python3 /usr/local/bin/configure-codex.py "${mcp_url}"

tcp_forwarding='no'
if bashio::config.true 'allow_tcp_forwarding'; then
    tcp_forwarding='yes'
fi

sed "s/@ALLOW_TCP_FORWARDING@/${tcp_forwarding}/" \
    /etc/ssh/sshd_config.template > /etc/ssh/sshd_config
chmod 0600 /etc/ssh/sshd_config

bashio::log.info 'The Codex workspace is ready at /workspace.'
if [[ -n "${mcp_url}" ]]; then
    bashio::log.info 'HA-MCP is enabled in the Codex configuration.'
else
    bashio::log.warning 'HA-MCP is not configured yet.'
fi
