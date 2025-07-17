---
file_format: mystnb
kernelspec:
  name: python3
mystnb:
  execution_timeout: 30
  merge_streams: True
---

(test_myst_nb)=

# Test Myst-NB cells

Below is an example of a simple myst-nb cell:

```{code-cell}
def print_message():
    message = "Hello, this is a simple print statement!"
    print(message)

print_message()
```

```{code-cell}
def print_message_and_math():
    message = "Hello, this is a simple print statement!"
    math_result = 5 + 3  # Example math operation
    print(message)
    print(f"The result of 5 + 3 is: {math_result}")

print_message_and_math()
```
