# coding: utf-8

import logging
import os
import shutil
import sys
from os.path import (
    abspath,
    basename,
    dirname,
    exists,
    getsize,
    isdir,
    isfile,
    join,
    normcase,
    normpath,
    splitext,
)
from typing import Callable

from chardet import UniversalDetector

_NONETYPE = type(None)
_CODING = sys.getdefaultencoding()
_CHUNKSIZE = 524288
_LOGGER = logging.getLogger(__name__)
LOGLEVEL = logging.CRITICAL
logging.basicConfig(
    level=LOGLEVEL, format="%(levelname)s - %(filename)s: %(message)s"
)


def fschunk(*items, size=_CHUNKSIZE):
    """以文本模式分块读取文件块并返回。"""
    fobjs = [open(fp, "rt", -1, ec) for fp, ec in items]
    index, lenfobjs = 0, len(fobjs)
    while index < lenfobjs:
        fobj = fobjs[index]
        while True:
            chunk = fobj.read(size)
            if not chunk:
                break
            length = len(chunk)
            if (length < size) and (index < (lenfobjs - 1)):
                remsize = size - length
                chunk = chunk + fobjs[index + 1].read(remsize)
            yield chunk
        index += 1
        fobj.close()


def detectcode(fpath):
    """使用 chardet 探测文件编码。"""
    detector = UniversalDetector()
    fobj = open(fpath, "rb")
    while not detector.done:
        chunk = fobj.read(4096)
        if not chunk:
            break
        detector.feed(chunk)
    fobj.close()
    detector.close()
    return detector.result["encoding"]


def samepath(p1, p2):
    """比较两个路径是否相同。"""
    return normpath(normcase(p1)) == normpath(normcase(p2))


def chunksize(num, limit):
    """获取较合适的每次读取字符的数量。"""
    if num <= limit:
        return num
    begin = 1
    while num > limit:
        begin += 1
        result = num // begin
        if result > limit:
            continue
        return result


