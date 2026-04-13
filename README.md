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
