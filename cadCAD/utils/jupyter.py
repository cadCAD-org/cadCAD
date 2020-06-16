def get_home_dir(user):
    return f"s3://jupyterbackups/jupyter/{user}/"

def set_write_path(_spark_context, user, datafolder_path):
    return get_home_dir(user) + datafolder_path +f'_{_spark_context.applicationId}'
