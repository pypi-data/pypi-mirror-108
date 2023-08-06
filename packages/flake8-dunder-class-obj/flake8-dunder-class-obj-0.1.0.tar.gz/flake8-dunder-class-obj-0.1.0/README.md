# flake8-dunder-class-obj

A flake8 plugin which marks classes with leading double-underscored (dunder) class
objects. A double underscored class object is subject to "Name Mangling", which can be a
surprising behavior.

```python
class Test:
    __my_var = 1
```

This is an example of a variable with a double underscore. It will be flagged with a
message:
`DCO100: class objects should not begin with __ unless name mangling is desired`

See:
[Python private variables](https://docs.python.org/3/tutorial/classes.html#private-variables)
for more information about name mangling.
