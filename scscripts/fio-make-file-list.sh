#!/bin/bash 

rm ~/scscripts/fl/mlxl1.txt
rm ~/scscripts/fl/mlxl2.txt
rm ~/scscripts/fl/mlxl3.txt

for i in `seq 1 2`; do find /bulk/fusion$i -name "*.dat" >> ~/scscripts/fl/mlxl1.txt; done
for i in `seq 5 6`; do find /bulk/fusion$i -name "*.dat" >> ~/scscripts/fl/mlxl1.txt; done
for i in `seq 3 4`; do find /bulk/fusion$i -name "*.dat" >> ~/scscripts/fl/mlxl2.txt; done
for i in `seq 7 8`; do find /bulk/fusion$i -name "*.dat" >> ~/scscripts/fl/mlxl2.txt; done
for i in `seq 9 12`; do find /bulk/fusion$i -name "*.dat" >> ~/scscripts/fl/mlxl3.txt; done

rsync -av ~/scscripts/fl/ root@sc01.heprc.uvic.ca:~/scscripts/fl/
rsync -av ~/scscripts/fl/ root@sc02.heprc.uvic.ca:~/scscripts/fl/
rsync -av ~/scscripts/fl/ root@sc04.heprc.uvic.ca:~/scscripts/fl/
