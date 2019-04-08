import sys
import socket
import subprocess
import json


def get_subnet_mask_from_number_of_significant_bits(s_bits):
    counter = s_bits

    j = 0
    tmp = ''
    while j < 4:
        i = 0
        while i < 8:
            if counter != 0:
                tmp += '1'
                counter -= 1
            else:
                tmp += '0'
            i += 1
        if j < 3:
            tmp += '.'
        j += 1

    return tmp


def get_subnet_mask(ip):
    proc = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if ip.encode() in line:
            break
    mask = proc.stdout.readline().rstrip().split(b':')[-1].replace(b' ', b'').decode()
    return mask


def dec2bin(x, n=0):
    return format(x, 'b').zfill(n)


def address_to_bin(address):
    numbers = address.split(".")
    binary = ""
    for i in numbers:
        binary = binary + (dec2bin(int(i), 8)) + "."
    binary = binary[:-1]
    return binary


def bin2dec(to_change):
    tmp = 0
    i = 7
    while i >= 0:
        tmp += int(to_change[7 - i]) * pow(2, i)
        i -= 1
    tmp = str(tmp)
    return tmp


def address_to_dec(to_change):
    dec = ""
    tab = to_change.split(".")
    for i in range(0, len(tab)):
        dec += bin2dec(tab[i]) + "."

    dec = dec[:-1]

    return dec


def get_address_ip_dec():
    if len(sys.argv) > 1:
        address_ip_with_mask = str(sys.argv[1])
        tmp = address_ip_with_mask.split("/")  # tmp[0] = ip
        address_ip = tmp[0]

    else:
        address_ip = socket.gethostbyname(socket.gethostname())

    return address_ip


def get_mask_bin(address_ip):
    if len(sys.argv) > 1:
        address_ip_with_mask = str(sys.argv[1])
        tmp = address_ip_with_mask.split("/")
        check_mask_two_digits(int(tmp[1]))
        sub_mask_bin = get_subnet_mask_from_number_of_significant_bits(int(tmp[1]))

    else:
        sub_mask_dec = get_subnet_mask(address_ip)
        sub_mask_bin = address_to_bin(sub_mask_dec)
        check_mask_bin(sub_mask_bin)

    return sub_mask_bin


# address_ip decimal
def check_address_ip_dec(address_ip):
    numbers = address_ip.split(".")

    check = 0
    counter = 0

    for i in numbers:
        counter = counter + 1
        if int(i) < 0 or int(i) > 255:
            check = 1

    if int(counter) != 4:
        check = 1

    if int(check) == 1:
        print "Incorrect address IP"
        return 1
    else:
        print "Correct address IP"
        return 0


# mask   two digits
def check_mask_two_digits(mask):
    if int(mask) > 32 or int(mask) > 32:
        print "Incorrect mask"
        return 1
    else:
        print "Correct mask"
        return 0


# mask binary
def check_mask_bin(mask):
    tab = mask.split(".")

    sum = 0
    sum += int(tab[0])
    sum += int(tab[1])
    sum += int(tab[2])
    sum += int(tab[3])

    if int(sum) > 44444444 or int(sum) < 0:
        print "Incorrect mask"
        return 1
    else:
        print "Correct mask"
        return 0


# address_ip_decimal       address ip decimal
# mask                      mask binary
def get_network_address(address_ip_decimal, mask):
    address_ip = address_to_bin(address_ip_decimal)

    network_address = ""

    i = 0
    while i < len(address_ip):
        if mask[i] == "1":
            network_address += address_ip[i]
            i += 1
        elif mask[i] == ".":
            network_address += "."
            i += 1
        else:
            network_address += "0"
            i += 1

    return network_address


# address_ip_dec        address ip decimal
# mask                  mask binary
def get_broadcast_address(address_ip_decimal, mask):
    address_ip = address_to_bin(address_ip_decimal)

    network_address = ""

    i = 0
    while i < len(address_ip):
        if mask[i] == "1":
            network_address += address_ip[i]
            i += 1
        elif mask[i] == ".":
            network_address += "."
            i += 1
        else:
            network_address += "1"
            i += 1

    return network_address


# address_ip_decimal    address ip decimal
def get_class(address_ip_decimal):
    adr_ec = address_ip_decimal.split(".")
    adr_dec_part = adr_ec[0]

    ip = dec2bin(int(adr_dec_part), 0)

    counter = 0
    i = 0
    while i < 4:
        if ip[i] == '1':
            counter += 1
        i += 1
    if counter == 0:
        return 'A'
    if counter == 1:
        return 'B'
    if counter == 2:
        return 'C'
    if counter == 3:
        return 'D'
    if counter == 4:
        return 'E'


def get_first_host_address(network_address):
    tab = network_address.split(".")
    tmp = tab[3]
    tmp = int(tmp)
    tmp += 1

    tab[3] = str(tmp).zfill(8)
    first_host_address = tab[0] + "." + tab[1] + "." + tab[2] + "." + tab[3]

    return first_host_address


