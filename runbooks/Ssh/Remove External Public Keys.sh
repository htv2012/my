#1/usr/bin/env bash
cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys.bak
grep haiv ~/.ssh/authorized_keys.bak > ~/.ssh/authorized_keys
echo Cleaned up ~/.ssh/authorized_keys file
