#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: thepoy
# @Email: thepoy@163.com
# @File Name: colort.py
# @Created:  2021-05-27 08:32:47
# @Modified: 2021-06-05 09:48:24

from typing import NewType

Style = NewType("style", int)


class _Mode:
    """模式"""

    @property
    def normal(self) -> Style:
        """终端默认样式"""
        return Style(0)

    @property
    def bold(self) -> Style:
        """高亮或加粗"""
        return Style(1)

    @property
    def underline(self) -> Style:
        """下划线"""
        return Style(4)

    @property
    def blink(self) -> Style:
        """闪烁"""
        return Style(5)

    @property
    def invert(self) -> Style:
        """反白"""
        return Style(7)

    @property
    def hide(self) -> Style:
        """隐藏"""
        return Style(8)


class _ForegroundColor:
    """前景色 / 文字颜色"""

    @property
    def black(self) -> Style:
        """黑色"""
        return Style(30)

    @property
    def red(self) -> Style:
        """红色"""
        return Style(31)

    @property
    def green(self) -> Style:
        """绿色"""
        return Style(32)

    @property
    def orange(self) -> Style:
        """橙色"""
        return Style(33)

    @property
    def blue(self) -> Style:
        """蓝色"""
        return Style(34)

    @property
    def purple(self) -> Style:
        """紫色"""
        return Style(35)

    @property
    def cyan(self) -> Style:
        """青色"""
        return Style(36)

    @property
    def white(self) -> Style:
        """白色"""
        return Style(37)


class _BackgroudColor:
    """背景色"""

    @property
    def black(self) -> Style:
        """黑色"""
        return Style(40)

    @property
    def red(self) -> Style:
        """红色"""
        return Style(41)

    @property
    def green(self) -> Style:
        """绿色"""
        return Style(42)

    @property
    def orange(self) -> Style:
        """橙色"""
        return Style(43)

    @property
    def blue(self) -> Style:
        """蓝色"""
        return Style(44)

    @property
    def purple(self) -> Style:
        """紫色"""
        return Style(45)

    @property
    def cyan(self) -> Style:
        """青色"""
        return Style(46)

    @property
    def white(self) -> Style:
        """白色"""
        return Style(47)


class DisplayStyle:
    foreground_color = _ForegroundColor()
    backgorud_color = _BackgroudColor()
    mode = _Mode()

    @property
    def end(self) -> Style:
        return Style(0)

    def format_with_one_style(self, src: str, style: Style) -> str:
        """用一种样式格式化输出的文字

        Parameters
        ----------
        src : {str}
            待格式化的源文字
        style : {Style}
            要使用的样式

        Returns
        -------
        str
            格式化后的文字

        Raises
        ------
        TypeError
            源文字或样式不是要求的类型时抛异常
        """
        if type(src) != str:
            raise TypeError(f"type of `src` is {type(src)}, not str")

        if type(style) != Style and type(style) != int:
            raise TypeError(f"type of `style` is {type(style)}, not Style or int")

        fmt = "\033[%dm%s\033[%dm"
        return fmt % (style, src, self.end)

    def format_with_multiple_styles(self, src: str, *styles: Style) -> str:
        """用多种样式格式化输出的文字

        Parameters
        ----------
        src : {str}
            待格式化的源文字
        *styles : {[Style]}
            要使用的样式，需要输入两种或以上的样式

        Returns
        -------
        str
            格式化后的文字

        Raises
        ------
        TypeError
            源文字或某一个样式不是要求的类型时抛异常
        """
        if type(src) != str:
            raise TypeError(f"type of `src` is {type(src)}, not str")

        if len(styles) < 2:
            raise TypeError("At least two styles")

        styles_str = []

        for style in styles:
            if type(style) != Style and type(style) != int:
                raise TypeError(f"type of `style` is {type(style)}, not Style or int")
            styles_str.append(str(style))

        style = ";".join(styles_str)
        return f"\033[{style}m{src}\033[{self.end}m"
