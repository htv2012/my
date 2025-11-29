#!/usr/bin/env bash


# Setup
# =====
#
# Create SSH Key Pair
# -------------------
#
# 1. Go to System > SSH Keypairs
# 2. Add
#     - Name: Ssh to MacbookAir
#     - Generate
# 3. Download public key
# 4. Add that public key to ~/.ssh/authorized_keys
# 
# Create Task
# -----------
# 
# 1. Login to TrueNAS web
# 2. Go to Tasks > Rsync Tasks
# 3. Create a new task

cd
echo ""

dest=truenas:/mnt/pool1/work/macbookair
for src in my JoplinBackup Projects
do
    echo ""
    echo ----------------------------------------
    echo $src
    echo ----------------------------------------
    rsync -av --delete --exclude '.git/' --exclude '.ruff_cache' $src $dest
done

