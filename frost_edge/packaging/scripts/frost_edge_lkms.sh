#!/bin/bash
echo "Loading LKMs";
insmod /lib/modules/frost/FE_AD1939.ko;
insmod /lib/modules/frost/FE_AD7768_4.ko;	
insmod /lib/modules/frost/FE_PGA2505.ko;
insmod /lib/modules/frost/FE_TPA613A2.ko;