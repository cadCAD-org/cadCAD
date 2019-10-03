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
