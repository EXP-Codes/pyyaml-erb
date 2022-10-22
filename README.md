# pyyaml-erb

> 解析 yaml 配置文件中的的环境变量

------

## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)


## 介绍

模仿 Ruby 的 [ERB](https://docs.ruby-lang.org/en/2.3.0/ERB.html) 能力，把 yaml 配置文件中的环境变量做简单解析。


## 安装说明

执行脚本： 

```
python -m pip install --upgrade pip
python -m pip install pyyaml-erb
```


## 使用说明

在代码中引入 pyyaml-erb 包，读取配置 yml 配置文件即可：

```python
import erb.yml as yaml
with open(SETTING_PATH, 'r', encoding='utf-8') as file :
    settings = yaml.load(file.read())
```

配置示例可参考 [settings.yml](./tests/config/settings.yml)，使用教程可参考单元测试 [test_yaml_erb.py](./tests/test_yaml_erb.py)。

例如环境变量为 `JAVA_HOME`，只需要在 yaml 配置为 `<%= ENV["KEY"] %>` 或 `<%= ${KEY} %>` 的值表达式即可识别并解析。

一般而言，值表达式有以下几种配置模式：

- `key_1: <%= ENV["VAR_1"] %>`： 默认的使用方式
- `key_2: <%= ENV["VAR_2"] or None %>`： 跟默认方式一样，多了默认值为 None，没意义
- `key_3: <%= ENV["VAR_3"] || null %>`： 跟默认方式一样，多了默认值为 None，没意义
- `key_4: <%= ENV["VAR_4"] || "nil" %>`： 跟默认方式一样，多了默认值为 None，没意义
- `key_5: <%= ENV["VAR_5"] || default %>`： 若环境变量不存在，会设置为默认值
- `key_6: "<%= ENV['VAR_6'] or 'default' %>"`： 若环境变量不存在，会设置为默认值
- `key_7: <%= ENV["VAR_7"] || 7 %>`： 若环境变量不存在，会设置为默认值，且默认值会解析为整型
- `key_8: <%= ENV["VAR_8"] || 1.23 %>`： 若环境变量不存在，会设置为默认值，且默认值会解析为浮点型
- `key_9: <%= ENV["VAR_9"] || true %>`： 若环境变量不存在，会设置为默认值，且默认值会解析为布尔型
- `key_10: <%= ENV["VAR_10"] || 'False' %>`： 若环境变量不存在，会设置为默认值，且默认值会解析为布尔型
- `key_0: '<%= ENV["VAR_0"] || ${VAR_11} or default %>'`： 混合模式

> 引号用双引号或单引号都可以，值表达式外围用不用引号包围都可以，表达式之间用 `||` 或 `or` 都可以

