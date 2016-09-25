import socket
import struct
import sys
import binascii

can_frame_fmt = "=IB3x8s"
can_frame_len = 16
scale_for_data = 16
masker_send = 2147483648
masker_get =	2147483647

class SocketManager:
	
	def __init__(self,interface):
		try:
			self.s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
			self.s.bind((interface,))
		except socket.error as e:
			#0errorcode = v[0]
			print (str(e))
			print('Error sending CAN frame')

	def __del__(self):
		self.s.close()

	def mask_send_Id(self, can_id ):
		can_id =hex( int(can_id,scale_for_data) | masker_send)[2:]
		return can_id
		
	def dissect_can_frame(self,frame):
		can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
		can_id = self.mask_get_Id(can_id)
		return (can_id, can_dlc, data[:can_dlc])
	
	def mask_get_Id(self, can_id ):
		return str(hex(can_id	& masker_get)[2:]).zfill(8)

	def SendMessage(self,can_id,data_len,data):
		data = data.ljust(16,'0')
		can_id = self.mask_send_Id( can_id)
		
		# it is not working ! I changed back this line
		#frame_message = bytearray([bytes(0) for x in range(13)])
		frame_message = bytearray(16)

#	cf, addr = s.recvfrom(can_frame_len)
	
	#creating id part
		frame_message[0] = bytearray.fromhex(can_id[6:8])[0]
		frame_message[1] = bytearray.fromhex(can_id[4:6])[0]
		frame_message[2] = bytearray.fromhex(can_id[2:4])[0]
		frame_message[3] = bytearray.fromhex(can_id[0:2])[0]
	
	#creating data_len part
		str_data_len = str(data_len)
		if len(str_data_len) < 2:
			str_data_len = "0" + str_data_len
		frame_message[4] = bytearray.fromhex(str_data_len)[0]
	
	#creating data part of message
		frame_message[8:] = bytearray.fromhex(data)
	
	#print (frame_message)
		self.s.send(frame_message)


	def GetMessage(self,can_name):
		cf, addr = self.s.recvfrom(16)
		return self.dissect_can_frame(cf)
