def get_home_dir(user):
    return f"s3://jupyterbackups/jupyter/{user}/"

def set_write_path(sc, user, datafolder_path):
    return get_home_dir(user) + datafolder_path +f'_{sc.applicationId}'
