#!/bin/bash

for i in `seq 5 8`;
do
  #numactl --cpunodebind=1 --membind=1 java -Dfdt.rQueueM=5 -Dfdt.wQueueM=60 -jar /opt/fdt/fdt.jar  -c 10.0.1.171 -bs 2M -P 10 -rCount 40 -p 54322  -wCount 40 -fl ~/fl/fl$i -loop -pull -d / > ~/results/card$i &
  echo "numactl --cpunodebind=1 --membind=1 java -Dfdt.rQueueM=5 -Dfdt.wQueueM=60 -jar /opt/fdt/fdt.jar  -c 10.0.1.171 -bs 2M -P 10 -rCount 40 -p 54322  -wCount 40 -fl ~/fl/fl$i -loop -pull -d / > ~/results/card$i &" 
done

