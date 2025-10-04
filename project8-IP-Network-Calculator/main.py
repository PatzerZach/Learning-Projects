from math import log2

def shortMethod(ip, mask, cidr):
    maskSplit = mask.split('.')
    ipSplit = ip.split('.')

    subnetID = ipSplit[:]

    cidrMap = {'octet_2':[9, 10, 11, 12, 13, 14, 15, 16],
           'octet_3':[17, 18, 19, 20, 21, 22, 23, 24],
           'octet_4':[25, 26, 27, 28, 28, 30],
           'magic_number':[128, 64, 32, 16, 8, 4, 2, 1],
           'sub_mask_for_int_octet':[128, 192, 224, 240, 248, 252, 254, 255]}

    for i,key in enumerate(['octet_2', 'octet_3', 'octet_4']):
        if any(cidr == c for c in cidrMap.get(key, [])):
            splitList = key.split('_')
            interestingOctet = int(splitList[1])
            magicNumberList = cidrMap['magic_number']
            magicNumber = magicNumberList[i]
            subIntList = cidrMap['sub_mask_for_int_octet']
            subIntOctet = subIntList[i]
 
    k = 0
    magicNumberRange = [0]
    while k < 255:
        k += magicNumber
        magicNumberRange.append(k)

    originalNearestDistance = 1000
    idx = 0
    for m,n in enumerate(magicNumberRange):
        if (int(ipSplit[interestingOctet-1]) - int(n)) < originalNearestDistance and (int(ipSplit[interestingOctet-1]) - int(n)) >= 0:
            originalNearestDistance = int(ipSplit[interestingOctet-1]) - int(n)
            idx = m

    subnetIdInterestingOctet = int(magicNumberRange[idx])
    subnetID[interestingOctet-1] = subnetIdInterestingOctet


    broadcastAddress = subnetID[:]

    broadcastCalculation = int(broadcastAddress[interestingOctet-1]) + int(magicNumber) - 1
    broadcastAddress[interestingOctet-1] = broadcastCalculation

    firstHost = subnetID[:]
    firstHostCalculation = int(firstHost[3]) + 1
    firstHost[3] = firstHostCalculation

    lastHost = broadcastAddress[:]
    lastHostCalculation = int(lastHost[3]) - 1
    lastHost[3] = lastHostCalculation

    return subnetID, broadcastAddress, firstHost, lastHost

def longMethod(ip, mask):
    maskSplit = mask.split('.')
    ipSplit = ip.split('.')

# SUBNET ID PORTION

    subnetID = []

    for i,j in enumerate(maskSplit):
        if int(j) == 255:
            subnetID.append(int(ipSplit[i]))
        elif int(j) == 0:
            subnetID.append(0)
        else:
            interestingOctet = i
            magicNumber = 256 - int(j)
            subnetID.append(-1)

    k = 0
    magicNumberRange = [0]
    while k < 255:
        k += magicNumber
        magicNumberRange.append(k)

    originalNearestDistance = 1000
    idx = 0
    #originalNearestDistance = []
    #idx = []
    for m,n in enumerate(magicNumberRange):
        if (int(ipSplit[interestingOctet]) - int(n)) < originalNearestDistance and (int(ipSplit[interestingOctet]) - int(n)) >= 0:
            originalNearestDistance = int(ipSplit[interestingOctet]) - int(n)
            idx = m

    subnetIdInterestingOctet = int(magicNumberRange[idx])
    subnetID[interestingOctet] = subnetIdInterestingOctet

# BROADCAST ADDRESS PORTION

    broadcastAddress = []

    for y,z in enumerate(maskSplit):
        if int(z) == 255:
            broadcastAddress.append(int(subnetID[y]))
        elif int(z) == 0:
            broadcastAddress.append(255)
        else:
            interestingBroadcastAddress = y
            magicBroadcastAddress = 256 - int(z)
            subnetBroadcastID = int(subnetID[y])
            finalOctetFinal = subnetBroadcastID + magicBroadcastAddress - 1
            broadcastAddress.append(finalOctetFinal)

    firstHost = subnetID[:]
    firstHost[-1] += 1

    lastHost = broadcastAddress[:]
    lastHost[-1] -= 1

    return subnetID, broadcastAddress, firstHost, lastHost, magicNumber


