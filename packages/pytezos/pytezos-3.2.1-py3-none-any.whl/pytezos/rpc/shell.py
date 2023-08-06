from binascii import hexlify
from datetime import datetime
from functools import lru_cache
from time import sleep
from typing import Any, Dict, List, Optional

import requests
import simplejson as json

from pytezos.crypto.encoding import base58_decode
from pytezos.jupyter import get_attr_docstring
from pytezos.logging import logger
from pytezos.rpc.kind import validation_passes
from pytezos.rpc.query import RpcQuery
from pytezos.rpc.search import CyclesQuery, VotingPeriodsQuery


def make_operation_result(**kwargs):
    return {'metadata': {'operation_result': kwargs}}


class ShellQuery(RpcQuery, path=''):
    @property
    def blocks(self):
        """Shortcut for `chains.main.blocks`"""
        return self.chains.main.blocks

    @property
    def head(self):
        """Shortcut for `blocks.head`"""
        return self.blocks.head

    @property  # type: ignore
    @lru_cache(maxsize=None)
    def block(self):
        """Cached head block, useful if you just want to explore things."""
        return self.blocks[self.head.hash()]

    @property
    def cycles(self):
        """Operate on cycles rather than blocks."""
        return CyclesQuery(node=self.node, path=self._wild_path + '/chains/{}/blocks', params=self._params + ['main'])

    @property
    def voting_periods(self):
        """
        Operate on voting periods rather than blocks.
        """
        return VotingPeriodsQuery(node=self.node, path=self._wild_path + '/chains/{}/blocks', params=self._params + ['main'])

    @property
    def contracts(self):
        """Shortcut for `head.context.contracts`"""
        return self.head.context.contracts

    @property
    def mempool(self):
        """Shortcut for `chains.main.mempool`"""
        return self.chains.main.mempool

    def wait_next_block(
        self,
        delay_sec=1,
        prev_hash=None,
        time_between_blocks: Optional[int] = None,
        max_iterations: Optional[int] = None,
    ):
        """Wait until next block is finalized.

        :param prev_hash: Current block hash (optional). If not set, current head is used.
        :param time_between_blocks: override the corresponding parameter from constants
        :param max_iterations: Manually set the number of iterations
        :param delay_sec: Sleep delay
        """
        if time_between_blocks is None:
            time_between_blocks = int(self.block.context.constants()["time_between_blocks"][0])  # type: ignore

        if time_between_blocks > 0:
            if prev_hash is None:
                header = self.head.header()
                prev_hash = header['hash']
                prev_block_dt = datetime.strptime(header['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                elapsed_sec = (datetime.utcnow() - prev_block_dt).seconds
                sleep_sec = 0 if elapsed_sec > time_between_blocks else time_between_blocks - elapsed_sec
            else:
                sleep_sec = time_between_blocks
            logger.info('Wait %s seconds until block %s is finalized', sleep_sec, prev_hash)
            sleep(sleep_sec)

        if max_iterations is None:
            max_iterations = max(1, time_between_blocks)

        for _ in range(max_iterations):
            current_block_hash = self.head.hash()
            if current_block_hash == prev_hash:
                sleep(delay_sec)
            else:
                return current_block_hash
        raise StopIteration("Timeout")

    def get_confirmations(self, opg_hash, kind, branch, head) -> int:
        """Returns the number of blocks applied after the operation was included in chain

        :param opg_hash: Operation group hash
        :param kind: Operation kind ('transaction', 'origination', etc)
        :param branch: Block ID one should stop the search at
        :param head: Block ID one should start the search from
        :return: Number of confirmations (0 if not found)
        """
        start = self.blocks[head].header()['level']
        stop = self.blocks[branch].header()['level']
        for level in range(start, stop, -1):
            vp = validation_passes[kind]
            hashes = self.blocks[level].operation_hashes[vp]()
            for idx, _hash in enumerate(hashes):
                if opg_hash == _hash:
                    _ = self.blocks[level].operations[vp, idx]()
                    logger.info('Operation %s was included in block %s', opg_hash, level)
                    return start - level + 1
        return 0


class ChainQuery(RpcQuery, path='/chains/{}'):
    def watermark(self):
        """Chain watermark, hex encoded."""
        data = self.chain_id()
        return hexlify(base58_decode(data.encode())).decode()


class InvalidBlockQuery(RpcQuery, path='/chains/{}/invalid_blocks/{}'):
    def delete(self):
        return self._delete()


class MempoolQuery(RpcQuery, path='/chains/{}/mempool'):
    def post(self, configuration):
        """Set operation filter rules.

        :param configuration: a JSON dictionary, known keys are `minimal_fees`, `minimal_nanotez_per_gas_unit`,
            `minimal_nanotez_per_byte`
        """
        return self._post(json=configuration)


class PendingOperationsQuery(RpcQuery, path='/chains/{}/mempool/pending_operations'):
    def __getitem__(self, item: str) -> Dict[str, Any]:
        """Search for operation in node's mempool by hash.

        :param item: operation group hash (base58)
        """
        operations_dict = self()
        for status, operations in operations_dict.items():
            for operation in operations:
                if isinstance(operation, dict):
                    if operation['hash'] == item:
                        return {
                            **make_operation_result(status=status),
                            **operation,
                        }
                elif isinstance(operation, list):
                    if operation[0] == item:
                        errors = operation[1].pop1('error', default=[])
                        return {
                            **make_operation_result(status=status, errors=errors),
                            **operation[1],
                            'hash': operation[0],
                        }
                else:
                    raise Exception('Unknown operation type', operation)
        raise StopIteration

    def flatten(self) -> List[Dict[str, Any]]:
        operations_dict = self()
        operations_list = list()
        for status, operations in operations_dict.items():
            for operation in operations:
                if isinstance(operation, dict):
                    operations_list.append(
                        {
                            **make_operation_result(status=status),
                            **operation,
                        }
                    )
                elif isinstance(operation, list):
                    errors = operation[1].pop1('error', default=[])
                    operations_list.append(
                        {
                            **make_operation_result(status=status, errors=errors),
                            **operation[1],
                            'hash': operation[0],
                        }
                    )
                else:
                    raise Exception('Unknown operation type', operation)
        return operations_list

    def __repr__(self):
        res = [
            super(PendingOperationsQuery, self).__repr__(),
            '[]' + get_attr_docstring(self.__class__, '__getitem__'),
        ]
        return '\n'.join(res)


class DescribeQuery(RpcQuery, path='/describe'):
    def __call__(self, recurse=True):
        """Get RPCs documentation and input/output schema.

        :param recurse: Show information for child elements, default is True.
            In some cases doesn't work without this flag.
        """
        return super(DescribeQuery, self).__call__(recurse=recurse)

    def __repr__(self):
        res = [
            super(DescribeQuery, self).__repr__(),
            f'(){get_attr_docstring(DescribeQuery, "__call__")}',
            'Can be followed by any path:\n.chains\n.network.connections\netc\n',
        ]
        return '\n'.join(res)


class BlockInjectionQuery(RpcQuery, path='/injection/block'):
    def post(self, block, timestamp=None, _async=False, force=False, chain=None):
        """Inject a block in the node and broadcast it.

        The `operations` embedded in `blockHeader` might be pre-validated using a contextual RPCs from the latest block
        (e.g. '/blocks/head/context/preapply').

        block format:

        .. code-block:: python

            {
                "data": <hex-encoded block header>,
                "operations": [ [ {
                "branch": <block_hash>,
                "data": <hex-encoded operation>
                } ... ] ... ]
            }

        :param block: JSON input
        :param _async: By default, the RPC will wait for the block to be validated before answering, \
        set True if you don't want to.
        :param force:
        :param chain: Optionally you can specify the chain (main/test)
        :returns: ID of the block
        """
        return self._post(
            params={
                'async': _async,
                'force': force,
                'chain': chain,
                'timestamp': timestamp,
            },
            json=block,
        )


class OperationInjectionQuery(RpcQuery, path='/injection/operation'):
    def post(self, operation, _async=False, chain=None):
        """Inject an operation in node and broadcast it.
        The `signedOperationContents` should be constructed using a contextual RPCs from the latest block
        and signed by the client.

        :param operation: Hex-encoded operation data or bytes
        :param _async: By default, the RPC will wait for the operation to be (pre-)validated before answering,
            set True if you don't want to.
        :param chain: Optionally you can specify the chain
        :returns: ID of the operation
        """
        if isinstance(operation, bytes):
            operation = operation.hex()

        return self._post(
            params={
                'async': _async,
                'chain': chain,
            },
            json=operation,
        )


class ProtocolInjectionQuery(RpcQuery, path='/injection/protocol'):
    def post(self, protocol, _async=False, force=False):
        """Inject a protocol in node.

        protocol format:

        .. code-block:: python

            {
                "expected_env_version": <integer>,
                "components": [{
                    "name": <unistring>,
                    "interface"?: <hex-encoded data>,
                    "implementation": <hex-encoded data> }
                     ...
                ]}
            }

        :param protocol: JSON input
        :param _async:
        :param force:
        :returns: ID of the protocol
        """
        return self._post(
            params={
                'async': _async,
                'force': force,
            },
            json=protocol,
        )


class ResponseGenerator:
    def __init__(self, res: requests.Response):
        self._lines = res.iter_lines()

    def __iter__(self):
        for line in self._lines:
            yield json.loads(line.decode())


class MonitorQuery(
    RpcQuery,
    path=[
        '/monitor/active_chains',
        '/monitor/bootstrapped',
        '/monitor/commit_hash',
        '/monitor/heads/{}',
        '/monitor/protocols',
        '/monitor/valid_blocks',
    ],
):
    def __call__(self, *args, **kwargs):
        return ResponseGenerator(
            self.node.request(
                method='GET',
                path=self.path,
                params=kwargs,
                stream=True,
            )
        )

    def __repr__(self):
        res = [
            super(MonitorQuery, self).__repr__(),
            'NOTE: Returned object is a generator.',
        ]
        return '\n'.join(res)


class ConnectionQuery(RpcQuery, path='/network/connections/{}'):
    def delete(self, wait=False):
        return self._delete(params=dict(wait=wait))


class NetworkItems(RpcQuery, path=['/network/peers', '/network/points']):
    def __call__(self, _filter=None):
        return self._get(params={'filter': _filter})


class NetworkLogQuery(RpcQuery, path=['/network/peers/{}/log', '/network/points/{}/log']):
    def __call__(self, monitor=False):
        if monitor:
            return ResponseGenerator(
                self.node.request(
                    method='GET',
                    path=self.path,
                    stream=True,
                )
            )
        return self._get()
