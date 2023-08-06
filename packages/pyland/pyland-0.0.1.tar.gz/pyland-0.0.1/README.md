# dl_cms

**test framework powered by pytest**  

- `common`文件夹，可放置跨项目的通用型脚本，作为共享目的
- `test`文件夹，每个项目独立一份子文件夹（可嵌套多层），DEMO项目子文件夹的内部结构如下

# basic struct  

- config   
> 全局配置 host 、db、log   

- data   
> 用例数据，如输入参数、参数模板（针对复杂参数使用）、其他数据（image、export、cookies）  
> 每个参数的有效用例和无效用例可分开编写，会按照一定方式组合为param_list  

- test_suits
> 用例编写（1、读取参数列表 2、调用interface对象 3、结果处理 4、断言  ） 
 
- demo.py
> 化所有待测接口为对象  （名称为自己的项目名称）

- run.py
> 按需执行用例计划，生成报告

# write testcase step  

**前提条件**  

- 测试用例（单个接口的详细的入参和出参设计，多个接口的调用依赖流程） 

- data，准备每个接口的测试数据（eg. cookies、input_loads)

![steps](doc/simple_architecture_1.0.jpg)

**步骤**

- config，修改host、db

- demo.py， 修改文件名，封装待测接口

- test_suits/conftest.py （可选）
> 通常，需准备测试环境的脚本（setup、teardown）   
> 特殊地，需二次格式化参数，二次格式化输出，以及复杂断言的脚本  

- test_suits/test_xx.py  
> 调用接口和conftest.py， 编写用例

- suit/run.py （可选） 
> 定义要执行的接口测试，运行即自动产生测试报告  

![allure-report example](http://f.shopee.co.id/file/57650ddf4085344c59d1d77fb0fabb78)

# 对接自动化测试平台

- 在平台上新建项目，输入git地址、项目路径（以tests目录为基准的相对路径， 如DEMO就是demo项目的路径）

- 在平台上导入用例，选择用例执行即可