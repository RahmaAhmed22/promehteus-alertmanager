# Mini Observability & Monitoring System
A monitoring solution providing full-stack visibility across **Cloud Infrastructure (EC2)**, **Kubernetes Cluster**, and **Flask-Application HTTP Requests**.

## Project Overview
This project demonstrates a monitoring flow using **Prometheus**, **Grafana**, and **Alertmanager**. It features an automated alerting system that routes notifications via **Telegram** and **Gmail** based on the source of the event.
The monitoring stack is centralized in a Dockerized environment, scraping metrics from three distinct layers through specialized exporters and API proxies.

---
## Part 1: EC2 Infrastructure Monitoring
**Objective:** 
* Capture host-level metrics to ensure the health of the underlying virtual machines.
* Used Node Exporter to track CPU, Memory and Disk.
* Configured **Alertmanager** to route infrastructure alerts (e.g., High Disk Usage) to **Telegram**.

> **Test Case 1: Disk Stress Simulation**

I intentionally increase the disk usage by above 80% using `fallocate`

<img width="624" height="427" alt="image" src="https://github.com/user-attachments/assets/ae7a070c-268f-4fd5-a730-453a7a852849" />

 *Grafana Node Exporter Dashboard:*

<img width="624" height="364" alt="image" src="https://github.com/user-attachments/assets/8673fe8e-745a-486f-ae35-f660113dcee8" />

> **Test Case 2: Instance Shutdown**

*Grafana Node Exporter Dashboard:*

<img width="624" height="360" alt="image" src="https://github.com/user-attachments/assets/29c6f49c-cdf0-4749-82d0-c8668d1a7835" />

*Telegram Notification For 2 Test Cases:*

<img width="389" height="454" alt="image" src="https://github.com/user-attachments/assets/353118ba-28c8-4aff-9770-930967b7c0f2" />

---

## Part 2: Flask Application Observability

**Objective:**

* Instrumented a Flask app to expose custom endpoints using basic instrumention like `Counter`, `Gauge`, `Summary`, `Histogram`.
*  Created routing logic to send 5xx Error alerts to **Gmail**.

**Test Case: HTTP Server Failure**

Simulated Continuously sending 500 HTTP request using command:

`while true; do curl -s http://localhost:5000/fail-server > /dev/null; echo "Request sent..."; sleep 1; done`

*Prometheus Graph*

<img width="624" height="272" alt="image" src="https://github.com/user-attachments/assets/5f63b19d-0de1-4116-a223-d868befb62f8" />

*Gmail Notification:*

<img width="624" height="321" alt="image" src="https://github.com/user-attachments/assets/fc7e8b57-5722-4f5f-a604-93d6fd5c4670" />

---

## Part 3: Kubernetes Cluster Monitoring

**Objective:** 

* Gain visibility into the cluster nodes usage through `Node Exporter`, pods and deployments usage and health through `kube-state-metrics` & `cAdvisor`.
* Built alerts for high usage of nodes and pods or pods continuous termination `OOMKilled` and routed it via **Gmail**.

> **Test Case 1: High Node CPU Usage**

*Gmail Notification:*

<img width="624" height="386" alt="image" src="https://github.com/user-attachments/assets/f06693a9-6bf5-4267-b51a-5b09e88e9888" />

> **Test Case 2: High Pod CPU Usage**

Enforcing High CPU exceeds Nginx deploymet CPU limits:

`kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://nginx-deploy; done"`

*Grafana K8S Cluster Dashboard:*

<img width="624" height="229" alt="image" src="https://github.com/user-attachments/assets/6edec30e-8cfe-49f0-8895-a345cb4e20eb" />

*Gmail Notification:*

<img width="624" height="502" alt="image" src="https://github.com/user-attachments/assets/a89a1226-0e83-4961-ab74-3fe0b05ca1e1" />


> **Test Case 3: Pod Memory Stress**

Running Memory Stress Pod with limits 100 MB RAM, which Kuberenets continuously terminates and gets into `OOMKilled` status.

*Grafana K8S Cluster Dashboard:*

<img width="624" height="151" alt="image" src="https://github.com/user-attachments/assets/1818e6d4-9039-44f7-ba16-eb69268ed5b6" />

*Gmail Notification:*

<img width="600" height="355" alt="image" src="https://github.com/user-attachments/assets/819aa346-4548-4575-be40-dfc07eba75ad" />

---

## Refernces:

* <https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/>

* <https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/>

* <https://github.com/kubernetes/kube-state-metrics/blob/main/examples/standard/>

* <https://github.com/prometheus/prometheus/blob/release-3.9/documentation/examples/prometheus-kubernetes.yml>

* <https://prometheus.io/>
