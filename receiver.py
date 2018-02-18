import dweepy

for dweet in dweepy.listen_for_dweets_from('raspberryPI'):
    print dweet
