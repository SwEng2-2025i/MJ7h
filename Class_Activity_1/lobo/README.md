# Task Manager – Hexagonal Architecture

This service allows you to create and list tasks using a hexagonal architecture (ports and adapters). Business logic is decoupled from infrastructure details, such as the web framework or storage.

## 📋 Endpoints disponibles

### ➕ Create a task

Create a new task with a title.

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender arquitectura hexagonal"}'
```

### 📄 List all tasks

Returns a list of all created tasks.

```bash
curl http://localhost:5000/tasks
```

Change the attribute done of one task passing by the id of the task 

```bash
curl -X PUT http://localhost:5000/tasks/<id>/done \
 -H "Content-Type: application/json"  \
 -d " \{\"title\": \"Aprender arquitectura hexagonal\"}"
```

Flow Diagram of the last Enpoint using a Hexagonal representation in Draw.io
![Draw.IO Hexagonal Diagram](ClassActivity1-lobo.drawio.svg)