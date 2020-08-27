# Nvidia GPU Exporter for Prometheus

## For Linux

Here exists an image for Nvidia GPU Exporter ([link](https://hub.docker.com/r/mindprince/nvidia_gpu_prometheus_exporter/)) but manifest is broken.

First, build a Docker image - [link](https://github.com/mindprince/nvidia_gpu_prometheus_exporter):

```bash
docker build -t nvidia_gpu_prometheus_exporter .
```

Then either run with docker directly:

```bash
docker run --privileged -p 9401:9401 -e LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu --volume /usr/lib/x86_64-linux-gnu/:/usr/lib/x86_64-linux-gnu/ bugroger/nvidia-exporter:latest
```

Or use Docker-compose:

```bash
docker-compose up -d
```

## For Windows

//todo
