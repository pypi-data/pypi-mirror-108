import gcsfs
import pickle
import os
from loguru import logger
import upswingutil as ul


def get_model_from_cloud_storage(file_path, file_name, token=None):
    __G_CLOUD_PROJECT__ = os.getenv('G_CLOUD_PROJECT', ul.G_CLOUD_PROJECT)
    __secret__ = os.getenv('FIREBASE', ul.FIREBASE)
    filepath = f'{__G_CLOUD_PROJECT__}.appspot.com/{file_path}/{file_name}'
    try:
        if token:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=token)
        else:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=f"{__secret__}")

        with fs.open(filepath, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logger.error(f'Unable to get model : {filepath}')
        logger.error(e)
        return None


if __name__ == '__main__':
    model = get_model_from_cloud_storage('revenue_forecast', 'revenue_forecast_11264.pkl')
    result = model.forecast(10) if model else []
    print(result)
