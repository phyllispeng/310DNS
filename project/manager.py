from socket import *
import subprocess

found = 0
pass_str = ""
stdout_str=""
p_list = []

#set a default port  1203
mserverPort = 1203


mserverSocket = socket(AF_INET, SOCK_STREAM)
mserverSocket.bind(('', mserverPort))

mserverSocket.listen(1)
print "The manager sever is ready to receive"

#open the manager.in file and put all the read in lines into a list print all the element out

with open('manager.in', 'r') as infile:
    data = infile.read()
data_list = data.splitlines()

for element in data_list:
    print element
    print "--------------------------------------------"
#type_number the length of the data list will be used as a counter for the while loop to generate port numbers
type_number = len(data_list)


#make a counter c and while c is smaller than the data_list ,which contains all the types, keep generating port numbers by Popen the nameServer.py file
#put all port number together separate by space and make it to a stirng , update the counter c
c=0
while c< type_number:

    proc = subprocess.Popen(['python','-u','nameServer.py'],stdout=subprocess.PIPE)
    p_list.append(proc)
    line = proc.stdout.readline()
    stdout_str = stdout_str+" "+line.rstrip()
    c=c+1

stdout_str_list = stdout_str.split()
#put the type and port number together and make it to a stirng updat counter i
i=0
for dlist in data_list:
    pass_str = pass_str+"  "+data_list[i]+" "+stdout_str_list[i]
    i=i+1
print pass_str

try:

    connectionSocketm, maddr = mserverSocket.accept()
    connection_mesg = connectionSocketm.recv(1024)
    #recv message from the client, put them in a buffer and use if else statment to check the signal in the while loop below
    #send signal back with messages
    if connection_mesg == "CONNECTSUCCESS":
        connectionSocketm.send("CONNECTED"+pass_str)

    while 1:

        minput =connectionSocketm.recv(1024)
        if len(minput) == 0:
            print "Connection closed"
            break

        minputSentence = minput.split()

        if minputSentence[0] == "TYPE":
            s=0
            for data in data_list:
                if data == minputSentence[1]:
                    print "find the type"
                    #set a singal found, if found the value set found to 1 and break else found is 0
                    found = 1
                    break
                else:
                    s=s+1
                    found = 0

            if found == 1:
                connectionSocketm.send("TYPESUCCESS "+minputSentence[1]+" "+stdout_str_list[s])
            else:
                connectionSocketm.send("TYPEFAIL")
        elif minputSentence[0]=="EXITM":
            print "this will stop the client connect with the manager server"
            connectionSocketm.send("MTIXE Manager Server >>> Bye... Happy Holiday ... Have a wonderful break ...")

        elif minputSentence[0] == "EXIT":
            print "this should stop the TCP server"

except Exception as e:
    print e
finally:
    print "close every nameServer"
    for p in p_list:
        p.terminate()
    connectionSocketm.close
