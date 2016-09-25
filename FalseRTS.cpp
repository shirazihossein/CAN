#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <iostream>

#include <net/if.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>

#include <linux/can.h>
#include <linux/can/raw.h>
#include <queue>          // std::queue
#include <thread>

using namespace std;

int s;
int read_can_port;
char ifname[] = "can1";
int nbytes;
struct sockaddr_can addr;
struct ifreq ifr;
struct can_frame frame_read;
std::queue<can_frame> QueueMessages;

char ECUAddress = 0x11;
char RTSPGN = 0xEC;
char DataTransferPGN = 0xEB;
int masker_send = 2147483648;
int numberOfRepeat = 3;


int open_port()
{
	if((s = socket(PF_CAN, SOCK_RAW, CAN_RAW)) < 0) {
		perror("Error while opening socket");
		return -1;
	}
	
	strcpy(ifr.ifr_name, ifname);
	ioctl(s, SIOCGIFINDEX, &ifr);
	
	addr.can_family  = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	printf("%s at index %d\n", ifname, ifr.ifr_ifindex);

	if(bind(s, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		perror("Error in socket bind");
		return -2;
	}
}


int read_port()
{
	int recvbytes = 0;
	recvbytes = read(s, &frame_read, sizeof(struct can_frame));
	return recvbytes;
}

int write_port(can_frame frame )
{
	return write(s, &frame, sizeof(struct can_frame));
}

void print_can_frame ( struct can_frame frame )
{
	printf(" %X \t ", frame.can_id );
	for (int i = 0 ; i < frame.can_dlc ; i++ )
		printf(" %02X " , frame.data[i] );

	printf("\n");
}


int send_CTS()
{
	struct can_frame frame;
	for ( int i = 0 ; i < numberOfRepeat ; i++ )
	{
		printf("Send CTS \n");

		frame.can_id  = masker_send | 0x00EC0011;
		frame.can_dlc = 8;
		frame.data[0] = 0x11;
		frame.data[1] = 0x07;
		frame.data[2] = 0x01;
		frame.data[3] = 0xFF;
		frame.data[4] = 0xFF;
		frame.data[5] = 0xEB;
		frame.data[6] = 0xFE;
		frame.data[7] = 0x00;
	}
	
	return write_port(frame);
}




void read_filter_mess(char sourceAddr)
{
	
	
	while ( read_port() ) 
	{
		read_port();
		char bytes[sizeof frame_read.can_id];
		std::copy(static_cast<const char*>(static_cast<const void*>(&frame_read.can_id)),static_cast<const char*>(static_cast<const void*>(&frame_read.can_id)) + sizeof frame_read.can_id,bytes);
        if ( bytes[1] == sourceAddr )
        {
			QueueMessages.push (frame_read);
			printf("One Message Added to queue \n");
		}
	}
	}

void processing_messages()
{
	char* dataPacket;
	int dataPacketLen = 0;
	bool IsArrayAllocated = false;
	while (1)
	{
		while (!QueueMessages.empty())
		{
			struct can_frame messFrame = QueueMessages.front();
			
			QueueMessages.pop();
			char bytes[sizeof messFrame.can_id];
			std::copy(static_cast<const char*>(static_cast<const void*>(&messFrame.can_id)),static_cast<const char*>(static_cast<const void*>(&messFrame.can_id)) + sizeof messFrame.can_id,bytes);
			
			if ( bytes[2] == RTSPGN && ! IsArrayAllocated )
			{
				send_CTS();
				printf("Get RTS \n");
				print_can_frame(messFrame);
				dataPacketLen = 7 * messFrame.data[3];
				dataPacket = new char[dataPacketLen];
				IsArrayAllocated = true;
				dataPacketLen = messFrame.can_dlc;
				printf("datapacketlen = %d" , dataPacketLen);
				
			}
			else if ( bytes[2] == RTSPGN && ! IsArrayAllocated )
			{
				printf("Get Second RTS \n");
				print_can_frame(messFrame);
				dataPacketLen = 7 * messFrame.data[3];
				dataPacket = new char[dataPacketLen];
				IsArrayAllocated = true;
				dataPacketLen = messFrame.can_dlc;
			}
			
			else if ( bytes[2] = DataTransferPGN )
			{
				printf("Get data packets \n");
				int offset =  (messFrame.data[0] - 1 ) * 7;
				for (int i = 0 ; i < 7 ; i++ )
					dataPacket[i + offset] = messFrame.data[i+1];
			}
			
			for (int i = 0 ; i < dataPacketLen  ; i++ )
				printf(" %02X " , dataPacket[i] );
			printf("\n");
		}
	}
	
	
	
	}
	
int send_request()
{
	struct can_frame frame;
	for ( int i = 0 ; i < numberOfRepeat ; i++ )
	{
		printf("Send Request \n");
		
		frame.can_id  = masker_send | 0x00EA0011;
		frame.can_dlc = 8;
		frame.data[0] = 0xEB;
		frame.data[1] = 0xFE;
		frame.data[2] = 0x00;
		frame.data[3] = 0x00;
		frame.data[4] = 0x00;
		frame.data[5] = 0x00;
		frame.data[6] = 0x00;
		frame.data[7] = 0x00;
		
	}
	
	return write_port(frame);
}
	 
	
	

int main(void)
{
	open_port();
	send_request();
	
	thread listner (read_filter_mess , ECUAddress);
	thread processor (processing_messages );

	listner.join();
	processor.join();

    
    return 0;
}

