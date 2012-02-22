SALT_KEY = 514229

def is_salt_valid( salt):
    data = salt[:6]
    check = salt[6:]
    m = str((int(data) ^ SALT_KEY) % 999)
    if m == check:
        return True
    return False

# simple mais pourri
def sign_message( msg):
    res = 0
    for i, c in enumerate(msg):
        res += ord(c) * (i % 20)
    sig = ("%06d" % res)[:6]
    check = str((int(sig) ^ SALT_KEY) % 999)
    sig += check
    return sig
