#!/usr/bin/env python3
"""
Script to extract the env vars from LFR
Require: vanquish_LFR_template.json downloaded from
https://gitswarm.f5net.com/velocity-test/ajobs-templates/-/blob/sk_lf/Appliance/vanquish_LFR_template.json
to the current dir
"""
import json


def extract(d, refkey):
    if isinstance(d, dict):
        for key, value in d.items():
            if key == refkey:
                yield value
            yield from extract(value, refkey)
    elif isinstance(d, list):
        for value in d:
            yield from extract(value, refkey)



with open("vanquish_LFR_template.json") as stream:
    lfr = json.load(stream)

env_vars = []
for env in extract(lfr, refkey="env"):
    env_vars.extend(env)

env_vars = list(set(env_vars))
env_vars.sort(key=str.lower)
print("\n".join(env_vars))

