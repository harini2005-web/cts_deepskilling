Microservice Decomposition

Course Service
- Owns course data
- Owns course endpoints
- Owns courses.db

Student Service
- Owns enrollment logic
- Owns students.db

Inter-service Communication

Student Service calls Course Service
using synchronous HTTP requests.

If Course Service is unavailable,
Student Service returns 503.

API Gateway

Routes:

/api/courses/* -> Course Service

/api/students/* -> Student Service

Trade-offs

Synchronous HTTP:
- Simple
- Immediate response
- Tight coupling

Message Queue:
- Looser coupling
- Better scalability
- Eventual consistency

RabbitMQ and Kafka are examples.