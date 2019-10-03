import os, json, boto3
from typing import List

ec2_attributes = {
    "KeyName":"joshua-IAM-keypair",
    "InstanceProfile":"EMR_EC2_DefaultRole",
    "SubnetId":"subnet-0034e615b047fd112",
    "EmrManagedSlaveSecurityGroup":"sg-08e546ae27d86d6a3",
    "EmrManagedMasterSecurityGroup":"sg-08e546ae27d86d6a3"
}

bootstrap_actions = [
    {
        "Path":"s3://insightde/emr/bootstraps/distroduce.sh",
        "Name":"bootstrap"
    }
]

instance_groups = [
    {
        "InstanceCount":5,
        "EbsConfiguration":
            {"EbsBlockDeviceConfigs":
                [
                    {
                            "VolumeSpecification":
                                {"SizeInGB":32,"VolumeType":"gp2"},
                            "VolumesPerInstance":2
                    }
                ]
            },
        "InstanceGroupType":"CORE",
        "InstanceType":"m4.xlarge",
        "Name":"Core - 2"
    },
    {
        "InstanceCount":1,
        "EbsConfiguration":
            {
                "EbsBlockDeviceConfigs":
                    [
                        {
                            "VolumeSpecification":
                                {"SizeInGB":32,"VolumeType":"gp2"},
                            "VolumesPerInstance":2
                        }
                    ]
            },
        "InstanceGroupType":"MASTER",
        "InstanceType":"m4.xlarge",
        "Name":"Master - 1"
    }
]

configurations = [
    {
        "Classification":"spark-env",
        "Properties":{},
        "Configurations":
            [
                {
                    "Classification":"export",
                    "Properties":{
                        "PYSPARK_PYTHON": "/usr/bin/python3",
                        "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
                    }
                }
            ]
    },
    {
        "Classification":"spark-defaults",
        "Properties":{
            "spark.sql.execution.arrow.enabled": "true"
        }
    },
    {
        "Classification":"spark",
        "Properties":{
            "maximizeResourceAllocation":"true"
        }
    }
]



def create_distroduce_cluster(name, region, ec2_attributes, bootstrap_actions, instance_groups, configurations):
    def log_uri(name, region):
        return f's3n://{name}-{region}/elasticmapreduce/'

    os.system(f"""
        aws emr create-cluster \
        --applications Name=Hadoop Name=Hive Name=Spark \
        --ec2-attributes '{json.dumps(ec2_attributes)}' \
        --release-label emr-5.26.0 \
        --log-uri '{str(log_uri(name, region))}' \
        --instance-groups '{json.dumps(instance_groups)}' \
        --configurations '{json.dumps(configurations)}' \
        --auto-scaling-role EMR_AutoScaling_DefaultRole \
        --bootstrap-actions '{json.dumps(bootstrap_actions)}' \
        --ebs-root-volume-size 10 \
        --service-role EMR_DefaultRole \
        --enable-debugging \
        --name '{name}' \
        --scale-down-behavior TERMINATE_AT_TASK_COMPLETION \
        --region {region}
    """)


def benchmark(names: List[str], region, ec2_attributes, bootstrap_actions, instance_groups, configurations):
    current_dir = os.path.dirname(__file__)
    s3 = boto3.client('s3')
    bucket = 'insightde'

    file = 'distroduce.sh'
    abs_path = os.path.join(current_dir, file)
    key = f'emr/bootstraps/{file}'

    s3.upload_file(abs_path, bucket, key)
    for name in names:
        create_distroduce_cluster(name, region, ec2_attributes, bootstrap_actions, instance_groups, configurations)


name = 'distibuted_produce'
region = 'us-east-1'
benchmark([name], region, ec2_attributes, bootstrap_actions, instance_groups, configurations)