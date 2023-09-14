#!/bin/bash

echo "3 and 4"
cp /bulk/fusion1/050Gfile{7..9}.dat /bulk/fusion3/. & 
cp /bulk/fusion2/050Gfile{7..9}.dat /bulk/fusion4/.
sleep 60
echo "5 6 7 8"
cp /bulk/fusion1/050Gfile{7..9}.dat /bulk/fusion5/. &
cp /bulk/fusion2/050Gfile{7..9}.dat /bulk/fusion6/. &
cp /bulk/fusion3/050Gfile{7..9}.dat /bulk/fusion7/. &
cp /bulk/fusion4/050Gfile{7..9}.dat /bulk/fusion8/.
echo "9 10 11 12"
cp /bulk/fusion1/050Gfile{7..9}.dat /bulk/fusion9/. &
cp /bulk/fusion2/050Gfile{7..9}.dat /bulk/fusion10/. & 
cp /bulk/fusion3/050Gfile{7..9}.dat /bulk/fusion11/. & 
cp /bulk/fusion4/050Gfile{7..9}.dat /bulk/fusion12/.
