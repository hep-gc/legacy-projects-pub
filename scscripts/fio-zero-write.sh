#!/bin/bash
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion1/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion1.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion2/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion2.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion3/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion3.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion4/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion4.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion5/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion5.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion6/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion6.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion7/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion7.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion8/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion8.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion9/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion9.txt &
java -cp ~/fdt.jar lia.util.net.common.DDCopy if=/dev/zero of=/bulk/fusion10/testfile bs=10M count=10240 rformat=M > /root/results/test1/fusion10.txt &
