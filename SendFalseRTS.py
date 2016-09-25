import SocketManager, time
from threading import Thread
from Config import Config as cg


can_name = "can1"
socket = SocketManager.SocketManager(can_name);

strDes = "11"
second_step = "18ec" + strDes + "00"

third_step = "00EC00" +  strDes.upper()
third_step_data  = "110701FFFFEBFE00"

print ("#second step: waiting for engine to send a clera to send message")

cf= socket.GetMessage(can_name)
while (cf[0] != second_step):
	cf= socket.GetMessage(can_name)


#Third step: sending clear to send message for engine
socket.SendMessage(third_step, data_len, third_step_data)
