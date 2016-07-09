from socket import *

serverPort = 0
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
#generate a random port and print out
addr, port = serverSocket.getsockname()
serverSocket.listen(1)
print port
#print'The sever is ready to receive'

db_list=[]
found_it = 0

try:
    connectionSocket, addr = serverSocket.accept()
    while 1:
        sentence = connectionSocket.recv(1024)
        inputSentence = sentence.split(' ', 1)

        #get the message that send by the client and put into a string sentence
        #if else statements that checkes the client signals
        #send signals and message back
        # <name> <type>
        if inputSentence[0]  == "DEL":

            if len(db_list) == 0:
                connectionSocket.send("FAIL")
            else:
                for db in db_list:
                    db_element = db.split()
                    db_compare = db_element[0]+' '+db_element[2]

                    if db_compare == inputSentence[1]:
                        db_list.remove(db)
                        db_whole = db_element[0]+' '+db_element[1]+' '+db_element[2]
                        #set a singal found, if found_it the value set found to 1 and break else found is 0
                        found_it = 1
                        break
                    else:
                        found_it = 0

                if found_it == 1:
                    #print "should success "
                    print found_it
                    connectionSocket.send("DELSUCCESS " + db_whole)
                else:
                    #print "its fial should in else "
                    print found_it
                    connectionSocket.send("FAIL")

        # put <name> <value> <type>
        elif inputSentence[0]  == "PUT":
            db_list.append(inputSentence[1])
            print db_list
            connectionSocket.send("ADDSUCCESS "+inputSentence[1])
        # get <name> <type>
        elif inputSentence[0] == "GET":
            if len(db_list) == 0:
                connectionSocket.send("FAIL")
            else:
                #   0      1       2
                # <name> <value> <type>
                for db in db_list:
                    db_element = db.split()
                    db_compare = db_element[0]+' '+db_element[2]

                    if db_compare == inputSentence[1]:
                        db_whole = db_element[0]+' '+db_element[1]+' '+db_element[2]
                        #set a singal found, if found_it the value set found to 1 and break else found is 0
                        found_it = 1
                        break
                    else:
                        found_it = 0

                if found_it == 1:
                    connectionSocket.send("GETSUCCESS "+db_whole)
                else:
                    connectionSocket.send("FAIL")

        # print out all database
        elif inputSentence[0] == "BROWSE":
            if len(db_list) == 0:
                connectionSocket.send("FAIL")
            else:
                browse_mesg =  "ESWORB"
                i=0 #counter for for loop
                for db in db_list:
                    browse_mesg=browse_mesg+" , "+db_list[i]
                    i=i+1
                connectionSocket.send(browse_mesg)
            print "browse option"

        elif inputSentence[0]  == "EXIT":
            stop_client = "TIXE Server >>> Bye... Happy Holiday ... Have a wonderful break ..."
            connectionSocket.send(stop_client)
            print "this will stop the client"

        else :
            invalid_command = "IC"
            connectionSocket.send(invalid_command)
            print "invalid command"

except Exception as e:
    print e
    pass
