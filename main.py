import asyncio
import json
from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Processed
from sb_on_demand.randomness import *
from datetime import datetime

NETWORK = "devnet"  # Change to "mainnet-beta" or "testnet" as needed

if NETWORK == "devnet":
    RPC_ENDPOINT = "https://api.devnet.solana.com"
elif NETWORK == "mainnet-beta":
    RPC_ENDPOINT = "https://api.mainnet-beta.solana.com"

connection = AsyncClient(RPC_ENDPOINT, commitment=Processed)

# Read wallet needed
payer = Keypair.from_base58_string("your_payer_keypair_base58_string_here")
randomness_account = Keypair.from_base58_string("your_randomness_account_keypair_base58_string_here")
authority_account = Keypair.from_base58_string("your_authority_account_keypair_base58_string_here")


async def main():
    await init(connection, randomness_account, payer, authority_account)
    await asyncio.sleep(10)

    await commit(connection, randomness_account.pubkey(), payer, authority_account)
    await asyncio.sleep(10)

    await reveal(connection, randomness_account.pubkey(), payer, authority_account)


async def init(connection: AsyncClient, randomness_account: Keypair, payer: Keypair, authority_account: Keypair):
    resp = await randomness_init(
        connection=connection,
        randomness_account=randomness_account,
        payer=payer,
        authority=authority_account,
    )

    print(f"Randomness init Signature: {str(resp)}")

    # Write to app.log
    with open("app.log", "a") as log_file:
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_file.write(f"{timestamp} Randomness init Signature: {str(resp)}\n")

    await asyncio.sleep(5)

    # Fetch randomness account data
    randomness_data = await fetch_randomness_account_data(connection, randomness_account.pubkey())

    # Print randomness account data
    print(f"Randomness account data: {json.dumps(randomness_data.to_json_dict(), indent=4)}")

    # Write randomness data to json file
    with open("randomness.json", "w") as f:
        json.dump(randomness_data.to_json_dict(), f, indent=4)

    print(f"Randomness data written to randomness.json")


async def commit(connection: AsyncClient, randomness_account: Pubkey, payer: Keypair, authority_account: Keypair):
    resp = await randomness_commit(connection, randomness_account, payer, authority_account)

    print(f"Randomness commit Signature: {str(resp)}")

    # Write to testrecord.txt
    with open("testrecord.txt", "a") as log_file:
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_file.write(f"{timestamp} Randomness commit Signature: {str(resp)}\n")

    await asyncio.sleep(10)

    # Fetch randomness account data
    randomness_data = await fetch_randomness_account_data(connection, randomness_account)
    print(f"Randomness account data: {json.dumps(randomness_data.to_json_dict(), indent=4)}")

    # Write randomness data to json file
    with open("randomness.json", "w") as f:
        json.dump(randomness_data.to_json_dict(), f, indent=4)
    print(f"Randomness data written to randomness.json")


async def reveal(connection: AsyncClient, randomness_account: Pubkey, payer: Keypair, authority_account: Keypair):
    resp = await randomness_reveal(connection, randomness_account, payer, authority_account)
    print(f"Randomness reveal Signature: {str(resp)}")

    # Write to testrecord.txt
    with open("testrecord.txt", "a") as log_file:
        timestamp = datetime.now().strftime("[%H:%M:%S]")
        log_file.write(f"{timestamp} Randomness reveal Signature: {str(resp)}\n")

    await asyncio.sleep(10)

    # Fetch randomness account data
    randomness_data = await fetch_randomness_account_data(connection, randomness_account)
    print(f"Randomness account data: {json.dumps(randomness_data.to_json_dict(), indent=4)}")

    # Write randomness data to json file
    with open("randomness.json", "w") as f:
        json.dump(randomness_data.to_json_dict(), f, indent=4)
    print(f"Randomness data written to randomness.json")


if __name__ == "__main__":
    # print(Keypair())
    asyncio.run(main())
