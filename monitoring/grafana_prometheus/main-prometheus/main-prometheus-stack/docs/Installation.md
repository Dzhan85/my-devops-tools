# Autonomous Driving Lab Monitoring System Installation

Before starting, make sure you have the latest version of Autonomous Driving Lab DevOps repository.

```bash
git clone https://tfs.university.innopolis.ru/tfs/AutonomousTransportationSystemsLab/System%20Administration/_git/System%20Administration
```

The stack is placed inside the repository by the path `monitoring/prometheus/`.

Here you can find two main components:

- `exporters` - Prometheus-compatible exporters to use for endpoint hosts to expose metrics.
- `prometheus-stack` - Includes files to start up Prometheus+Grafana containers with provisioned configuration. You can alter default configuration there, for example, add new Grafana dashboards or alert rules.

## Installation with Ansible

There is a set of Ansible playbooks and roles helping to install and manage Prometheus+Grafana monitoring stack.

Ansible files are stored in the repository in the `ansible` folder. The next playbooks are useful:

- **deploy-repo.yml** - playbook to work with Git repositories (for example, to clone DevOps repository). Cloning via SSH to forward SSH keys (ForwardingAgent yes)
- **prometheus-agents.yml** - playbook to deploy and manage exporters on targets.
- **prometheus-server.yml** - playbook to deploy and manage.

These playbooks work with four group hosts. If you use a different inventory from a pre-defined set, make sure you set them.

- **prometheus-server** - a set of hosts where Prometheus+Grafana containers will be deployed.
- **prometheus-linux** - a set of Linux hosts, targets for Node Exporter.
- **prometheus-docker** - a set of Linux hosts with Docker runtime, targets for cAdvisor.
- **prometheus-nvidia-gpu** - a set of Linux hosts with Nvidia GPU graphics, targets for Nvidia GPU Exporter.

Below commands to test playbooks locally. Change inventory appropriately if you want to apply playbooks on real infrastructure.

Deploy exporters:

```bash
ansible-playbook -i inventory/local prometheus-agents.yml
```

Deploy Prometheus+Grafana with default parameters:

```bash
ansible-playbook -i inventory/local prometheus-server.yml
```

Alter default deployment: let containers locate on servers, but stopped:

```bash
ansible-playbook -i inventory/local prometheus-server.yml --ask-become-pass --extra-vars  "STATE=absent" --extra-vars "IS_RUNNING=true"
```

## Manual Installation

## Starting Prometheus+Grafana Server

```bash
cd monitoring/prometheus
docker-compose up -d
```
