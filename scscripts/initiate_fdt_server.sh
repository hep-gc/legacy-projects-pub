#!/bin/bash

for i in `seq 54301 54315`;
do
   fdtServer -p $i &> /root/log/fdtserver$i.log & 
done
