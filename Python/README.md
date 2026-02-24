

# 🐍 Python for DevOps – Strong Basics Notes

**Author: Mohammed Sohail**
**Goal:** Learn only what is required for DevOps automation (not full Python development)

---

# 📌 1. What is Python? (Simple Explanation)

Python is a simple programming language used to:

* Automate tasks
* Execute system commands
* Work with APIs
* Process logs
* Handle JSON/YAML data
* Build small CLI tools

In DevOps, Python is used as an **automation tool**, not for building big web apps.

---

# 📌 2. Why Python is Important for DevOps

As a DevOps Engineer, you use Python to:

* Run shell commands (kubectl, docker, aws)
* Automate repetitive tasks
* Parse logs
* Read configuration files
* Interact with AWS (boto3)
* Monitor systems
* Build small automation tools

You do NOT need:

* Django
* Flask
* Web development
* Advanced algorithms

---

# 📌 3. Python Basics (Must Know)

---

## 3.1 Variables

```python
a = 2
b = 3
c = a + b
print(c)
```

Explanation:

* `a` stores 2
* `b` stores 3
* `c` stores 5
* `print()` shows output in terminal

---

## 3.2 Data Types

### Integer

```python
x = 10
```

### Float

```python
y = 3.14
```

### String

```python
name = "sohail"
```

### Boolean

```python
is_running = True
```

---

# 📌 4. List (Very Important)

List stores multiple values.

```python
pods = ["pod1", "pod2", "pod3"]

print(pods)
print(pods[0])
```

Used in DevOps to:

* Store pod names
* Store server names
* Process command output line by line

---

# 📌 5. Dictionary (Very Important for DevOps)

Dictionary stores key-value pairs.

```python
pod = {
    "name": "chat-app",
    "status": "Running",
    "restarts": 0
}

print(pod["status"])
```

Why important?

AWS, Kubernetes, APIs return data in JSON format (dictionary).

---

# 📌 6. If Condition (Decision Making)

```python
status = "CrashLoopBackOff"

if status == "Running":
    print("Pod is healthy")
else:
    print("Pod is not healthy")
```

Used to:

* Check pod health
* Check disk usage
* Check CPU threshold

---

# 📌 7. For Loop (Automation Core)

Loop helps repeat actions.

```python
pods = ["Running", "Pending", "CrashLoopBackOff"]

for status in pods:
    print(status)
```

With condition:

```python
for status in pods:
    if status == "Running":
        print("Healthy")
    else:
        print("Not Healthy")
```

DevOps = Loop + Condition + Command

---

# 📌 8. Function (Reusable Logic)

```python
def check_status(status):
    if status == "Running":
        return "Healthy"
    else:
        return "Not Healthy"

result = check_status("Running")
print(result)
```

Why important?

You don’t repeat code.
You reuse logic.

---

# 📌 9. Combining Loop + Dictionary

```python
pods = [
    {"name": "app1", "status": "Running"},
    {"name": "app2", "status": "CrashLoopBackOff"},
    {"name": "app3", "status": "Running"}
]

def check_pods(pod_list):
    for pod in pod_list:
        if pod["status"] == "Running":
            print(pod["name"], "is Healthy")
        else:
            print(pod["name"], "is Not Healthy")

check_pods(pods)
```

This is real DevOps style thinking.

---

# 📌 10. Running System Commands (Very Important)

Avoid using:

```python
import os
os.system("kubectl get pods")
```

Better method:

```python
import subprocess

result = subprocess.run(
    ["kubectl", "get", "pods"],
    capture_output=True,
    text=True
)

print(result.stdout)
```

Why better?

* More control
* Capture output
* Check errors
* Production safe

---

# 📌 11. Check Command Success

```python
import subprocess

result = subprocess.run(
    ["kubectl", "get", "pods"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("Success")
else:
    print("Error:", result.stderr)
```

---

# 📌 12. Virtual Environment (Good Practice)

Create virtual environment:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

Deactivate:

```bash
deactivate
```

Install packages:

```bash
pip install boto3 pyyaml
```

---

# 📌 13. JSON Handling (Important for AWS/K8s)

```python
import json

data = '{"name": "app1", "status": "Running"}'
parsed = json.loads(data)

print(parsed["status"])
```

---

# 📌 14. File Reading (Log Processing)

```python
with open("log.txt", "r") as file:
    for line in file:
        print(line.strip())
```

Used to:

* Analyze logs
* Check errors
* Monitor events

---

# 📌 15. What is Enough Python for DevOps?

You must know:

* Variables
* Data types
* List
* Dictionary
* Loop
* If condition
* Function
* subprocess
* Basic file handling
* Basic JSON

You do NOT need:

* Advanced OOP
* Web frameworks
* Complex data structures
* GUI apps
* Deep algorithm knowledge

---

# 📌 16. Real DevOps Automation Example

Count running pods:

```python
def count_running(status_list):
    count = 0
    for status in status_list:
        if status == "Running":
            count = count + 1
    return count

pods = ["Running", "Pending", "Running", "CrashLoopBackOff"]
print("Total Running:", count_running(pods))
```

---

# 📌 17. DevOps Mindset with Python

DevOps Script Pattern:

1. Run command
2. Capture output
3. Process data
4. Make decision
5. Take action

Example:

```python
import subprocess

result = subprocess.run(
    ["kubectl", "get", "pods", "--no-headers"],
    capture_output=True,
    text=True
)

for line in result.stdout.splitlines():
    print(line)
```

---

# 📌 Final Conclusion

As a DevOps Engineer:

Python is a tool for automation.
Not for building big applications.

You only need:

* Strong basics
* Clean logic
* Ability to read & modify scripts
* Confidence to debug errors

That is enough.

---

# 🚀 Next Step

After mastering this level:

Move to:

* Linux Deep Dive
* Networking
* Docker internals
* Kubernetes debugging

Python is now your helper tool.

---

END OF NOTES ✅
