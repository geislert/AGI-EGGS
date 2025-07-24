import asyncio
import pytest

from agi_eggs.node import PiNode, EggNode
from agi_eggs.network import Network
from agi_eggs.persistence import MessageStore

@pytest.mark.asyncio
async def test_message_exchange(tmp_path):
    pi_store = MessageStore(tmp_path/'pi.jsonl')
    egg_store = MessageStore(tmp_path/'egg.jsonl')
    pi = PiNode('pi', store=pi_store)
    egg = EggNode('egg', port=8766, store=egg_store)

    net_pi = Network(port=8765)
    net_egg = Network(port=8766)

    await asyncio.gather(net_pi.start_server(pi), net_egg.start_server(egg))

    received = {}
    @pi.on('reply')
    async def on_reply(msg):
        received['reply'] = msg.content['message']

    writer_to_pi = await net_egg.connect('localhost', 8765)
    await egg.send(writer_to_pi, {'key':'reply', 'message':'hi'})
    await asyncio.sleep(0.1)

    await net_pi.stop()
    await net_egg.stop()

    assert received.get('reply') == 'hi'
