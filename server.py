from socket import *    #some necessary imports
import sys, os
from pathlib import Path
from shutil import copyfile

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 65200
serverSocket.bind(('10.0.0.1',serverPort))  #binds server socket to own IP and port
serverSocket.listen(1)
connectionSocket, addr = serverSocket.accept() #establishes the connection to the host's socket

def doFileListing() -> str:
    filepath = Path(sys.argv[0]) #grabs the path of the server.py file
    dirpath = filepath.parent #zooms out to the parent directory
    filestring = ', '.join(os.listdir(dirpath.__str__())) #directly store this list in a string
    return '[' + filestring + ']' #output with aesthetic brackets

def copyOfFile(filetoCopy):
    copyfile(filetoCopy, 'Copy of ' + filetoCopy)
    return 'The file has been successfully copied!'

def renameFile(fileToRename, newName):
    os.rename(fileToRename, newName)
    return 'The file has been successfully renamed!'

def deleteFile(tobeDeleted):
    os.remove(tobeDeleted)
    return 'The file has been successfully deleted!'

while 1: #infinite loop, waits for requests
    commandMsg = connectionSocket.recv(1024)  # get message
    if(commandMsg == b'1'):
        listing = doFileListing()
        binList = listing.encode('ascii') #encodes the string-ified list into binary code to be sent back to host
        connectionSocket.sendall(binList) #sends the list to client
    elif(commandMsg == b'2'):
        filetoCopy = connectionSocket.recv(1024) #receives the name of the file to be copied
        copyOutput = copyOfFile(filetoCopy.decode('ascii')) #sends the name to the method and gets the success msg
        connectionSocket.sendall(copyOutput.encode('ascii')) #sends the encoded success msg over the socket
    elif(commandMsg == b'3'):
        filetoRename = connectionSocket.recv(1024)  # receives the name of the file to be renamed
        newFileName = connectionSocket.recv(1024) # receives the new name
        renOutput = renameFile(filetoRename.decode('ascii'), newFileName.decode('ascii'))  # sends the params to method, get success msg
        connectionSocket.sendall(renOutput.encode('ascii'))  # sends the binary success msg over the socket
    elif(commandMsg == b'4'):
        filetoDelete = connectionSocket.recv(1024)  # receives the name of the file to be deleted
        delOutput = deleteFile(filetoDelete.decode('ascii')) #sends the name to the method and gets the success msg
        connectionSocket.sendall(delOutput.encode('ascii')) #sends the binary success msg over the socket
    else:
        continue