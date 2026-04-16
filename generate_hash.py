import hashlib

names = ["kumar", "rohini", "sasi","suma"]

for name in names:
    print(name, "→", hashlib.sha256(name.encode()).hexdigest())