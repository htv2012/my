#!/bin/sh

PUBKEY=${1:-~/.ssh/id_rsa.pub}
echo "
users:
  - default
  - name: ubuntu
    sudo: ALL=(ALL) NOPASSWD:ALL
    ssh_authorized_keys:
    - $(cat $PUBKEY)
" > cloud-init.yaml

bat cloud-init.yaml
