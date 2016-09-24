#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <net/if.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>

#include <linux/can.h>
#include <linux/can/raw.h>
#include <queue>          // std::queue



int s;
int read_can_port;
char ifname[] = "can1";
int nbytes;
struct sockaddr_can addr;
struct ifreq ifr;
struct can_frame frame_read;


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
	printf("1");
	int recvbytes = 0;
	recvbytes = read(s, &frame_read, sizeof(struct can_frame));
	return recvbytes;
}

int write_port(can_frame *frame )
{
	
	//nbytes = write(s, &frame, sizeof(struct can_frame));
}

void print_can_frame ( struct can_frame frame )
{
	printf(" %X \t ", frame.can_id );
	for (int i = 0 ; i < frame.can_dlc ; i++ )
		printf(" %02X " , frame.data[i] );

	printf("\n");
}


int main(void)
{
    open_port();
	if ( read_port() ) 
	{
		print_can_frame(frame_read);
	}
	
	std::queue<can_frame> myqueue;
	printf("myqueue contains: " ) ;
	while (!myqueue.empty())
	{
		printf( " %d : " , myqueue.front() ) ;
		myqueue.pop();
	}
	
	
	
	/*

	
	while (1)
	{
		
	
	frame.can_id  = 0x1412;
	frame.can_dlc = 2;
	for (int i = 0 ; i < frame.can_dlc ; i++ )
		frame.data[i] = i;
	
	
	//write_port(*frame);
	}
	 
	 */
    
    return 0;
}
