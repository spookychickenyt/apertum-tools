# Apertum Tools
Tools for querying the Apertum blockchain and NFT structures.  

This is a work in progress, new tools will be uploaded soon.  

  
# DID Information
did_info.py will query both the Apertum RPC and Explorer to pull relevent information.  
The script will display the parent (sponsor) and the children (customers) of the supplied DID, as well as additional information including DID owner wallet address, APTM balance and other NFTs associated with the DID.  
  
did_info.py is a python script, it must exist in the same directory as both the did_abi.json and miner_abi.json files  
  
  
# Prerequisits (Fedora)
dnf install python3  
pip install web3  
pip install pycurl  
pip install jsonpickle  
  
  
# usage 
./did_info.py [DID Number]


