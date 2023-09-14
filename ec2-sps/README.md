ec2-sps
=======
A service to filter aggregate EC2 spot prices  

install python client tool:

1: git clone https://github.com/hep-gc/ec2-sps.git

usage:

1: cd from directory you cloned the project cd \<ec2-sps clone directory\>/ecs-sps/src/client

2: python SpotPriceServiceClient -h 

note: 

the client needs to know where the sps sevice is. It is currently using a service avail. on glint.heprc.uvic.ca:9363. You can change this in the spot_price_api.cfg file.


