# Ssh into TrueNAS

------------------------------------------------------------------------

## Setup

### Enable Ssh Service

1. Go to Services/SSH
2. Select Edit (the pencil icon)
3. Check "Allow password authentication"

### Configure User Access

1. Go to Accounts/Users
2. Locate the user and edit
3. Optional: paste the local's public key for public key authentication

### Optional: Setup local ssh

1. Edit ~/.ssh/config
2. Add

        Host truenas
            HostName IP-ADDRESS
            User USER-ALIAS

------------------------------------------------------------------------

## Usage

    ssh truenas

