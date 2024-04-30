# Nyu-tv Cloud Project

**"Nyu-tv"** is a cloud-based project designed for individuals within Nyu to facilitate stream access requests, scheduling, and live streaming. Users can request stream access for their channels, allowing others from Nyu to subscribe and view streams with minimal latency. Leveraging AWS resources, the backend of this project is hosted serverlessly for efficient scalability and maintenance.

## Key Features:

- Stream access request system for Nyu individuals.
- Channel scheduling and live streaming capabilities.
- Low-latency viewing experience for Nyu subscribers.
- Utilizes AWS services for reliable and scalable backend infrastructure.
- Serverless architecture for efficient resource management and maintenance.

## Admin frontend

- Allows the admin to view all the requests from users to create a channel
- Allows the admin to approve/deny an individual from creating a channel
    - Calls AWS lambdas to fetch and update channel creation requests