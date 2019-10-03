from distroduce.emr import launch_cluster
from distroduce.configuration.cluster import ec2_attributes, bootstrap_actions, instance_groups, configurations
region = 'us-east-1'
cluster_name = 'distibuted_produce'
launch_cluster(cluster_name, region, ec2_attributes, bootstrap_actions, instance_groups, configurations)