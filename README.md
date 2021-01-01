# BaiTuanTong-Backend
2020Fall 软件工程第一组项目——百团通（暂定）后端仓库。

### 配置环境
```bash
pip install -r requirements.txt
bash make_dir.sh
```

### 启动后端
```bash
python manage.py
```

### 测试
```bash
运行全部测试：
pytest

运行单个测试文件：
pytest 文件名.py

运行一组用例（一个测试类）：
pytest 文件名.py::类名

运行单个用例：
pytest 文件名.py::类名::方法名

选项：
-s：输出调试信息，如在用例中print的内容
-v：输出用例更加详细的执行信息，比如运行环境、用例所在的文件及用例名称、每个用例的pass or fail等
-x：遇到用例执行失败或断言失败，立即停止运行，不执行后面的用例
--collect-only：展示当前目录下的全部测试用例
-k：使用该参数可以指定运行满足要求的用例。用法如下：
pytest -k "类名"
pytest -k "方法名"
pytest -k "类名 and not 方法名"
注意: -k参数后面跟的引号只能用双引号""，不能用单引号''，否则不会识别到用例，运行会报错
```