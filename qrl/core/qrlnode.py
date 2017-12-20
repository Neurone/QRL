# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import decimal
import time
from decimal import Decimal
from typing import Optional, List

from qrl.core import config, ntp
from qrl.core.EphemeralMessage import EphemeralMessage
from qrl.core.Block import Block
from qrl.core.BufferedChain import BufferedChain
from qrl.core.ESyncState import ESyncState
from qrl.core.StakeValidator import StakeValidator
from qrl.core.State import State
from qrl.core.TokenList import TokenList
from qrl.core.Transaction import TransferTransaction, Transaction, LatticePublicKey
from qrl.core.logger import logger
from qrl.core.p2pChainManager import P2PChainManager
from qrl.core.p2pPeerManager import P2PPeerManager
from qrl.core.p2pTxManagement import P2PTxManagement
from qrl.generated import qrl_pb2, qrllegacy_pb2


# FIXME: This will soon move to core. Split/group functionality
class QRLNode:
    def __init__(self, db_state: State):
        self.start_time = time.time()
        self.db_state = db_state

        self.peer_manager = None
        self.peer_manager = P2PPeerManager()
        self.peer_manager.load_peer_addresses()
        self.peer_manager.register(P2PPeerManager.EventType.NO_PEERS, self.connect_peers)

        self.chain_manager = P2PChainManager()

        self.tx_manager = P2PTxManagement()

        self._buffered_chain = None  # FIXME: REMOVE. This is temporary
        self._p2pfactory = None  # FIXME: REMOVE. This is temporary

    @property
    def version(self):
        # FIXME: Move to __version__ coming from pip
        return config.dev.version

    @property
    def state(self):
        if self._p2pfactory is None:
            return ESyncState.unknown.value
        # FIXME
        return self._p2pfactory.sync_state.state.value

    @property
    def num_connections(self):
        if self._p2pfactory is None:
            return 0
        # FIXME
        return self._p2pfactory.connections

    @property
    def num_known_peers(self):
        # FIXME
        return len(self.peer_addresses)

    @property
    def uptime(self):
        return int(time.time() - self.start_time)

    @property
    def block_height(self):
        return self._buffered_chain.height

    @property
    def staking(self):
        if self._p2pfactory is None:
            return False
        return self._p2pfactory.pos.stake

    @property
    def epoch(self):
        if len(self._buffered_chain._chain.blockchain) == 0:
            return 0
        return self._buffered_chain._chain.blockchain[-1].epoch

    @property
    def uptime_network(self):
        block_one = self._buffered_chain.get_block(1)
        network_uptime = 0
        if block_one:
            network_uptime = int(time.time() - block_one.timestamp)
        return network_uptime

    @property
    def stakers_count(self):
        return len(self.db_state.stake_validators_tracker.sv_dict)

    @property
    def block_last_reward(self):
        if len(self._buffered_chain._chain.blockchain) == 0:
            return 0

        return self._buffered_chain._chain.blockchain[-1].block_reward

    @property
    def block_time_mean(self):
        # FIXME: Keep a moving mean
        return 0

    @property
    def block_time_sd(self):
        # FIXME: Keep a moving var
        return 0

    @property
    def coin_supply(self):
        # FIXME: Keep a moving var
        return self.db_state.total_coin_supply()

    @property
    def coin_supply_max(self):
        # FIXME: Keep a moving var
        return config.dev.max_coin_supply

    @property
    def coin_atstake(self):
        # FIXME: This is very time consuming.. (moving from old code) improve/cache
        total_at_stake = 0
        for staker in self.db_state.stake_validators_tracker.sv_dict:
            total_at_stake += self.db_state.balance(staker)
        return total_at_stake

    @property
    def peer_addresses(self):
        return self.peer_manager._peer_addresses

    @property
    def addresses(self) -> List[bytes]:
        return self._buffered_chain.wallet.addresses

    # FIXME: REMOVE. This is temporary
    def set_chain(self, buffered_chain: BufferedChain):
        self._buffered_chain = buffered_chain

    # FIXME: REMOVE. This is temporary
    def set_p2pfactory(self, p2pfactory):
        self._p2pfactory = p2pfactory

    @staticmethod
    def get_dec_amount(str_amount_arg: str) -> Decimal:
        # FIXME: Concentrating logic into a single point. Fix this, make type safe to avoid confusion. Quantity formats should be always clear
        # FIXME: Review. This is just relocated code. It looks odd
        # FIXME: Antipattern. Magic number.
        # FIXME: Validate string, etc.
        return decimal.Decimal(decimal.Decimal(str_amount_arg) * 100000000).quantize(decimal.Decimal('1'),
                                                                                     rounding=decimal.ROUND_HALF_UP)

    @staticmethod
    def validate_amount(amount_str: str) -> bool:
        # FIXME: Refactored code. Review Decimal usage all over the code
        Decimal(amount_str)
        return True

    def get_address_bundle(self, key_addr: bytes):
        for addr in self._buffered_chain.wallet.address_bundle:
            if addr.address == key_addr:
                return addr
        return None

    # FIXME: Rename this appropriately
    def transfer_coins(self, addr_from: bytes, addr_to: bytes, amount: int, fee: int = 0):
        block_chain_buffer = self._buffered_chain.block_chain_buffer
        stake_validators_tracker = block_chain_buffer.get_stake_validators_tracker(block_chain_buffer.height() + 1)

        addr_bundle = self.get_address_bundle(addr_from)
        if addr_bundle is None:
            raise LookupError("The source address does not belong to this wallet/node")

        xmss_from = addr_bundle.xmss
        if xmss_from is None:
            raise LookupError("The source address does not belong to this wallet/node")

        if addr_from in stake_validators_tracker.sv_dict and stake_validators_tracker.sv_dict[addr_from].is_active:
            raise LookupError("Source address is a Stake Validator, balance is locked while staking")

        if (addr_from in stake_validators_tracker.future_stake_addresses and
                stake_validators_tracker.future_stake_addresses[addr_from].is_active):
            raise LookupError("Source address is a Future Stake Validator, balance is locked")

        xmss_pk = xmss_from.pk()

        # TODO: Review this
        # Balance validation
        if xmss_from.get_remaining_signatures() == 1:
            balance = self.db_state.balance(addr_from)
            if amount + fee < balance:
                # FIXME: maybe this is too strict?
                raise RuntimeError("Last signature! You must move all the funds to another account!")

        tx = self.create_send_tx(addr_from,
                                 addr_to,
                                 amount,
                                 fee,
                                 xmss_pk)

        tx.sign(xmss_from)
        self.submit_send_tx(tx)
        return tx

    # FIXME: Rename this appropriately
    def create_send_tx(self,
                       addr_from: bytes,
                       addr_to: bytes,
                       amount: int,
                       fee: int,
                       xmss_pk: bytes) -> TransferTransaction:
        balance = self.db_state.balance(addr_from)
        if amount + fee > balance:
            raise RuntimeError("Not enough funds in the source address")

        return TransferTransaction.create(addr_to=addr_to,
                                          amount=amount,
                                          fee=fee,
                                          xmss_pk=xmss_pk)

    def create_lt(self,
                  addr_from: bytes,
                  fee: int,
                  kyber_pk: bytes,
                  dilithium_pk: bytes,
                  xmss_pk: bytes) -> LatticePublicKey:

        return LatticePublicKey.create(fee=fee,
                                       kyber_pk=kyber_pk,
                                       dilithium_pk=dilithium_pk,
                                       xmss_pk=xmss_pk)

    def create_ephemeral_channel(self,
                                 addr_from: bytes,
                                 addr_to: bytes,
                                 ttl: int,
                                 active: int,
                                 symmetric_key: bytes,
                                 prf512: bytes):

        active = int(active + ntp.getTime())
        ttl = active + ttl

        lattice_public_keys = self._buffered_chain.get_lattice_public_key(addr_to)
        if not lattice_public_keys.lattice_keys:
            return None

        xmss = self._buffered_chain.find_xmss(addr_from)
        if not xmss:
            return None
        lattice_public_key_txn = LatticePublicKey(lattice_public_keys.lattice_keys[0])
        ephemeral_message = EphemeralMessage.create_channel_request(ttl=ttl,
                                                                    active=active,
                                                                    lattice_key_txn=lattice_public_key_txn,
                                                                    aes256_symkey=symmetric_key,
                                                                    prf512_seed=prf512,
                                                                    address_to=addr_to,
                                                                    xmss=xmss)
        return ephemeral_message

    def create_ephemeral_message(self,
                                 ttl: int,
                                 active: int,
                                 symmetric_key: bytes,
                                 prf512: bytes,
                                 message: bytes):

        ephemeral_message = EphemeralMessage.create_message(msg_id=prf512,
                                                            ttl=ttl,
                                                            active=active,
                                                            message=message,
                                                            aes256_symkey=symmetric_key)
        return ephemeral_message

    def get_ephemeral_message_logs(self, address_from: bytes) -> bytes:
        message_log = self._buffered_chain.get_ephemeral_message_logs(address_from)
        return message_log

    # FIXME: Rename this appropriately
    def submit_send_tx(self, tx: TransferTransaction) -> bool:
        if tx is None:
            raise ValueError("The transaction was empty")

        if tx.subtype == qrl_pb2.Transaction.LATTICE:
            self._p2pfactory.broadcast_lt(tx)
        elif tx.subtype in (qrl_pb2.Transaction.TRANSFER,
                            qrl_pb2.Transaction.MESSAGE,
                            qrl_pb2.Transaction.TOKEN,
                            qrl_pb2.Transaction.TRANSFERTOKEN):
            tx.validate_or_raise()

            block_number = self._buffered_chain.height + 1
            tx_state = self._buffered_chain.get_stxn_state(block_number, tx.txfrom)

            if not tx.validate_extended(tx_state=tx_state,
                                        transaction_pool=self._buffered_chain.tx_pool.transaction_pool):
                raise ValueError("The transaction failed validatation (blockchain state)")

            self._buffered_chain.tx_pool.add_tx_to_pool(tx)
            self._buffered_chain.wallet.save_wallet()
            # FIXME: Optimization Required
            subtype = qrllegacy_pb2.LegacyMessage.TX
            if tx.subtype == qrl_pb2.Transaction.MESSAGE:
                subtype = qrllegacy_pb2.LegacyMessage.MT
            elif tx.subtype == qrl_pb2.Transaction.TOKEN:
                subtype = qrllegacy_pb2.LegacyMessage.TK
            elif tx.subtype == qrl_pb2.Transaction.TRANSFERTOKEN:
                subtype = qrllegacy_pb2.LegacyMessage.TT
            self._p2pfactory.broadcast_tx(tx, subtype=subtype)

        return True

    def broadcast_eph(self, ephemeral_channel_request, operator_xmss_address) -> bool:
        if not ephemeral_channel_request:
            raise ValueError("EphemeralChannel was Empty")

        self._p2pfactory.broadcast_eph(ephemeral_channel_request, operator_xmss_address)

        return True

    @staticmethod
    def address_is_valid(address: bytes) -> bool:
        # TODO: Validate address format
        if len(address) < 1:
            return False

        if address[0] != ord('Q'):
            return False

        return True

    def get_address_is_used(self, address: bytes) -> bool:
        if not self.address_is_valid(address):
            raise ValueError("Invalid Address")

        return self.db_state.address_used(address)

    def get_address_state(self, address: bytes) -> qrl_pb2.AddressState:
        if not self.address_is_valid(address):
            raise ValueError("Invalid Address")

        tmp_address_state = self.db_state.get_address(address)
        transaction_hashes = self.db_state.get_address_tx_hashes(address)
        address_state = qrl_pb2.AddressState(address=tmp_address_state.address,
                                             balance=tmp_address_state.balance,
                                             nonce=tmp_address_state.nonce,
                                             ots_bitfield=tmp_address_state.ots_bitfield,
                                             transaction_hashes=transaction_hashes)

        return address_state

    def get_transaction(self, query_hash: bytes) -> Optional[Transaction]:
        """
        This method returns an object that matches the query hash
        """
        # FIXME: At some point, all objects in DB will indexed by a hash
        # TODO: Search tx hash
        # FIXME: We dont need searches, etc.. getting a protobuf indexed by hash from DB should be enough
        # FIXME: This is just a workaround to provide functionality

        return self._buffered_chain.get_transaction(query_hash)

    def get_block_from_hash(self, query_hash: bytes) -> Optional[Block]:
        """
        This method returns an object that matches the query hash
        """
        # FIXME: At some point, all objects in DB will indexed by a hash
        return None

    def get_block_from_index(self, index: int) -> Block:
        """
        This method returns an object that matches the query hash
        """
        # FIXME: At some point, all objects in DB will indexed by a hash
        return self._buffered_chain.get_block(index)

    def get_blockidx_from_txhash(self, transaction_hash):
        answer = self.db_state.get_tx_metadata(transaction_hash)
        if answer is None:
            return None
        else:
            _, block_index = answer
        return block_index

    def get_token_detailed_list(self):
        pbdata = self.db_state.get_token_list()
        token_list = TokenList.from_json(pbdata)
        token_detailed_list = qrl_pb2.TokenDetailedList()
        for token_txhash in token_list.token_txhash:
            token_txn, _ = self.db_state.get_tx_metadata(token_txhash)
            token_detailed_list.tokens.extend([token_txn.pbdata])
        return token_detailed_list

    def get_current_stakers(self, offset, count) -> List[StakeValidator]:
        stakers = list(self.db_state.stake_validators_tracker.sv_dict.values())
        start = min(offset, len(stakers))
        end = min(start + count, len(stakers))
        return stakers[start:end]

    def get_next_stakers(self, offset, count) -> List[StakeValidator]:
        stakers = list(self.db_state.stake_validators_tracker.sv_dict.values())
        start = min(offset, len(stakers))
        end = min(start + count, len(stakers))
        return stakers[start:end]

    def get_vote_metadata(self, blocknumber):
        return self._buffered_chain.get_vote_metadata(blocknumber)

    def get_latest_blocks(self, offset, count) -> List[Block]:
        # FIXME: This is incorrect. Offset does not work
        answer = []
        end = self.block_height - offset
        start = max(0, end - count - offset)
        for blk_idx in range(start, end + 1):
            answer.append(self._buffered_chain.get_block(blk_idx))

        return answer

    def get_latest_transactions(self, offset, count):
        # FIXME: This is incorrect
        # FIXME: Moved code. Breaking encapsulation. Refactor
        answer = []
        skipped = 0
        for tx in self.db_state.get_last_txs():
            if isinstance(tx, TransferTransaction):
                if skipped >= offset:
                    answer.append(tx)
                    if len(answer) >= count:
                        break
                else:
                    skipped += 1

        return answer

    def get_latest_transactions_unconfirmed(self, offset, count):
        answer = []
        skipped = 0
        for tx in self._buffered_chain.tx_pool.transaction_pool:
            if isinstance(tx, TransferTransaction):
                if skipped >= offset:
                    answer.append(tx)
                    if len(answer) >= count:
                        break
                else:
                    skipped += 1
        return answer

    def getNodeInfo(self) -> qrl_pb2.NodeInfo:
        info = qrl_pb2.NodeInfo()
        info.version = self.version
        info.state = self.state
        info.num_connections = self.num_connections
        info.num_known_peers = self.num_known_peers
        info.uptime = self.uptime
        info.block_height = self.block_height
        info.block_last_hash = b''  # FIXME
        info.stake_enabled = self.staking
        info.network_id = config.dev.genesis_prev_headerhash  # FIXME
        return info

    ####################################################
    ####################################################
    ####################################################
    ####################################################

    def connect_peers(self):
        logger.info('<<<Reconnecting to peer list: %s', self.peer_addresses)
        for peer_address in self.peer_addresses:
            self._p2pfactory.connect_peer(peer_address)
