from agi_eggs.power.disaster_charging import allocate_power


def test_allocate_power():
    assert allocate_power('solar')[0] == 'comms'
    assert allocate_power('hand_crank')[0] == 'sos_beacon'
