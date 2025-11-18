# apertum-tools
Tools for querying the Apertum blockchain and NFT structures

# DID Information
did_info.py will query both the Apertum RPC and Explorer to pull relevent information.  The script will display the parent (sponsor) and the children (customers) of the supplied DID, as well as additional information including DOD owner wallet address, APTM balance and other NFTs associated with the DID

did_info.py is a python script, it must exist in the same directory as the did_abi.json file

# INSTALLATION EXAMPLE (Fedora)
dnf install python3
pip install web3
pip install pycurl
pip install jsonpickle


USAGE: ./did_info.py [DID Number]


