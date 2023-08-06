# tfmcutil

#### 介绍
文本文件合并、分割模块：练习用的小模块。

#### 模块结构
tfmcutil 模块包含一个 TextFiles 类，文件的分割、合并通过该类实例的 sizedfiles、onefile 方法完成。


#### 安装教程

`python3 -m pip install tfmcutil`

#### 使用说明

```python
# 假设以下文件都存在且路径正确
from tfmcutil import TextFiles

f1 = TextFiles(("test.txt", "utf-8"))
f2 = TextFiles("test1.txt", ("test2.txt", "ascii"))
f3 = f1 + f2

print(len(f3)) # 实例中包含的文件数

print(f3.items()) # 实例中所有的 (文件路径, 编码) 元组

f3.onefile("result.txt") # 合并成一个文件

f3.sizedfiles(1000, "sized.txt") # 按字符数分割成多个文件， sized_1.txt、sized_2.txt ...

f4 = TextFiles.fromstring("测试内容\n第二行测试内容", "new.txt") # 将字符串写入 "new.txt" 并保存，返回 TextFiles 实例

f5 = f4 + f1

print(f5.totalsize()) # 返回实例中所有文件大小总和，单位字节

# 更多请查看源代码或 help(TextFiles)
```

#### 参与贡献

1.  Fork 本仓库
2.  新建 feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
