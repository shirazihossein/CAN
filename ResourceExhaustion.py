import SocketManager, time
from threading import Thread
from Config import Config as cg


socket = SocketManager.SocketManager(cg.can_name);

#Sending request to the engine ECU
socket.SendMessage(cg.PGN1Req,cg.data_len,cg.requestData)
time.sleep(.1)
socket.SendMessage(cg.PGN2Req,cg.data_len,cg.requestData)


time.sleep(.1)
for i in range (255):
	print ("Sending CTS of PGN 1 : {}".format(cg.PGN1CTS) )
	socket.SendMessage(cg.PGN1CTS,8,cg.CTSData)
	
	print ("Sending CTS of PGN 2 : {}".format(cg.PGN2CTS))
	socket.SendMessage(cg.PGN2CTS,8,cg.CTSData)
	
	time.sleep(.5)
