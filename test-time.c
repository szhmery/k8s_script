#include <netinet/in.h>
#include <stdlib.h>
#include <string.h>
#include<time.h>
#include<sys/time.h>
#include<sys/types.h>

#define NUM_USEC_PER_SEC 1000000

#define UBR_D31TS_TO_TGC(d31_ext_timestamp)     \
    (d31_ext_timestamp >> 9)

#define UBR_D31TS_TO_D30TS(d31_ext_timestamp) \
    (UBR_D31TS_TO_TGC(d31_ext_timestamp) & 0xFFFFFFFF)

uint32_t ptp_to_docsis_timestamp (uint64_t sec, uint32_t nsec)
{
#define BILLION         1000000000ULL
    return (uint32_t)((((sec & 0x3FFFF) * BILLION + nsec) << 5) / 3125);
}

int main(){

    uint32_t sec = 1547694306;
    uint32_t usec = 817291;
    uint32_t egress_sec = 1551177581;
    uint32_t egress_usec = 784500;
    uint64_t d31_timestamp;
    uint32_t timestamp,bwr_tgc;
    uint64_t total_time = (uint64_t)sec * NUM_USEC_PER_SEC + (uint64_t)usec;
    uint64_t egress_docsis_timestamp;
    struct timespec ts;
    int i;
    //for(i=0;i<2;i++){
	clock_gettime(CLOCK_REALTIME, &ts);
	d31_timestamp = (uint64_t)ptp_to_docsis_timestamp((uint64_t)ts.tv_sec, (uint32_t)ts.tv_nsec);
//	d31_timestamp = (uint64_t)ptp_to_docsis_timestamp((uint64_t)egress_sec, (uint32_t)(egress_usec*1000));
        //egress_docsis_timestamp = (uint32_t)((((egress_sec & 0x3FFFF) * BILLION + (egress_usec*1000)) << 5) / 3125);
        //d31_timestamp = (uint64_t)((egress_docsis_timestamp << 5) / 3125);//us->ns
        d31_timestamp = (d31_timestamp & 0xFFFFFFFF) << 9;
        timestamp =  UBR_D31TS_TO_D30TS(d31_timestamp);
        bwr_tgc =  UBR_D31TS_TO_TGC(d31_timestamp);


	printf("ts.tv_sec=%ld, ts.tv_nsec = %d,egress_docsis_timestampc=%ld, d31_timestamp=%ld, timestamp=%d, bwr_tgc=%d\n",
        ts.tv_sec, ts.tv_nsec,egress_docsis_timestamp,d31_timestamp,timestamp,bwr_tgc);
	usleep(1000);
    //}
    //printf("usec=%d\n",usec);
    //printf("total_time=%ld\n",total_time);
    return 0;

}



