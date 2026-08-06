#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -euo pipefail

install -d -m 0700 /data/ssh-host-keys

for type in rsa ecdsa ed25519; do
    key="/data/ssh-host-keys/ssh_host_${type}_key"
    if [[ ! -f "${key}" ]]; then
        ssh-keygen -q -N '' -t "${type}" -f "${key}"
    fi
    ln -sfn "${key}" "/etc/ssh/ssh_host_${type}_key"
    ln -sfn "${key}.pub" "/etc/ssh/ssh_host_${type}_key.pub"
done
