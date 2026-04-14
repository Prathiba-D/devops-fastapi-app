<h3>Automated CI/CD pipeline to build, scan, and deploy a containerized FastAPI application on Kubernetes with full observability.</h3>

<h4>📌 Project Overview</h4>
This project demonstrates a real-world DevOps workflow, implementing a fully automated pipeline from code commit to deployment and monitoring.
It integrates CI/CD automation, containerization, Kubernetes orchestration, security scanning, and observability, closely resembling a production environment setup.

<h4>📸 Demo</h4>
<p align="center">
  <img src="images/app-deployed-userform.PNG" width="700"/><br>
  FastAPI application successfully deployed and accessible via Kubernetes service
  <br><br>
</p>
<p align="center">
  <img src="images/jenkins-pipeline-stages.PNG" width="700"/><br>
  CI/CD pipeline showcasing build, security scan, and Kubernetes deployment stages
  <br><br>
</p>
<p align="center">
  <img src="images/grafana-dashboard.PNG" width="700"/><br>
  Grafana dashboard visualizing real-time system and application metrics
  <br><br>
</p>

<h4>🏗️ Architecture</h4>
<h4>⚙️ Tech Stack</h4>
<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Tools Used</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>CI/CD</td>
      <td>Jenkins</td>
    </tr>
    <tr>
      <td>Containerization</td>
      <td>Docker</td>
    </tr>
    <tr>
      <td>Orchestration</td>
      <td>Kubernetes (kOps on AWS)</td>
    </tr>
    <tr>
      <td>Image Registry</td>
      <td>AWS ECR</td>
    </tr>
    <tr>
      <td>Monitoring</td>
      <td>Prometheus, Grafana</td>
    </tr>
    <tr>
      <td>Security</td>
      <td>Trivy</td>
    </tr>
    <tr>
      <td>Code Quality</td>
      <td>SonarQube</td>
    </tr>
    <tr>
      <td>Backend</td>
      <td>FastAPI</td>
    </tr>
  </tbody>
</table>

<h4>⚙️ CI Server Setup (Jenkins)</h4>
<p>Configured a dedicated CI server with required tools and permissions </p>
<p align="center">
  <img src="images/ci-tools-installed.PNG" width="700"/><br>
  Installed tools
  <br><br>
</p>
<p align="center">
  <img src="images/jenkins-plugins.PNG" width="700"/><br>
  Jenkins Plugins
  <br><br>
</p>
<p align="center">
  <img src="images/iam-role-policies.PNG" width="700"/><br>
  Custom IAM Role attached to CI Server
  <br><br>
</p>
<p align="center">
  <img src="images/jenkins-webhook-config.PNG" width="700"/><br>
  GitHub Webhook Integration
  <br><br>
</p>

<h4>🏗️ Infrastructure Setup (AWS + kOps)</h4>
Provisioned a Kubernetes cluster using kOps with AWS as the cloud provider<br>
<p align="center">
  <img src="images/ec2-instances.PNG" width="700"/><br>
  EC2 Instances
  <br><br>
</p>
<p align="center">
  <img src="images/kops-cluster-creation.PNG" width="700"/><br>
  KOPS Cluster
  <br><br>
</p>

<h4>🔄 CI/CD Pipeline</h4>
<p>Fully automated pipeline triggered on code changes</p><br>
<p align="center">
  <img src="images/jenkins-pipeline-stages.PNG" width="700"/><br>
  Pipeline Execution Flow
  <br><br>
</p>
<p align="center">
  <img src="images/aws-ecr-repository.PNG" width="700"/><br>
  AWS ECR Repository
  <br><br>
</p>

<h4>Pipeline Stages</h4>
<ol>
  <li>Code pushed to GitHub</li>
  <li>Jenkins pipeline triggered via webhook</li>
  <li>Code quality analysis (SonarQube)</li>
  <li>Docker image built</li>
  <li>Security scan (Trivy)</li>
  <li>Image pushed to AWS ECR</li>
  <li>Deployment to Kubernetes</li>
