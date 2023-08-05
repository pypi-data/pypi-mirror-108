# ToCM_reference_data
A python library to process reference data usefull for my projects.


## How to
This is a small code example of how this library works
```python
import tocm_reference_data as ref
import matplotlib.pyplot as plt

for line in ref.Hestand_2015.figure7.lines:
    plt.plot(line.x, line.y, label=line.label)

plt.legend()
plt.show()

print(ref.Hestand_2015.metadata)

```