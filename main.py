from bloomfilter import BloomFilter

bloom_filter = BloomFilter(20, 0.05)

emails = [
    "abound@email.com",
    "abounds@email.com",
    "abundance@email.com",
    "abundant@email.com",
    "accessible@email.com",
    "bloom@email.com",
    "blossom@email.com",
    "bolster@email.com",
    "bonny@email.com",
    "bonus@email.com",
    "bonuses@email.com",
    "coherent@email.com",
    "cohesive@email.com",
    "colorful@email.com",
    "comely@email.com",
    "comfort@email.com",
    "gems@email.com",
    "generosity@email.com",
    "generous@email.com",
    "generously@email.com",
    "genial@email.com",
]

for email in emails:
    bloom_filter.add(email)

test_emails = [
    "banana@email.com",
    "minion@email.com",
    "abound@email.com",
    "comfort@email.com",
]

for email in test_emails:
    if bloom_filter.check(email):
        if email not in emails:
            print(f"{email} is a false positive!")
        else:
            print(f"{email} is probably present!")
    else:
        print(f"{email} is definitely not present!")
