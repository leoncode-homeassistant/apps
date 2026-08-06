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
codex_provider="$(bashio::config 'codex_provider')"
codex_provider_name="$(bashio::config 'codex_provider_name')"
codex_base_url="$(bashio::config 'codex_base_url')"
codex_model="$(bashio::config 'codex_model')"
python3 /usr/local/bin/configure-codex.py \
    "${mcp_url}" \
    "${codex_provider}" \
    "${codex_provider_name}" \
    "${codex_base_url}" \
    "${codex_model}"

if bashio::config.has_value 'codex_api_key'; then
    codex_api_key="$(bashio::config 'codex_api_key')"
    printf '%s' "${codex_api_key}" | CODEX_HOME=/data/codex codex login --with-api-key
    unset codex_api_key
    bashio::log.info 'Codex authentication was updated from the app configuration.'
else
    bashio::log.info 'No API key is stored in the app configuration; authenticate through Codex desktop or the CLI.'
fi

tcp_forwarding='no'
if bashio::config.true 'allow_tcp_forwarding'; then
    tcp_forwarding='yes'
fi

sed "s/@ALLOW_TCP_FORWARDING@/${tcp_forwarding}/" \
    /etc/ssh/sshd_config.template > /etc/ssh/sshd_config
chmod 0600 /etc/ssh/sshd_config

bashio::log.info 'The Codex workspace is ready at /workspace.'
if [[ "${codex_provider}" == 'custom' ]]; then
    bashio::log.info "Codex model provider: ${codex_provider_name} (${codex_base_url}); model: ${codex_model}."
else
    bashio::log.info "Codex model provider: OpenAI; model: ${codex_model}."
fi
if [[ -n "${mcp_url}" ]]; then
    bashio::log.info 'HA-MCP is enabled in the Codex configuration.'
else
    bashio::log.warning 'HA-MCP is not configured yet.'
fi
