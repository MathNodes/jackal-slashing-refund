#!/bin/bash
VALIDATOR_ADDRESS="jklvaloper1wq34uv9rhkv7tjk0pu263cfyshhgr9frn2ztds"

~/canined query staking delegations-to $VALIDATOR_ADDRESS --output json | jq -r '.delegation_responses[] | "\(.delegation.delegator_address),\(.delegation.shares)"' | cut -d "." -f 1