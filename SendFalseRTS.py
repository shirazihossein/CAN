import socket
import struct
import sys
import binascii
import array
import SocketManager, sys, signal
import time


strDes = "11"

first_step = "00EA00" + strDes.upper()
first_step_data = "EBFE000000000000"

second_step = "18ec" + strDes + "00"

third_step = "00EC00" +  strDes.upper()
third_step_data  = "110701FFFFEBFE00"

forth_step = "18eb" + strDes + "00"
final_step = "00EC00" + strDes.upper()
final_step_data = "122C0007FFEBFE00"


try:
	socket = SocketManager.SocketManager(self.interface)
except Exception as inst:
	print ( "Error in first_step" )

while True:
			
	#second step: waiting for engine to send a clear to send message
	cf= socket.GetMessage(self.interface)
	while (cf[0] != second_step):
		cf= socket.GetMessage(self.interface)

			
	while True:
		#Third step: sending clear to send message for engine
		socket.SendMessage(third_step, data_len, third_step_data)
		print ("Send False RTS")

