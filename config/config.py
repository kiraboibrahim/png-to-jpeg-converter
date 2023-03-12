from environs import Env

env = Env()
env.read_env(recurse=False)


class Config(object):
    SECRET_KEY = env("SECRET_KEY")
    MAX_FILE_UPLOAD_SIZE = 5242880 # 5MB