</ol>

<h4>🔐 Code Quality & Security</h4>
<p>Integrated quality checks and vulnerability scanning into CI pipeline</p><br>
<p align="center">
  <img src="images/sonarqube-dashboard.PNG" width="700"/><br>
  SonarQube Analysis
  <br><br>
</p>
<p align="center">
  <img src="images/sonarqube-quality-gate.PNG" width="700"/><br>
  Quality Gate Status
  <br><br>
</p>
<p align="center">
  <img src="images/trivy-scan-report.PNG" width="700"/><br>
  Trivy Vulnerability Scan
  Report is live <a href="https://prathiba-d.github.io/devops-fastapi-app/">here</a>
  <br><br>
</p>

<h4>☸️ Kubernetes Deployment</h4>
<p>Deployed application using Kubernetes with zero-downtime strategy</p><br>
<p align="center">
  <img src="images/k8s-nodes.PNG" width="700"/><br>
  Cluster Nodes Status
  <br><br>
</p>
<p align="center">
  <img src="images/k8s-rolling-update.PNG" width="700"/><br>
  Rolling Update Strategy
  <br><br>
</p>

<h4>📊 Monitoring & Observability</h4>
<p>Implemented full-stack observability using Prometheus, Alertmanager, and Grafana for metrics collection, alerting, and visualization</p>
<p align="center">
  <img src="images/prometheus-targets-up.PNG" width="700"/><br>
  Prometheus Targets Up (Healthy)
  <br><br>
</p>
<p align="center">
  <img src="images/prometheus-target-down.PNG" width="700"/><br>
  Prometheus Target Down (Failure Scenario)
  <br><br>
</p>
<p align="center">
  <img src="images/alertmanager-active-alerts.PNG" width="700"/><br>
  Active Alerts Dashboard - Alertmanager aggregating and displaying active alerts triggered by Prometheus rules
  <br><br>
</p>
<p align="center">
  <img src="images/alertmanager-email-notification.PNG" width="700"/><br>
  Automated email alerts sent based on configured alerting rules
  <br><br>
</p>
<p align="center">
  <img src="images/node-exporter-metrics.PNG" width="700"/><br>
  Node exporter - System-level metrics including CPU, memory, and resource utilization
  <br><br>
</p>
<p align="center">
  <img src="images/fastapi-metrics-endpoint.PNG" width="700"/><br>
  Application-level metrics exposed via FastAPI and scraped by Prometheus
  <br><br>
</p>
<h4>📂 Project Structure</h4>
<pre>
devops-fastapi-app/
│── main.py                  # FastAPI application source code
│── Dockerfile               # Container build definition
│── Jenkinsfile              # CI/CD pipeline configuration
│── k8s/                     # Kubernetes manifests (Deployment, Service)
│── monitoring/              # Prometheus & Alertmanager configs
│── images/                  # Screenshots used in README.md
│── README.md                # Project documentation
</pre>
<pre>
<h4>💡 Key Highlights</h4>
✅ Automated CI/CD pipeline from code commit to deployment using Jenkins  
✅ Deployed a production-like Kubernetes cluster using kOps on AWS  
✅ Implemented container security scanning using Trivy  
✅ Enforced code quality gates with SonarQube  
✅ Achieved zero-downtime deployments using Kubernetes rolling updates  
✅ Enabled full system observability with Prometheus & Grafana dashboards
</pre>

<h4>🎯 What This Project Demonstrates</h4>
<ul>
  <li>Strong understanding of DevOps principles and workflows</li>
  <li>Hands-on experience with CI/CD automation</li>
  <li>Hands-on experience with containerization & orchestration</li>
  <li>Hands-on experience with infrastructure provisioning</li>
  <li>Hands-on experience with monitoring & alerting systems</li>
  <li>Ability to build production-ready, scalable systems</li>
</ul>
