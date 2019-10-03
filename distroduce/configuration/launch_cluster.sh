#!/bin/bash
aws emr create-cluster \
--applications Name=Hadoop Name=Hive Name=Spark \
--ec2-attributes '{"KeyName":"joshua-IAM-keypair","InstanceProfile":"EMR_EC2_DefaultRole","SubnetId":"subnet-0034e615b047fd112","EmrManagedSlaveSecurityGroup":"sg-08e546ae27d86d6a3","EmrManagedMasterSecurityGroup":"sg-08e546ae27d86d6a3"}' \
--release-label emr-5.26.0 \
--log-uri 's3n://aws-logs-251682129355-us-east-1/elasticmapreduce/' \
--instance-groups '[{"InstanceCount":5,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"InstanceGroupType":"CORE","InstanceType":"m4.xlarge","Name":"Core - 2"},{"InstanceCount":1,"EbsConfiguration":{"EbsBlockDeviceConfigs":[{"VolumeSpecification":{"SizeInGB":32,"VolumeType":"gp2"},"VolumesPerInstance":2}]},"InstanceGroupType":"MASTER","InstanceType":"m4.xlarge","Name":"Master - 1"}]' \
--configurations '[{"Classification":"spark-env","Properties":{},"Configurations":[{"Classification":"export","Properties":{}}]},{"Classification":"spark-defaults","Properties":{}},{"Classification":"spark","Properties":{"maximizeResourceAllocation":"true"}}]' \
--auto-scaling-role EMR_AutoScaling_DefaultRole \
--bootstrap-actions '[{"Path":"s3://insightde/emr/bootstraps/distroduce.sh","Name":"bootstrap"}]' \
--ebs-root-volume-size 10 \
--service-role EMR_DefaultRole \
--enable-debugging \
--name 'distibuted_produce' \
--scale-down-behavior TERMINATE_AT_TASK_COMPLETION \
--region us-east-1