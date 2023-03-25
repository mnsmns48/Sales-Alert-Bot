our_price = int()
apple_ord = dict()
xiaomi_ord = dict()

with open('Shippers/apple.txt', 'r', encoding='utf8') as f:
    file = f.read()

apple_order_list = file.split('\n')
for i in apple_order_list:
    k = i.split(' ')
    if int(k[-1]) in range(10000, 20000):
        our_price = int(k[-1]) + 1500
    if int(k[-1]) in range(20000, 30000):
        our_price = int(k[-1]) + 2500
    if int(k[-1]) in range(30000, 40000):
        our_price = int(k[-1]) + 3000
    if int(k[-1]) in range(40000, 50000):
        our_price = int(k[-1]) + 3500
    if int(k[-1]) in range(50000, 100000):
        our_price = int(k[-1]) + 5000
    if int(k[-1]) in range(100000, 300000):
        our_price = int(k[-1]) + 8000
    y = [(" ".join(k[:-1]), our_price)]
    apple_ord.update(y)


with open('Shippers/xiaomi.txt', 'r', encoding='utf8') as f2:
    file2 = f2.read()

xiaomi_order_list = file2.split('\n')

for i in xiaomi_order_list:
    k = i.split(' ')
    if k[-2] == 'EU' or k[-2] == 'RU':
        k.remove(k[-2])
    if int(k[-1]) in range(4000, 9000):
        our_price = int(k[-1]) + 1500
    if int(k[-1]) in range(9000, 20000):
        our_price = int(k[-1]) + 2500
    if int(k[-1]) in range(20000, 70000):
        our_price = int(k[-1]) + 4000
    y = [(" ".join(k[:-1]), our_price)]
    xiaomi_ord.update(y)
