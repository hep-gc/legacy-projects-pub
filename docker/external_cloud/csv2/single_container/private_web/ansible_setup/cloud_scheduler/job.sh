Universe   = vanilla
Executable = job.exec
Arguments  = 7 25
 dir           = $ENV(HOME)/logs
#dir           = /var/tmp/apf-logs/rolf-logs                                                                                                                                                                                                  
output        = $(dir)/$(Cluster).$(Process).out
error         = $(dir)/$(Cluster).$(Process).err
log           = $(dir)/$(Cluster).$(Process).log
priority       = 10
Requirements = group_name =?= "csv2-group" && TARGET.Arch == "x86_64"
should_transfer_files = YES
when_to_transfer_output = ON_EXIT

request_cpus = 1
request_memory = 10
request_disk = 20

# +VMInstanceType = "cc-west:c1-7.5gb-30,cc-east:c2-7.5gb-92,chameleon:m1.medium"                                                                                                                                                             
# +VMInstanceType = "cc-east-a:c2-7.5gb-92"                                                                                                                                                                                                   
# +VMInstanceType = "cc-west-a:c1-7.5gb-30"                                                                                                                                                                                                   

# +VMUserData = "/home/seuster/TestCondor/ssh_key.yaml:cloud-config,/home/seuster/TestCondor/core.yaml:cloud-config,/home/seuster/TestCondor/certs.yaml:cloud-config,/home/seuster/TestCondor/benchmark.yaml:cloud-config,/home/seuster/TestCondor/default.yaml.j2:cloud-config,/home/seuster/TestCondor/iaas.yaml:cloud-config,/home/seuster/TestCondor/monitoring.yaml:cloud-config,/home/seuster/TestCondor/cernvm-data.txt:ucernvm-config"                                             

queue 1
