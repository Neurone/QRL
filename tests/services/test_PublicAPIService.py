# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import heapq
from unittest import TestCase

from grpc import ServicerContext, StatusCode
from mock import Mock, MagicMock, patch
from pyqrllib.pyqrllib import str2bin, hstr2bin, bin2hstr

from qrl.core import config
from qrl.core.AddressState import AddressState
from qrl.core.Block import Block
from qrl.core.ChainManager import ChainManager
from qrl.core.GenesisBlock import GenesisBlock
from qrl.core.State import State
from qrl.core.TransactionInfo import TransactionInfo
from qrl.core.txs.TransferTransaction import TransferTransaction
from qrl.core.misc import logger
from qrl.core.node import SyncState, POW
from qrl.core.p2p.p2pfactory import P2PFactory
from qrl.core.qrlnode import QRLNode
from qrl.crypto.misc import sha256
from qrl.generated import qrl_pb2
from qrl.services.PublicAPIService import PublicAPIService
from tests.misc.helper import get_alice_xmss, get_bob_xmss, replacement_getTime
from tests.blockchain.MockedBlockchain import MockedBlockchain

logger.initialize_default()


@patch('qrl.core.misc.ntp.getTime', new=replacement_getTime)
class TestPublicAPI(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPublicAPI, self).__init__(*args, **kwargs)

    def test_getNodeState(self):
        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.sync_state = SyncState()
        p2p_factory.num_connections = 23
        p2p_factory.pow = Mock()

        chain_manager = Mock(spec=ChainManager)
        chain_manager.height = 0
        chain_manager.last_block = Block()

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode._p2pfactory = p2p_factory
        qrlnode._pow = p2p_factory.pow

        service = PublicAPIService(qrlnode)
        node_state = service.GetNodeState(request=qrl_pb2.GetNodeStateReq, context=None)

        # self.assertEqual(__version__, node_state.info.version)  # FIXME
        self.assertEqual(qrl_pb2.NodeInfo.UNSYNCED, node_state.info.state)
        self.assertEqual(23, node_state.info.num_connections)
        # self.assertEqual("testnet", node_state.info.network_id)  # FIXME

    def test_getKnownPeers(self):
        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.sync_state = SyncState()
        p2p_factory.num_connections = 23
        p2p_factory.pow = Mock()

        chain_manager = Mock(spec=ChainManager)
        chain_manager.height = 0
        chain_manager.last_block = Block()

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode._p2pfactory = p2p_factory
        qrlnode._pow = p2p_factory.pow
        qrlnode.peer_manager = Mock()
        qrlnode.peer_manager.known_peer_addresses = ['127.0.0.1', '192.168.1.1']

        service = PublicAPIService(qrlnode)
        response = service.GetKnownPeers(request=qrl_pb2.GetKnownPeersReq, context=None)

        self.assertEqual(2, len(response.known_peers))
        self.assertEqual('127.0.0.1', response.known_peers[0].ip)
        self.assertEqual('192.168.1.1', response.known_peers[1].ip)

        logger.info(response)

    def test_getStats(self):
        db_state = Mock(spec=State)
        db_state.total_coin_supply = 1000
        db_state.get_measurement = MagicMock(return_value=60)
        db_state.get_block_by_number = MagicMock(return_value=None)

        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.sync_state = SyncState()
        p2p_factory.num_connections = 23
        p2p_factory.pow = Mock()

        chain_manager = ChainManager(db_state)
        chain_manager._last_block = GenesisBlock()

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode._p2pfactory = p2p_factory
        qrlnode._pow = p2p_factory.pow

        service = PublicAPIService(qrlnode)
        request = qrl_pb2.GetStatsReq()
        stats = service.GetStats(request=request, context=None)

        # self.assertEqual(__version__, stats.node_info.version)  # FIXME

        self.assertEqual(qrl_pb2.NodeInfo.UNSYNCED, stats.node_info.state)
        self.assertEqual(23, stats.node_info.num_connections)
        # self.assertEqual("testnet", stats.node_info.network_id)  # FIXME

        self.assertEqual(0, stats.epoch)
        self.assertEqual(0, stats.uptime_network)

        self.assertEqual(65000000000000000, stats.block_last_reward)
        self.assertEqual(0, stats.block_time_mean)
        self.assertEqual(0, stats.block_time_sd)

        self.assertEqual(105000000, stats.coins_total_supply)
        self.assertEqual(1000, stats.coins_emitted)

        self.assertEqual(0, len(stats.block_timeseries))

    def test_getStats_timeseries(self):
        with MockedBlockchain.create(10) as mock_blockchain:
            service = PublicAPIService(mock_blockchain.qrlnode)
            request = qrl_pb2.GetStatsReq(include_timeseries=1)
            stats = service.GetStats(request=request, context=None)

            print(stats.block_timeseries)

            self.assertEqual(11, len(stats.block_timeseries))
            self.assertEqual(61, stats.block_time_mean)
            self.assertEqual(1, stats.block_time_sd)

    def test_getAddressState(self):
        db_state = Mock(spec=State)
        alice_xmss = get_alice_xmss()
        address_state = AddressState.create(address=alice_xmss.address,
                                            nonce=25,
                                            balance=10,
                                            ots_bitfield=[b'\x00'] * config.dev.ots_bitfield_size,
                                            tokens=dict(),
                                            slave_pks_access_type=dict(),
                                            ots_counter=0)
        db_state.get_address_state = MagicMock(return_value=address_state)

        p2p_factory = Mock(spec=P2PFactory)
        chain_manager = ChainManager(db_state)

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode._p2pfactory = p2p_factory
        qrlnode._peer_addresses = ['127.0.0.1', '192.168.1.1']

        service = PublicAPIService(qrlnode)

        context = Mock(spec=ServicerContext)
        request = qrl_pb2.GetAddressStateReq()
        service.GetAddressState(request=request, context=context)
        context.set_code.assert_called()
        context.set_details.assert_called()

        context = Mock(spec=ServicerContext)
        request = qrl_pb2.GetAddressStateReq()
        request.address = get_alice_xmss().address
        response = service.GetAddressState(request=request, context=context)
        context.set_code.assert_not_called()

        self.assertEqual(alice_xmss.address, response.state.address)
        self.assertEqual(25, response.state.nonce)
        self.assertEqual(10, response.state.balance)
        self.assertEqual([b'\x00'] * config.dev.ots_bitfield_size, response.state.ots_bitfield)
        self.assertEqual([], response.state.transaction_hashes)

    def test_getObject(self):
        SOME_ODD_HASH = sha256(b'this should not be found')

        db_state = Mock(spec=State)
        db_state.get_tx_metadata = MagicMock(return_value=None)
        db_state.get_block = MagicMock(return_value=None)

        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.pow = Mock(spec=POW)

        chain_manager = ChainManager(db_state)

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode._p2pfactory = p2p_factory
        qrlnode._pow = p2p_factory.pow
        qrlnode._peer_addresses = ['127.0.0.1', '192.168.1.1']

        service = PublicAPIService(qrlnode)

        # First try an empty request
        context = Mock(spec=ServicerContext)
        request = qrl_pb2.GetObjectReq()
        response = service.GetObject(request=request, context=context)
        context.set_code.assert_not_called()
        context.set_details.assert_not_called()
        self.assertFalse(response.found)

        # Some odd address
        context = Mock(spec=ServicerContext)
        request = qrl_pb2.GetObjectReq()
        request.query = SOME_ODD_HASH
        response = service.GetObject(request=request, context=context)
        context.set_code.assert_not_called()
        self.assertFalse(response.found)

        # Find an address
        bob_xmss = get_bob_xmss()
        addr1_state = AddressState.create(address=bob_xmss.address,
                                          nonce=25,
                                          balance=10,
                                          ots_bitfield=[b'\x00'] * config.dev.ots_bitfield_size,
                                          tokens=dict(),
                                          slave_pks_access_type=dict(),
                                          ots_counter=0)
        addr1_state.transaction_hashes.append(sha256(b'0'))
        addr1_state.transaction_hashes.append(sha256(b'1'))

        db_state.get_address_state = MagicMock(return_value=addr1_state)

        context = Mock(spec=ServicerContext)
        request = qrl_pb2.GetObjectReq()
        request.query = bob_xmss.address
        response = service.GetObject(request=request, context=context)
        context.set_code.assert_not_called()
        self.assertTrue(response.found)
        self.assertIsNotNone(response.address_state)

        self.assertEqual(bob_xmss.address, response.address_state.address)
        self.assertEqual(25, response.address_state.nonce)
        self.assertEqual(10, response.address_state.balance)
        self.assertEqual([sha256(b'0'), sha256(b'1')], response.address_state.transaction_hashes)

        # Find a transaction
        alice_xmss = get_alice_xmss()
        db_state.address_used = MagicMock(return_value=False)
        tx1 = TransferTransaction.create(
            addrs_to=[bob_xmss.address],
            amounts=[125],
            fee=19,
            xmss_pk=bob_xmss.pk,
            master_addr=alice_xmss.address)

        chain_manager.tx_pool.transaction_pool = [(0, TransactionInfo(tx1, 0))]

        context = Mock(spec=ServicerContext)
        request = qrl_pb2.GetObjectReq()
        request.query = tx1.txhash
        response = service.GetObject(request=request, context=context)
        context.set_code.assert_not_called()
        self.assertTrue(response.found)
        self.assertIsNotNone(response.transaction)
        self.assertEqual('transfer', response.transaction.tx.WhichOneof('transactionType'))
        self.assertEqual(alice_xmss.address, response.transaction.tx.master_addr)
        self.assertEqual(bob_xmss.pk, response.transaction.tx.public_key)
        self.assertEqual(tx1.txhash, response.transaction.tx.transaction_hash)
        self.assertEqual(b'', response.transaction.tx.signature)

        self.assertEqual(bob_xmss.address, response.transaction.tx.transfer.addrs_to[0])
        self.assertEqual(125, response.transaction.tx.transfer.amounts[0])
        self.assertEqual(19, response.transaction.tx.fee)

        alice_xmss = get_alice_xmss()
        # Find a block
        db_state.get_block_by_number = MagicMock(
            return_value=Block.create(block_number=1,
                                      prev_headerhash=sha256(b'reveal'),
                                      prev_timestamp=10,
                                      transactions=[],
                                      miner_address=alice_xmss.address))

        context = Mock(spec=ServicerContext)
        request = qrl_pb2.GetObjectReq()
        request.query = bytes(str2bin('1'))
        response = service.GetObject(request=request, context=context)
        context.set_code.assert_not_called()
        self.assertTrue(response.found)
        self.assertIsNotNone(response.block_extended)
        self.assertEqual(1, response.block_extended.header.block_number)

    def test_getLatestData(self):
        blocks = []
        txs = []
        alice_xmss = get_alice_xmss()
        bob_xmss = get_bob_xmss()
        for i in range(1, 4):
            for j in range(1, 3):
                txs.append(TransferTransaction.create(addrs_to=[bob_xmss.address],
                                                      amounts=[i * 100 + j],
                                                      fee=j,
                                                      xmss_pk=alice_xmss.pk))

            blocks.append(Block.create(block_number=i,
                                       prev_headerhash=sha256(b'reveal'),
                                       prev_timestamp=10,
                                       transactions=txs,
                                       miner_address=alice_xmss.address))

        txpool = []
        for j in range(10, 15):
            tx = TransferTransaction.create(addrs_to=[bob_xmss.address],
                                            amounts=[1000 + j],
                                            fee=j,
                                            xmss_pk=get_alice_xmss().pk)
            txpool.append((tx.fee, TransactionInfo(tx, 0)))

        db_state = Mock(spec=State)
        db_state.get_tx_metadata = MagicMock(return_value=None)
        db_state.get_last_txs = MagicMock(return_value=txs)
        db_state.get_block_by_number = Mock()
        db_state.get_block_by_number.side_effect = blocks

        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.pow = Mock(spec=POW)

        chain_manager = ChainManager(db_state)
        chain_manager.tx_pool = Mock()
        chain_manager.tx_pool.transactions = heapq.nlargest(len(txpool), txpool)
        chain_manager.tx_pool.transaction_pool = txpool
        chain_manager._last_block = Mock()
        chain_manager._last_block.block_number = len(blocks)

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode.get_block_from_index = MagicMock(return_value=None)

        qrlnode._p2pfactory = p2p_factory
        qrlnode._pow = p2p_factory.pow

        service = PublicAPIService(qrlnode)
        context = Mock(spec=ServicerContext)

        request = qrl_pb2.GetLatestDataReq(filter=qrl_pb2.GetLatestDataReq.ALL,
                                           offset=1,
                                           quantity=3)

        response = service.GetLatestData(request=request, context=context)

        context.set_code.assert_not_called()
        context.set_details.assert_not_called()

        # Verify blockheaders
        self.assertEqual(3, len(response.blockheaders))
        self.assertEqual(1, response.blockheaders[0].header.block_number)
        self.assertEqual(2, response.blockheaders[1].header.block_number)
        self.assertEqual(3, response.blockheaders[2].header.block_number)

        # Verify transactions_unconfirmed
        self.assertEqual(3, len(response.transactions_unconfirmed))
        # TODO: Verify expected order
        self.assertEqual(1013, response.transactions_unconfirmed[0].tx.transfer.amounts[0])
        self.assertEqual(1012, response.transactions_unconfirmed[1].tx.transfer.amounts[0])
        self.assertEqual(1011, response.transactions_unconfirmed[2].tx.transfer.amounts[0])

        # Verify transactions
        self.assertEqual(3, len(response.transactions))
        self.assertEqual(2, response.transactions[0].tx.fee)
        self.assertEqual(1, response.transactions[1].tx.fee)
        self.assertEqual(2, response.transactions[2].tx.fee)

        self.assertEqual(102, response.transactions[0].tx.transfer.amounts[0])
        self.assertEqual(201, response.transactions[1].tx.transfer.amounts[0])
        self.assertEqual(202, response.transactions[2].tx.transfer.amounts[0])

    def test_GetAddressFromPK(self):
        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.sync_state = SyncState()
        p2p_factory.num_connections = 23
        p2p_factory.pow = Mock()

        chain_manager = Mock(spec=ChainManager)
        chain_manager.height = 0

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode._p2pfactory = p2p_factory
        qrlnode._pow = p2p_factory.pow

        service = PublicAPIService(qrlnode)
        pk = hstr2bin('01060057ac9cb6085a8135631dcf018dff46d9c368a0b64d508f512e584199b6800'
                      'f8cfcb672b931398a023680fe0308ed4b6ec75877d684bc2ccf11703e8369f064e7')
        request = qrl_pb2.GetAddressFromPKReq(pk=bytes(pk))
        response = service.GetAddressFromPK(request=request, context=None)
        self.assertEqual('010600b56d161c7de8aa741962e3e49b973b7e53456fa47f2443d69f17c632f29c8b1aab7d2491',
                         bin2hstr(response.address))

    def test_GetTokenTxn_Error(self):
        p2p_factory = Mock(spec=P2PFactory)
        p2p_factory.sync_state = SyncState()
        p2p_factory.num_connections = 23
        p2p_factory.pow = Mock()

        chain_manager = Mock(spec=ChainManager)
        chain_manager.height = 0

        qrlnode = QRLNode(mining_address=b'')
        qrlnode.set_chain_manager(chain_manager)
        qrlnode._p2pfactory = p2p_factory
        qrlnode._pow = p2p_factory.pow

        service = PublicAPIService(qrlnode)
        request = qrl_pb2.TokenTxnReq()
        context = Mock(spec=ServicerContext)
        context.set_code = MagicMock()

        service.GetTokenTxn(request=request, context=context)
        context.set_code.assert_called_with(StatusCode.INVALID_ARGUMENT)
