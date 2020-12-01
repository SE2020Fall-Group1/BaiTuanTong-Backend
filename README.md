# BaiTuanTong-Backend
2020Fall 软件工程第一组项目——百团通（暂定）后端仓库。

### 启动后端
```bash
python manage.py
```

### 测试
```bash
运行全部测试：
pytest

运行单个测试文件（以test_RegisterAndLogin.py为例）：
pytest test_RegisterAndLogin.py

运行单个用例（或一个类中所有用例）（以test_RegisterAndLogin.py文件中的test_register1函数为例）：
pytest test_RegisterAndLogin.py::test_register1

选项：
-s：输出调试信息，如在用例中print的内容
-v：输出用例更加详细的执行信息，比如运行环境、用例所在的文件及用例名称、每个用例的pass or fail等
--collect-only：展示当前目录下的全部测试用例
```