class TextFiles:
    def __init__(self, *items):
        self.__items = list()
        self.initialize(items)

    def initialize(self, items):
        """
        初始化的相关操作。

        设置文本文件路径，如果 coding 为 None，则使用 chardet 获取文件编码。
        """
        for item in items:
            if isinstance(item, (tuple, list)):
                fpath, coding, *_ = item
                if not isinstance(coding, (str, _NONETYPE)):
                    raise TypeError(f"参数'{item}'[1](编码)数据类型应为字符串。")
                _LOGGER.debug(f"初始化参数中文件'{fpath}'编码标记：{coding}。")
            elif isinstance(item, str):
                fpath, coding = item, None
                _LOGGER.debug(f"'TextFiles'初始化时，参数中文件'{fpath}'无编码标记。")
            else:
                raise TypeError("参数数据类型错误，类型应为字符串或元组、列表。")
            if not isinstance(fpath, str):
                raise TypeError(f"参数'{item}'的第一个元素(路径)类型应为字符串。")
            if not isfile(fpath):
                raise ValueError(f"不存在'{item}'的第一个元素(路径)所指的文件。")
            if coding is None:
                coding = detectcode(fpath)
                _LOGGER.debug(f"文件'{fpath}'的编码被探测为：{coding}。")
            if not coding:
                coding = _CODING
                _LOGGER.debug(f"文件'{fpath}'编码探测失败，使用默认编码：{coding}。")
            self.__items.append((abspath(fpath), coding))
            _LOGGER.debug(f"文件'{fpath}'的编码已被标记为：{coding}。")

    def files(self):
        """
        返回一个生成器。

        遍历生成器可获得本实例中所有的文件路径。
        """
        for item in self.__items:
            yield item[0]

    def items(self):
        return self.__items[:]

    def totalsize(self):
        """返回实例中所有文件的总大小，单位'字节'。"""
        return sum(getsize(fp) for fp in self.files())

    def __len__(self):
        return len(self.__items)

    def __add__(self, other):
        if not isinstance(other, TextFiles):
            paramtype = type(other).__name__
            raise TypeError(f"不支持的相加操作数类型：'TextFiles'和'{paramtype}'。")
        return TextFiles(*self.__items, *other.items())

    def __radd__(self, other):
        return self.__add__(other)

    def onefile(self, filepath, sep="", newcoding=None, overwrite=False):
        """
        将多个文件合并成一个文件

        :param filepath: str, 创建合并的文件的路径。

        :param sep: str|Callable -> str, 合并的文件中，每个子文件内容之间的分隔符。

        sep可为字符串或总是返回字符串且不接受参数的可调用对象。

        :param newcoding: str|None, 合并的文件的新编码，为 None 时使用默认编码。

        :param overwrite: bool, 如果 filepath 所指文件已存在，overwrite 为 True 则覆盖，否则追加写入。
        """
        if not isinstance(filepath, str):
            raise TypeError("路径参数'filepath'值类型应为字符串。")
        if not isinstance(sep, (str, Callable)):
            raise TypeError("分隔符参数'sep'值类型应为字符串或可调用对象。")
        if not isinstance(newcoding, (str, _NONETYPE)):
            raise TypeError("编码参数'newcoding'值类型应为字符串。")
        for fp in self.files():
            if not samepath(fp, filepath):
                continue
            raise FileExistsError(f"将创建的文件'{filepath}'与将合并的文件同名。")
        if len(self.__items) == 1:
            fp = self.__items[0][0]
            return shutil.copyfile(fp, filepath)
        ec = newcoding or _CODING
        if overwrite:
            os.remove(filepath)
        with open(filepath, "a", encoding=ec) as nfo:
            for fp, ec in self.__items:
                for block in fschunk((fp, ec)):
                    nfo.write(block)
                if isinstance(sep, str):
                    chapter_sep = sep
                else:
                    chapter_sep = sep()
                if chapter_sep:
                    nfo.write(chapter_sep)  # 写入分隔符，默认为空字符串
        return filepath

    def sizedfiles(self, charnum, startfp, newcoding=None):
        """
        将文件分割成指定大小(以字符计数)的子文件。

        :param charnum: int > 0, 分割的子文件每个文件的字符数。

        :param startfp: str, 起始文件名，子文件名取 startfp + '_' + 序号。

        :param newcoding: str, 子文件的新编码，为 None 时使用默认编码。
        """
        if not isinstance(charnum, int):
            paramtype = type(charnum).__name__
            raise TypeError(f"预期参数'filesize'值类型为'int'，非'{paramtype}'。")
        if charnum <= 0:
            raise ValueError("不支持分割成小于等于0个字符的子文件。")
        if not isinstance(startfp, str):
            paramtype = type(startfp).__name__
            raise TypeError(f"预期参数'startfp'值类型为'str'，非'{paramtype}'。")
        if not isinstance(newcoding, (str, _NONETYPE)):
            paramtype = type(newcoding).__name__
            raise TypeError(f"预期参数'newcoding'值类型为'str'，非'{paramtype}'。")
        ec = newcoding or _CODING
        readsize = chunksize(charnum, _CHUNKSIZE)

        def fileobjs():
            """文件对象生成器。"""
            serial, fd = 1, dirname(startfp)
            pre, suf = splitext(basename(startfp))
            while True:
                current = join(
                    fd,
                    f"{pre}_{serial}{suf}",
                )
                yield open(current, "a", -1, ec)
                serial += 1

        fileobjgen, remsize = fileobjs(), charnum
        fileobject = next(fileobjgen)
        for chunk in fschunk(*self.__items, size=readsize):
            fileobject.write(chunk)
            remsize -= len(chunk)
            if remsize <= 0:
                remsize = charnum
                fileobject.close()
                fileobject = next(fileobjgen)

    @classmethod
    def fromstring(cls, string, savepath, coding=None):
        """
        ### 从字符串实例化一个 TextFiles 类实例。

        本类方法会先在 savepath 位置创建一个文本文件，然后返回该文件的 TextFiles 实例。

        如果已存在 savepath 文件，则会抛出 FileExistsError 异常。

        :param savepath: str, 创建的文本文件路径；

        :param coding: str, 创建的文本文件使用的编码；

        :param string: str, 写入创建的文本文件的字符串。

        :return: TextFiles, 返回 TextFiles 实例。
        """
        coding = coding or _CODING
        if not isinstance(string, str):
            paramtype = type(string).__name__
            raise TypeError(f"预期参数'string'值类型为'str'，非'{paramtype}'。")
        if not isinstance(savepath, str):
            paramtype = type(savepath).__name__
            raise TypeError(f"预期参数'savepath'值类型为'str'，非'{paramtype}'。")
        if exists(savepath):
            raise FileExistsError(f"文件'{savepath}'已存在。")
        if not isinstance(coding, (str, _NONETYPE)):
            paramtype = type(coding).__name__
            raise TypeError(f"预期参数'coding'值类型为'str'，非'{paramtype}'。")
        filedirname = dirname(savepath)
        if not exists(filedirname):
            os.makedirs(filedirname)
        elif not isdir(filedirname):
            raise ValueError(f"文件路径'{savepath}'的父目录名称已被文件占用。")
        with open(savepath, "wt", encoding=coding) as fobj:
            fobj.write(string)
        return cls((savepath, coding))
