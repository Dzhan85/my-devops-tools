# Main Robolab Monitoring Systems

- [List of Prometheus Exporters](https://github.com/prometheus/prometheus/wiki/Default-port-allocations)

## Sections

- [Installation](docs/Installation.md)
- [Autonomous Car Central Management Panel](docs/AutonomousCar-CentralMgmt-Panel.md)

## Usage

Currently, the main monitoring system is availabile at `https://monitoring.robolab.innopolis.university/`.

> Actual address after RAID failure restored is `https://10.90.105.121:3000`

This is in beta-version, the default password is: `admin:admin`.

## Components

We use stack Prometheus+Grafana in the Docker environment. There is a good [project](https://github.com/stefanprodan/dockprom), we copied source files to alter the configuration. Those components includes:

- Prometheus: v2.18.1
- Alertmanager: v0.20.0
- Grafana: v7.0.0
- Grafana Remote Render Engine: latest
- Caddy V1: latest
- Pushgateway: v1.2.0
- cAdvisor: v0.36.0
- Node Exporter: v0.18.1
- Blackbox Exporter: 0.16.0
- SNMP Exporter: 0.18.0
- Customized Script Exporter

Monitoring system runs on a dedicated [VM](../Infrastructure/Hardware/grafana_prometheus_monitoring.md).

## Dashboards

Autonomous Car:

- [Autonomous Car Central Management Panel](docs/AutonomousCar-CentralMgmt-Panel.md) - the panel with brief status information per autonomous car

General:

- Monitoring Services Stack Dashboard (provisioned) - The Monitor Services Dashboard shows key metrics for monitoring the containers that make up the monitoring stack.
- [Node Exporter Full monitoring](https://grafana.com/grafana/dashboards/1860) (provisioned) - all default values exported by Prometheus node exporter graphed.
- Modified [Alerts - Linux Nodes](https://grafana.com/grafana/dashboards/5984) (provisioned) - Alerts for Linux Nodes using prometheus and node_exporter.
- [Alerts - Windows Nodes](https://grafana.com/grafana/dashboards/5993) (provisioned) - Alerts for Windows Nodes using Prometheus and wmi_exporter.
- [Windows Server](https://grafana.com/grafana/dashboards/11515) (provisioned) - Dashboard for Windows Servers
- Modified [GPU Monitoring](https://grafana.com/grafana/dashboards/10703) (provisioned) - Modified Dashboard Nvidia GPU Exporter for Prometheus
- [Node Metrics comparison](https://grafana.com/grafana/dashboards/11756) - A simplified version of [dashboard](https://grafana.com/grafana/dashboards/405) configured to be able to view multiple servers side by side.
- Modified [Storage I/O](https://grafana.com/grafana/dashboards/11801) - Storage performance is all about both IOPS and Latency.
- Uptime status - node scrappes availaiblity status
