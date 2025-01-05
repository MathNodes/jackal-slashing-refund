#!/bin/env/python3

'''
Get ujkl delegator address and amount, comma separted
./canined query staking delegations-to jklvaloper1wq34uv9rhkv7tjk0pu263cfyshhgr9frn2ztds --output json | jq -r '.delegation_responses[] | "\(.delegation.delegator_address),\(.delegation.shares)"' | cut -d "." -f 1
'''

import pexpect
from time import sleep

DELEGATOR_FILE = "/home/jackal/Logs/delegators"
WALLET_ADDRESS = "jkl1wq34uv9rhkv7tjk0pu263cfyshhgr9frxezz4f"
KEYRING_DIR = "/home/jackal/.canine"
CANINED = "/home/jackal/canined"
SATOSHI = 1000000
SLASHING_PCT = 0.0001
DENOM = "ujkl"
CHAIN_ID = "jackal-1"
keyring_passphrase = "Z!NNFj9^se*Ur7JNAFT*o55Q^iqjAa*kSPbUi64rPXc8PRvvaZa3SbE"

class SlashingRefund():
    
    def __init__(self):
        self.__transfer_cmd = '%s tx bank send --gas auto --gas-prices 0.2ujkl --gas-adjustment 2.0 --yes %s %s %s%s --chain-id %s' 
        
        
        
    def read_delegator_file(self, file):
        delegators = []
        delegator_info = {}
        with open(file, "r") as delegator_file:
            delegator_data = delegator_file.readlines()
            
        for d in delegator_data:
            delegator_info['address'], delegator_info['amount'] = d.split(',')
            delegator_info['amount'] = int(delegator_info['amount']) 
            delegators.append(delegator_info)
            delegator_info = {}
            
        return delegators
    
    
    def refund_slashing_amount(self, delegators):
        for d in delegators:
            address = d['address']
            amt     = float(float(d['amount'])*SLASHING_PCT)
            
            print(f"{address},{float(int(d['amount'])/SATOSHI)},{float((int(amt)/SATOSHI)*1.5)}")
            transfer_cmd = self.__transfer_cmd % (CANINED, 
                                                  WALLET_ADDRESS,
                                                  address,
                                                  int(amt)*1.5,
                                                  DENOM,
                                                  CHAIN_ID)
            
            print(transfer_cmd)
            #answer = input("Process command (Y/n): ")
            answer = "Y" 
            if answer.upper() == "Y":
                try: 
                    child = pexpect.spawn(transfer_cmd)
                    
                    child.expect("Enter .*")
                    child.sendline(keyring_passphrase)
                    print(child.before)
                    print(child.after)
                    child.expect(pexpect.EOF)    
                    print(child.before.decode('utf-8'))
                    print(child.after)

                except Exception as e:
                    print(str(e))
                    
                sleep(30)
            
            
if __name__ == "__main__":
    sr = SlashingRefund()
    sr.refund_slashing_amount(sr.read_delegator_file(DELEGATOR_FILE))