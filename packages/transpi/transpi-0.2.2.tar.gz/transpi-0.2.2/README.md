# transpi

transpi is a translation tool.

### quick use

first `pip install transpi`, then:

```python
import transpi
result = transpi.trans("human")
print(result)

# or use different engine
result2 = transpi.trans("human", engine="bing")
print(result2)
```

### versions
- v0.2.0
  
  support bing trans
  
- v0.1.0
  
  support youdao trans