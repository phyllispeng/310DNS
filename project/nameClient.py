from socket import *

#connect to manager server
serverPort_str = raw_input('To connect to Manager Server nter the <host name: localhost> & <port number: 1203> >>> ')
input_list = serverPort_str.split()
serverName = input_list[0]
serverPort = int(input_list[1] )

mclientSocket = socket(AF_INET, SOCK_STREAM)
mclientSocket.connect((serverName, serverPort))

# send CONNECTSUCCESS to get the list of port number and types
mclientSocket.send("CONNECTSUCCESS")
manager_type = mclientSocket.recv(1024)
manager_type_list = manager_type.split('  ')
tlist_len = len(manager_type_list)

i = 1

# Print out all the types and the port linked with the types with a counter i
# Start from position 0
while i < tlist_len:
    print "\n" + manager_type_list[i]
    i=i+1

#boolean value c handles the loop that runs both manager and nameServer
c= True
#signal that will change c to false and jump out from while loop c end the manager server
sig_c =0
while c is True:

#boolean value b handles the loop that runs manager server to nameClient
    b=True
    while b is True:
        #prompt
        print "\n*Enter help to see the Manager Server Command List*"
        input_mcmd = raw_input('Manager >>> ')
        input_mcmd_list = input_mcmd.split()
        input_len = len(input_mcmd_list)
        #if else statement check input messgae and check if input is valid
        if input_mcmd_list[0] == "type":
            #if type have more than 2 arguments then invalid input
            if input_len < 2:
                print "Invalid input"

            mclientSocket.send("TYPE "+input_mcmd_list[1])
        elif input_mcmd_list[0] == "help":
            #if help have more than 1 argument then invalid input
            if input_len > 1:
                print "Invalid input"

            print "                                Manager Server Command List                                           "
            print "======================================================================================================"
            print "Command      Fomart<>                       Description                                               "
            print "======================================================================================================"
            print "help         help                           used to list all the commands                             "
            print "type         type <type name>               used to select a type that list by manager               "
            print "exit         exit                           used to terminate the current TCP connection             "
            print "======================================================================================================"
            continue
        elif input_mcmd_list[0] == "exit":
            #if exit have more than 1 argument then invalid input
            if input_len > 1:
                print "Invalid input"
            mclientSocket.send("EXITM ")
        else:
            print "Invalid input"
            continue
        #recive from the manager server
        manager_reply = mclientSocket.recv(1024)
        manager_reply_list = manager_reply.split()
        manager_reply_list_bye = manager_reply.split(' ',1)

        # if else statement check the return signals from the server

        if manager_reply_list[0] == "TYPESUCCESS":
            # if TYPESUCESS print out the Connected to the server of type with type name
            # and With port number follows by the port number
            print "Connected to the server of type --- " +manager_reply_list[1]
            print "With port number ==== "+manager_reply_list[2]
            b=False
        elif manager_reply_list[0] == "TYPEFAIL":
            # if TYPEFAIL means cannot find the type, therefore print out No such type
            print "No such type"
            continue
        elif manager_reply_list[0] == "MTIXE":
            print manager_reply_list_bye[1]
            #exit the manager server set c while loop's signal to 1
            sig_c=1
            b=False

    #check if signal is 1 if yes set c to false and back to the top of the loop and end the whole loop close the
    #socket
    if sig_c == 1:
        c=False
        continue
    #connect to regular server
    input_serverPort = int(manager_reply_list[2]) #gonna change it soon
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName,input_serverPort))

    #boolean value a that handles the loop of nameServer
    a = True

    while a is True:
        print "\n*Enter help to see the Name Server Command List*"
        input_cmd = raw_input ('Uggghhh >>> ')


        input_cmd_list = input_cmd.split(' ',1)
        input_cmd_len = len(input_cmd_list)
        #get input from command line and send to the server
        #if else statement check the input values and send signals to the nameSever
        if input_cmd_list[0]  == "help":
            #if help have more than 1 argument then invalid input
            if input_cmd_len > 1:
                print "Invalid input"
                continue
        #sentence = "HELP"
            print "                                   Name Server Command List                                           "
            print "======================================================================================================"
            print "Command      Fomart<>                       Description                                               "
            print "======================================================================================================"
            print "help         help                           used to list all the commands                             "
            print "put          put <name> <value> <type>      used to add name records to the name servece database     "
            print "get          get <name> <type>              used to send a query to the server database               "
            print "del          del <name> <type>              used to remove a name record from the database            "
            print "browse       browse                         used to retrieve all current name records in the database "
            print "done         done                           used to terminates the current TCP connection             "
            print "======================================================================================================"
            continue

        # put <name> <value> <type>
        elif input_cmd_list[0] == "put":
            #if put have more than 4 arguments then invalid input
             if input_cmd_len > 4:
                print "Invalid input"
             sentence = "PUT "+input_cmd_list[1]
             clientSocket.send(sentence)

        # get <name> <type>
        elif input_cmd_list[0] == "get":
            #if get have more than 3 arguments then invalid input
             if input_cmd_len > 3:
                print "Invalid input"
             sentence ="GET "+ input_cmd_list[1]
             clientSocket.send(sentence)

        # print out all database
        elif input_cmd_list[0] == "browse":
            #if browse have more than 1 argument then invalid input
            if input_cmd_len > 1:
                print "Invalid input"
            sentence = "BROWSE"
            clientSocket.send(sentence)

        # del <name> <type>
        elif input_cmd_list[0] == "del":
            #if del have more than 3 arguments then invalid input
            if input_cmd_len > 3:
                print "Invalid input"
            sentence = "DEL "+input_cmd_list[1]
            clientSocket.send(sentence)
        #done
        elif input_cmd_list[0] == "done":
            #if done have more than 1 argument then invalid input
            if input_cmd_len > 1:
                print "Invalid input"
            sentence = "EXIT"
            clientSocket.send(sentence)
        #invalid command
        else:
            sentence = "IC"
            clientSocket.send(sentence)
        #recv from the server
        modifiedSentence = clientSocket.recv(1024)
        cmd_list = modifiedSentence.split(' ',1)

        # if else statement check the return signals from the server
        if cmd_list[0] == "TIXE":
            print cmd_list[1]
            #exit from the nameServer and set a to false jump out of the loop and close the socket
            a = False
        # if FAIL pring out fail invalid argument
        elif cmd_list[0] == "FAIL":
            print "! FAIL - INVALID ARGUMENT !"
            continue
        # if put oprtion successed print added data
        elif cmd_list[0] == "ADDSUCCESS":
            print "\nServer >>> Added data: "+ cmd_list[1]
            continue
        # if delete option successed print deleted data
        elif cmd_list[0] == "DELSUCCESS":
            print "\nServer >>> Deleted data: "+cmd_list[1]
            continue
        # if get option successed print got data
        elif cmd_list[0] == "GETSUCCESS":
            print "Server >>> Got data: "+cmd_list[1]
        # if input is invalid print out invalid command
        elif cmd_list[0]== "CI":
            print "Server >>> Invalid Command"
            continue
        # if browse option successed print out the list of data
        elif cmd_list[0] == "ESWORB":
            print_out = cmd_list[1].split(',')
            print "\n===================="
            print "      Database      "
            print "===================="
            for element in print_out:
                print element
            print "\n====================\n"
        # if get other things send back print invalid
        else:
            print "Invalid"
            continue

    clientSocket.close()

mclientSocket.close()
