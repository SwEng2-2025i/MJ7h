This challenge extends the current hexagonal architecture project in Python.

---

## 🎯 Objective

Extend the current system to allow a task to be marked as complete (done = True) using a new HTTP endpoint.

Based on: The hexagonal task system (ports & adapters) in Python [link](https://github.com/SwEng2-2025i/SwEng2_2025i_Examples/tree/main/Example%204%20-%20Hexagonal%20Architecture)

---

## ✅ Requirements

1. **Modify the Domain**

2. **Extend the Input Port**

3. **Update the Use Case**

4. **Enhance the Repository**

5. **Add a New HTTP Endpoint**
   - Create an endpoint:
     ```
     PUT /tasks/<id>/done
     ```
     It should mark the task as completed.

6. **Test with `curl`**
   ```bash
   # Create a task
   curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"title": "Finish challenge"}'

   # Mark as done (replace <id> with the actual task ID)
   curl -X PUT http://localhost:5000/tasks/<id>/done

7. It should be **well documented**, complete the README with flowcharts presenting the new functionality


## 🏁 Success criteria

- The new endpoint must work.

- Tasks must correctly reflect the done = true field when listed.

- The architecture must remain hexagonal (no business logic in adapters).


## Submission Format
It must be delivered **via a pull request to the main branch of the repository**, which must be merged before the delivery date. In the folder Class_Activity_1, create an X folder (where X = your team animal), which must include the deliverable.
