# Marked Requests (and Sessions)

## Introduction

The **Marked Requests** library is a Python wrapper around the popular [`requests`](https://requests.readthedocs.io/en/latest/)  library. 

It allows you to send a unique, predefined header to your **vulnbox**. 

This feature helps in distinguishing your requests from others, making it easier to track and analyze your traffic.

### Why Use Marked Requests?

1. **Easy Traffic Identification**: When working with a shared server environment, such as during a Capture the Flag (CTF) event or penetration testing exercise, it can be challenging to identify which requests are yours. The special header lets you mark your traffic, making it straightforward to trace your activities.

2. **Clear Team Boundaries**: In scenarios where multiple teams or individuals are interacting with the same server, it's crucial to avoid confusion. The predefined header clearly identifies your requests, ensuring there's no ambiguity about which team is testing what.

## How It Works

- **Session Persistence**: By extending the `requests.Session` class, the *ADsession* retains session properties, such as cookies, across multiple requests. This ensures that once you log in or establish a session, subsequent requests can leverage this context.

- **Custom Headers for Specific Targets**: You can specify a target server (the vulnbox) that requires special headers. These headers are automatically added to your requests to this server, while requests to other servers remain unaffected.

- **Seamless Integration**: The library is designed to be a drop-in replacement for standard `requests` sessions. You can continue using the familiar `requests.get` and `requests.post` methods with added benefits.

### Benefits

- **Simplicity**: Easy to implement and use, with minimal changes to your existing code.
- **Clarity**: Clear differentiation of your traffic from others, reducing misunderstandings.
- **Efficiency**: Maintains session state and handles cookies automatically, just like the standard `requests` library.

## Getting Started

Here's a quick example to get you started using the *ADsession*:

```python
from MarkedRequests.MarkedRequests import ADsession

# Initialize your session
session = ADsession(vulnbox_ip='192.168.0.1')  # Replace with your vulnbox IP

# Leave empty if vulnbox_ip is an ENVIRONMENT VARIABLE CALLED **VM_IP**
# ex: session = ADsession()

# Make a request
response = session.get('http://192.168.0.1/api/data', headers={"name":"value"}, json={"key":"value"})
print(response.text)
```

This setup ensures that all requests to `http://192.168.0.1` include the special header, making your traffic easily identifiable.
