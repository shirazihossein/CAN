import SocketManager, time
import _thread
from Config import Config as cg


can_name = "can1"
strDes = "11"
socket = SocketManager.SocketManager(can_name);
first_RTS = "18ec1100"

false_RTS1 = "18EC1100"
false_RTS_data  = "10000000FFEBFE00"
data_len = 8



print ("#second step: waiting for engine to send a clera to send message")

cf= socket.GetMessage(can_name)
while (cf[0] != first_RTS):
	cf= socket.GetMessage(can_name)


#Third step: sending clear to send message for engine
socket.SendMessage(false_RTS1, data_len, false_RTS_data)

#Third step: sending clear to send message for engine
#socket.SendMessage(false_RTS, data_len, false_RTS_data)

#Third step: sending clear to send message for engine
#socket.SendMessage(false_RTS, data_len, false_RTS_data)
	

