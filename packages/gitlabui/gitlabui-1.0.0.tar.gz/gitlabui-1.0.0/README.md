# gitlabui

[![Docker Pulls](https://img.shields.io/docker/pulls/batou9150/gitlabui.svg)](https://hub.docker.com/r/batou9150/gitlabui/)
[![Docker Stars](https://img.shields.io/docker/stars/batou9150/gitlabui.svg)](https://hub.docker.com/r/batou9150/gitlabui/) 

## Run the dev server
```shell
python3 setup.py install
python3 gitlabui-runner.py
```

## Run the production server with gunicorn

See [Gunicorn configuration](https://docs.gunicorn.org/en/stable/configure.html) for production configuration.

```bash
python3 setup.py install
gunicorn -b 0.0.0.0:5000 gitlabui:app
```

### Gunicorn configuration file example
```python
import multiprocessing

bind = "0.0.0.0:5000"
workers = multiprocessing.cpu_count() * 2 + 1
threads=2
```

Run with : `gunicorn -c conf.py gitlabui:app`

## Run with docker
```shell
docker run -d \
  -e GITLAB_URL=http://localhost/api/v4 \
  -e GITLAB_TOKEN=<YOUR_PRIVATE_TOKEN> \
  -p 5000:5000 batou9150/gitlabui gunicorn -b 0.0.0.0:5000 gitlabui:app
```
