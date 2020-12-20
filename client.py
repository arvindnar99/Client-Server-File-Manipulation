from socket import *
SERV = '10.0.0.1'  # The server IP
SENDPORT = 65200   # Server port to send data to/rcv data from

s = socket(AF_INET, SOCK_STREAM) #create socket to send data over
s.connect((SERV, SENDPORT))  # estab connection with server
while 1: #infinite loop, waits for inputs
    print('Ready to serve... Input 1 for file listing, 2 for copy, 3 for rename, or 4 for delete')
    inputmsg = input('Enter the number now: ')

    if(inputmsg != '1' and inputmsg != '2' and inputmsg != '3' and inputmsg != '4'): #if the input is improper, err out and loop back to start
        print('Incorrect input!: ' + inputmsg + ' Try again, just input a number 1 through 4')
        continue
    inputmsgBit = inputmsg.encode('ascii')  # puts our verified input into binary to be sent through the connection
    s.sendall(inputmsgBit) #sends the verified bit

    if(inputmsg == '2'): #these if statements handle extra input for instructions that require more input
        filetoCopy = input('What file would you like to copy?: ')
        s.sendall(filetoCopy.encode('ascii')) #sends the bytes representing the file to copy
    elif(inputmsg == '3'):
        filetoRename = input('What file would you like to rename?: ')
        s.sendall(filetoRename.encode('ascii'))  # sends the bytes representing the file to rename
        newName = input('What would you like to rename that file to?: ')
        s.sendall(newName.encode('ascii')) #sends the bytes representing the new name
    elif(inputmsg == '4'):
        filetoDelete = input('What file would you like to delete?: ')
        s.sendall(filetoDelete.encode('ascii')) #sends the bytes representing the file to delete

    data = s.recv(1024) #gets the results of the operation from server
    print(data.decode('ascii')) #outputs decoded string return data to host terminal