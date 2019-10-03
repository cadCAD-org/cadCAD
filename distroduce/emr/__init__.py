import os, json, boto3
from typing import List


def launch_cluster(name, region, ec2_attributes, bootstrap_actions, instance_groups, configurations):
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


# def benchmark(names: List[str], region, ec2_attributes, bootstrap_actions, instance_groups, configurations):
#     current_dir = os.path.dirname(__file__)
#     s3 = boto3.client('s3')
#     bucket = 'insightde'
#
#     file = 'distroduce.sh'
#     abs_path = os.path.join(current_dir, file)
#     key = f'emr/bootstraps/{file}'
#
#     s3.upload_file(abs_path, bucket, key)
#     for name in names:
#         launch_cluster(name, region, ec2_attributes, bootstrap_actions, instance_groups, configurations)