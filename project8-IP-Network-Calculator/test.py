def main():
    ipAddressInput = input("Enter IP address, can include CIDR: ")
    
    try:
        inputSplit = ipAddressInput.split('/')
        print(inputSplit)
        cidrInput = inputSplit[1]
        print(cidrInput)
    except:
        pass

        
    if len(ipAddressInput.split('/')) > 1:
        print("You have inputted a CIDR!")

main()
