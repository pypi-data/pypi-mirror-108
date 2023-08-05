# Python Config Registry Package

### 说明
这是一个 Python 配置快速注册调用模块，主要解决多维数组深层次配置调用问题。

### 链接
- [GitHub](https://github.com/ztj1993/py-config-registry)
- [PyPI](https://pypi.org/project/config-registry)

### 安装
```
pip install config-registry
```

### 设置获取数据
```
from ConfigRegistry import ConfigRegistry

setting = Registry()

setting.set('a', 'a')
setting.set('b', {'bb': 'bbb'})
setting.set('c.h', 'h')

print(setting.get())
print(setting.get('b.bb'))
```

### 加载字典
```
from ConfigRegistry import ConfigRegistry

setting = ConfigRegistry()

setting.load({'a': {'aa': 'aaa'}})
print(setting.get('a.aa'))
```

### 合并字典
```
from ConfigRegistry import ConfigRegistry

setting = ConfigRegistry()

setting.load({'a': {'a1': 'aaa1'}})
setting.merge('a', {'a2': 'aaa2' })
print(setting.get('a'))
```

### 设置默认值
```
from ConfigRegistry import ConfigRegistry

setting = ConfigRegistry()

setting.set('a', 'aaa')
setting.default('a', 'bbb')
setting.default('c', 'ccc')
print(setting.get('a'))
print(setting.get('c'))
```

### 钩子调用
```
import time
from ConfigRegistry import ConfigRegistry

setting = ConfigRegistry()

def callback():
    print('callback')

setting.set_hook('hook', 3, callback)
time.sleep(1)
setting.refresh_hook('hook')
time.sleep(3)
setting.refresh_hook('hook')
```

### 扁平化数据
```
from ConfigRegistry import ConfigRegistry

setting = ConfigRegistry({'a': {'aa': 'aaa'}, 'b': {'bb': 'bbb'}})
print(setting.flat())
```
