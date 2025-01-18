#!/bin/bash
VALIDATOR_ADDRESS="jklvaloper1wq34uv9rhkv7tjk0pu263cfyshhgr9frn2ztds"
LIMIT=1000

~/canined query staking delegations-to $VALIDATOR_ADDRESS --limit $LIMIT --output json | jq -r '.delegation_responses[] | "\(.delegation.delegator_address),\(.delegation.shares)"' | cut -d "." -f 1