<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
</head>
<body>
  <h1>📸 Instagram Simulator</h1>
  <p>A simplified Instagram-like application built with Django, featuring custom authentication, social features, RESTful APIs, and complete containerization.</p>

  <h2>🔐 Authentication</h2>
  <ul>
    <li>Custom user model using <strong>email and password</strong></li>
    <li>Profile model connected via Django signals</li>
    <li><code>User</code> and <code>Profile</code> models have a one-to-one relationship</li>
    <li>Located in the <code>accounts</code> application</li>
  </ul>

  <h2>📝 Social Features & Models</h2>
  <ul>
    <li>Defined in the <code>posts</code> app</li>
    <li><strong>Post</strong>: shareable content</li>
    <li><strong>Follow</strong>: tracks relationships between users</li>
    <li><strong>Comment</strong>: allows user interaction</li>
    <li><strong>Notification</strong>: alerts for likes, comments, and follow requests</li>
  </ul>

  <h2>📁 Templates</h2>
  <ul>
    <li>Templates divided into 4 categories based on functionality and layout</li>
    <li>Designed for modular use and easy customization</li>
  </ul>

  <h2>⚙️ Views & APIs</h2>
  <ul>
    <li>Implemented using <strong>Class-Based Views (CBVs)</strong></li>
    <li>RESTful API features built with <strong>Generic API Views</strong> from Django REST Framework</li>
    <li>Only <strong>admin users</strong> have access to full CRUD operations through the API</li>
    <li>Secured with <strong>JWT Authentication</strong>, enabling future sync support for client-side user access</li>
  </ul>

  <h2>🐳 Docker Integration</h2>
  <ul>
    <li>The entire project is fully Dockerized</li>
    <li>Includes Dockerfiles for backend services and dependencies</li>
    <li>Easy setup using <code>docker-compose</code></li>
    <li>Suitable for local development and deployment environments</li>
  </ul>

  <h2>🚀 Setup Instructions</h2>
  <ol>
    <li>Clone repo: <code>git clone [your-repo-link]</code></li>
    <li>Install packages: <code>pip install -r requirements.txt</code></li>
    <li>Run migrations: <code>python manage.py migrate</code></li>
    <li>Start server: <code>python manage.py runserver</code></li>
    <h3>And for docker up</h3>
    <li>build docker: <code>docker-compose build</code></li>
    <li>run container: <code>docker-compose up -d</code></li>
    <li>migrate: <code>docker-compose exec backend python manage.py migrate</code></li>
  </ol>

  <h2>👨‍💻 Developer</h2>
  <p>Created by <strong>Mohamad Amin Bajelan</strong>. For collaboration or inquiries, feel free to reach out or visit the GitHub repository.</p>
</body>
</html>
