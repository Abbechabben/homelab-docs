
from scapy.all import *
import time
import datetime


def createPacket(to="192.168.1.1", destp=53, sorp=55555,flag="S",snum=521):
    print("Starting to Create Packet")
    packet = IP(dst=to)/TCP(dport=destp, sport=sorp, flags=flag,seq=snum) #Creating a packet with the different header options of the TCP & IP headers
    print("Packet Created")
    return packet

def sendPacket(packet):
    #Scappy opens a sniffer and sees everything crossing my NIC thats why I see e.g 4packets, 0 answers, remaining: 1 packet in the terminal
    response = sr1(packet,timeout=.001) 
    return response

def readresponse(response):
    
    
    if response is None or response.haslayer(ICMP): #Runned into problem where I received ICMP packets back when I tried to send packets, had to add hashlayer(ICMP ) to filter them out
        return False
    
    elif response[TCP].flags == "SA": #Syn/Ack, means the port is open because it responds to my Syn request & can establish a connecetion with me 
        #Port is open!!! 
        return True
    else:
        return False # If receiving something like for example RA (Meaning the port is not open)

def usrinpt(): #Did not have the energy for developing fully... Will be continued... 
    while True: 
        portRange = input("Which port Range do you want to scan (e.g 10000), for all press enter: ")
        if portRange.isdigit() and int(portRange) > 0 and int(portRange) < 65537:
            portRangeH = int(portRange)
            portRangeL = 1
            break
        elif portRange == "":
            portRangeH = 65536
            portRangeL = 1
            break
        else:
            print("Please insert a number between 1-65536!")
    return portRangeL, portRangeH #will be a range instead of just a low = 1 and high = inputted number



def main():
    portList = []#To add all of them ports
    
    portRangeL, portRangeH = usrinpt()
    startTime = datetime.datetime.now()
    print(startTime)
    for destp in range(portRangeH-portRangeL+1):
        print(destp+portRangeL)
        packet = createPacket(destp=portRangeL+destp)
        #Get the response
        response = sendPacket(packet=packet)
        #Check if port is open
        accessable = readresponse(response=response)
        if accessable == True: 
            # Add port to this particular IP (IP ranges will be added later...)
            portList.append(packet[TCP].dport)
    stopTime = datetime.datetime.now()
    totalTime = stopTime-startTime
    print(totalTime, portList)
        

if __name__ == "__main__":
    main()
