from transform.settings import cloud_config, sdx_app
from transform.views.main import transform

if __name__ == '__main__':
    cloud_config()
    sdx_app.add_post_endpoint(transform, rule="/transform")
    sdx_app.run(port=5000)