def numberOfSubnets(magicNumber):

    hostBits = log2(magicNumber)
    borrowedBits = 8 - hostBits
    totalSubnets = 2 ** borrowedBits

    return totalSubnets


def hostsEachSubnet(magicNumber):

    usableHosts = magicNumber - 2 # Subtracting two to remove both Subnet ID and Broadcast Address
    
    return usableHosts


def calculateSubnetFromCIDR(cidr):
    binaryList = []
    for i in range(cidr): # if input is 24 then this would be 0 to 23
        binaryList.append(1)
    if len(binaryList) < 32:
        numberOfZeroes = 32 - len(binaryList)
    for j in range(numberOfZeroes):
        binaryList.append(0)

    binaryValues = [128, 64, 32, 16, 8, 4, 2, 1]

    binaryListWithDecimals = []

    for k in range(0, len(binaryList), 8):
        chunk = binaryList[k:k + 8]
        binaryListWithDecimals.append(chunk)

    subnetMaskValues = []

    for l in binaryListWithDecimals:
        currentValue = 0
        for m,n in enumerate(l):
            if n == 1:
                currentValue += binaryValues[m]
            else:
                currentValue += 0
        subnetMaskValues.append(currentValue)

    finalSubnetMask = ".".join(map(str, subnetMaskValues))
    print(finalSubnetMask)
    return finalSubnetMask


def calculateCIDRFromSubnet(subnet):
    binaryValues = [128, 64, 32, 16, 8, 4, 2, 1]

    octet = subnet.split('.')

    addedTimes = 0
    for i in octet:
        currentValue = 0
        for j,k in enumerate(binaryValues):
            if currentValue != int(i):
                currentValue += binaryValues[j]
                addedTimes += 1

    finalOutput = f"/{addedTimes}"

    return finalOutput


def main():
    ipAddressInput = input("\nEnter IP address, can include CIDR: ")
    
    inputSplit = ipAddressInput.split('/')

    if len(inputSplit) > 1:
        print("You have inputted a CIDR!")
        cidrInput = int(inputSplit[1])
        subnet = calculateSubnetFromCIDR(cidrInput)
    else:
        subnet = input("Please enter your subnet mask: ")
        cidrViewInput = calculateCIDRFromSubnet(subnet)
        cidrInput = int(cidrViewInput[1:])
        cidrQuestionInput = input("Would you like to see the CIDR of this subnet (y/n)? ")
        if cidrQuestionInput == 'y':
            print(f"\nCIDR Format: {cidrInput}")
        
    

    subnetID, broadcastAddress, firstHost, lastHost, magicNumber = longMethod(ipAddressInput, subnet)


    totalSubnets = numberOfSubnets(magicNumber)
    hostsPerSubnet = hostsEachSubnet(magicNumber)
    totalHosts = totalSubnets * hostsPerSubnet

    print("\n\n========== Basic Information ==========")
    print(f"\nTotal Number of Hosts: {int(totalHosts)}")
    print(f"Total Number of Subnets: {int(totalSubnets)}")
    print(f"Usable Hosts Per Subnet: {int(hostsPerSubnet)}")

    subnetID = ".".join(map(str, subnetID))
    broadcastAddress = ".".join(map(str, broadcastAddress))
    firstHost = ".".join(map(str, firstHost))
    lastHost = ".".join(map(str, lastHost))

    print("\n\n========== Long Calculation Method ==========")
    print(f"\nSubnet ID: {subnetID}")
    print(f"Broadcast Address: {broadcastAddress}")
    print(f"First Host: {firstHost}")
    print(f"Last Host: {lastHost}")
        
    subnetID, broadcastAddress, firstHost, lastHost = shortMethod(ipAddressInput, subnet, cidrInput)

    subnetID = ".".join(map(str, subnetID))
    broadcastAddress = ".".join(map(str, broadcastAddress))
    firstHost = ".".join(map(str, firstHost))
    lastHost = ".".join(map(str, lastHost))

    print("\n\n========== Short Calculation Method ==========")
    print(f"\nSubnet ID: {subnetID}")
    print(f"Broadcast Address: {broadcastAddress}")
    print(f"First Host: {firstHost}")
    print(f"Last Host: {lastHost}\n")

if __name__ == "__main__":
    main()
