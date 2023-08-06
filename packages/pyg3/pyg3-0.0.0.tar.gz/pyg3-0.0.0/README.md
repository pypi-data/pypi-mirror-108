


```python
In [1]: import pyg3

In [2]: d = pyg3.Domain()

In [3]: d
Out[3]: <pyg3.Domain at 0x7f0ebe6ec1f0>
```

Meaningful errors:

```python
In [4]: n = pyg3.Node()
-------------------------------------------------------------------------
TypeError                               Traceback (most recent call last)
<ipython-input-4-3e097288ae09> in <module>
----> 1 n = pyg3.Node()

TypeError: __init__(): incompatible constructor arguments. The following argument types are supported:
    1. pyg3.Node(arg0: int, arg1: int, arg2: float, arg3: float)

Invoked with:

In [5]: n = pyg3.Node(0, 0, 1.0, 10.0)

In [6]: d.addNode(n)
Out[6]: True

In [7]: d.getNode(0)
Out[7]: <pyg3.Node at 0x7f0ebc6fca70>
```


Thread safe:

```python
In [8]: d2 = pyg3.Domain()

In [9]: d2.getNode(0)
In [10]: n2 = pyg3.Node(0,0,0.0,0.0)

In [11]: d2.addNode(n2)
Out[11]: True

In [12]: d2.getNode(0)
Out[12]: <pyg3.Node at 0x7f0ebe714e70>
```

```python
In [13]: d.getNode(0)
Out[13]: <pyg3.Node at 0x7f0ebc6fca70>
```

```python
In [14]: d.getNode(0) == n
Out[14]: True

In [15]: d2.getNode(0) == n2
Out[15]: True
```



