import hashlib
import random
import time

from app.eospy.keys import EOSKey



def generate_house_seed():
    ms = int(round(time.time() * 1000))
    rd = random.randint(0, 9999999)
    seed = sha256(str(ms) + str(rd))
    return seed


def get_expire_timestamp():
    return int(time.time()) + 600


# abcdefghij12


def get_random_user_seed():
    rd = random.randint(0, 9999999)
    h = sha256(str(rd))
    return str(h)[0:12]


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


user_seed = get_random_user_seed()
print('user_seed=' + user_seed)

house_seed = generate_house_seed()
print('house_seed=' + house_seed)

house_seed_hash = sha256(house_seed)
print('house_seed_hash=' + house_seed_hash)

expire_st = get_expire_timestamp()
print('expire_st=' + str(expire_st))

sig_data = house_seed_hash + str(expire_st)
print('sig_data=' + sig_data)

digest = sha256(sig_data)
sig = k.sign(digest)
print('sig=' + sig)

# EOS7ikmSFnJ4UuAuGDPQMTZFBQa7Kh6QTzBAUivksFETmX6ncxGW7

# r = k.verify("SIG_K1_K2rGavWb37ixHBrMTWLFDp9W7uQUkzXVUaK79KF3vuQrkqt2PMQzvdZhy1ryBEgWauAKPRnuZ24rypzTJNJXk6rG5qzEXr",
#              "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
# print(r)
