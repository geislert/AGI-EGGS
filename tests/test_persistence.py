from agi_eggs.node import Message
from agi_eggs.persistence import MessageStore


def test_store_roundtrip(tmp_path):
    store = MessageStore(tmp_path/'msgs.jsonl')
    m = Message(sender='a', content={'key':'x'})
    store.append(m)
    msgs = store.read_all()
    assert len(msgs) == 1
    assert msgs[0].sender == 'a'
    # file should be removed after reading
    assert not (tmp_path/'msgs.jsonl').exists()
