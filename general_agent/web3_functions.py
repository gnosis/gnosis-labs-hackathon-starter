import os

from eth_account import Account
from eth_typing import ChecksumAddress
from web3.types import (  # noqa: F401  # Import for the sake of easy importing with others from here.
    Wei,
)
from microchain import Function
from web3 import Web3


class GetBalance(Function):
    def __init__(self) -> None:
        # We define a web3 connector here using either the ENV or the default RPC.
        GNOSIS_RPC_URL = os.getenv(
            "GNOSIS_RPC_URL", "https://gnosis-rpc.publicnode.com"
        )
        self.w3 = Web3(Web3.HTTPProvider(GNOSIS_RPC_URL))
        super().__init__()

    @property
    def description(self) -> str:
        return "Use this function to fetch the balance of a given account in xDAI"

    @property
    def example_args(self) -> list[ChecksumAddress]:
        return [Web3.to_checksum_address("0x464A10A122Cb5B47e9B27B9c5286BC27487a6ACd")]

    def __call__(self, address: ChecksumAddress) -> Wei:
        return self.w3.eth.get_balance(account=address)


class GetOwnWallet(Function):
    @property
    def description(self) -> str:
        return "Use this function to fetch your wallet address"

    @property
    def example_args(self) -> list[str]:
        return []

    def __call__(self) -> str:
        private_key = os.getenv("BET_FROM_PRIVATE_KEY")
        if not private_key:
            raise EnvironmentError("BET_FROM_PRIVATE_KEY missing in the environment.")
        acc = Account.from_key(private_key)
        return str(acc.address)