def get_last_host_address(network_address):
    tab = network_address.split(".")
    tmp = tab[3]
    tmp = int(tmp)
    tmp -= 1

    tab[3] = str(tmp).zfill(8)
    last_host_address = tab[0] + "." + tab[1] + "." + tab[2] + "." + tab[3]

    return last_host_address


def max_host_quantity(broadcast_address_dec, network_address_dec):
    maximum_host_quantity = 1
    tmp = [0, 0, 0, 0]
    tab_broadcast = broadcast_address_dec.split(".")
    tab_network = network_address_dec.split(".")

    tmp[3] = int(tab_broadcast[3]) - int(tab_network[3])
    tmp[2] = int(tab_broadcast[2]) - int(tab_network[2])
    tmp[1] = int(tab_broadcast[1]) - int(tab_network[1])
    tmp[0] = int(tab_broadcast[0]) - int(tab_network[0])

    for i in range(len(tmp)):
        if int(tmp[i]) > 0:
            tmp[i] += 1

    for i in range(len(tmp)):
        if int(tmp[i]) > 0:
            maximum_host_quantity *= tmp[i]

    maximum_host_quantity -= 2
    return maximum_host_quantity


# write to JSON
data = []

address_ip_dec = get_address_ip_dec()
mask_bin = get_mask_bin(get_address_ip_dec())

# print address_ip_dec
# print mask_bin

check_address_ip_dec(address_ip_dec)
# addressIpDec       address ip decimal
# mask               mask binary
networkAddressBin = get_network_address(address_ip_dec, mask_bin)
print "Network address binary: " + networkAddressBin
data.append("Network address binary: " + networkAddressBin)

networkAddressDec = address_to_dec(networkAddressBin)
print "Network address decimal: " + networkAddressDec
data.append("Network address decimal: " + networkAddressDec)

networkClass = get_class(address_ip_dec)
print "Network class: " + get_class(address_ip_dec)
data.append("Network class: " + get_class(address_ip_dec))

print "Network mask binary: " + mask_bin
data.append("Network mask binary: " + mask_bin)

networkMaskDecimal = address_to_dec(mask_bin)
print "Network mask decimal: " + address_to_dec(mask_bin)
data.append("Network mask decimal: " + address_to_dec(mask_bin))

broadcastAddressBin = get_broadcast_address(address_ip_dec, mask_bin)
print "Broadcast address binary: " + broadcastAddressBin
data.append("Broadcast address binary: " + broadcastAddressBin)

broadcastAddressDec = address_to_dec(get_broadcast_address(address_ip_dec, mask_bin))
print "Broadcast address decimal: " + broadcastAddressDec
data.append("Broadcast address decimal: " + broadcastAddressDec)

print "First host address binary: " + get_first_host_address(networkAddressBin)
data.append("First host address binary: " + get_first_host_address(networkAddressBin))

firstHostAddress = address_to_dec(get_first_host_address(networkAddressBin))
print "First host address decimal: " + address_to_dec(get_first_host_address(networkAddressBin))
data.append("First host address decimal: " + address_to_dec(get_first_host_address(networkAddressBin)))

lastHostAddress = get_last_host_address(broadcastAddressBin)
print "Last host addres binary: " + get_last_host_address(broadcastAddressBin)
data.append("Last host addres binary: " + get_last_host_address(broadcastAddressBin))

print "Last host address decimal: " + address_to_dec(get_last_host_address(broadcastAddressBin))
data.append("Last host address decimal: " + address_to_dec(get_last_host_address(broadcastAddressBin)))

maxHostQuantityDecimal = str(max_host_quantity(broadcastAddressDec, networkAddressDec))
print "Max hosts quantity decimal: " + str(max_host_quantity(broadcastAddressDec, networkAddressDec))
data.append("Max hosts quantity decimal: " + str(max_host_quantity(broadcastAddressDec, networkAddressDec)))

maxHostQuantityBinary = str(dec2bin(max_host_quantity(broadcastAddressDec, networkAddressDec), 0))
print "Max hosts quantity binary: " + str(dec2bin(max_host_quantity(broadcastAddressDec, networkAddressDec), 0))
data.append("Max hosts quantity binary: " + str(dec2bin(max_host_quantity(broadcastAddressDec, networkAddressDec), 0)))

s = "."
data = {'address': []}
data['address'].append(
    {
        'Network address binary: ': networkAddressBin,
        'Network address decimal: ': networkAddressDec,
        'Network class: ': networkClass,
        'Network mask binary: ': mask_bin,
        'Network mask decimal: ': networkMaskDecimal,
        'Broadcast address binary: ': broadcastAddressBin,
        'Broadcast address decimal: ': broadcastAddressDec,
        'First host address: ': firstHostAddress,
        'Last host address: ': lastHostAddress,
        'Max hosts quantity decimal: ': maxHostQuantityDecimal,
        'Max hosts quantity binary: ': maxHostQuantityBinary,

    }
)

with open('data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
