#!/usr/bin/env bash
# Use this script to when creating a new AWS EC2 instance
sudo yum update -y
sudo yum install -y python3 git tmux
whoami > /tmp/who