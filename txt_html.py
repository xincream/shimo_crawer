# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import re
import cgi


def shimo_format(text):
    text = split_code_apart(text)
    text = add_html_tags(text)
    return text


def add_html_tags(text):
    lines = text.split('<block>')
    html_text = ''
    for line in lines:
        if line.startswith('\n\n<pre>'):
            html_text += line
        else:
            text_lines = line.split('\n\n')
            for text_line in text_lines:
                if text_line == '\n':
                    html_text += '<br>'
                    continue
                text_line = convert_html(text_line)
                html_text += '<p>\n' + text_line.replace('\n', '<br>\n') + '</p>\n'
    return html_text


def split_code_apart(text):
    lines = text.split('\n')
    if len(lines) <= 1:
        return text
    apart_text = ''
    code_flag = False
    for i in range(0, len(lines) - 1):
        if lines[i].startswith('*'):
            if not code_flag:
                # 代码块开始
                apart_text += '<block>\n\n<pre>\n<code>'
                code_flag = True
        else:
            if code_flag:
                # 代码块结束
                apart_text += '</code>\n</pre>\n\n<block>'
                code_flag = False
        apart_text += convert_html(lines[i][1:]) + '\n' if code_flag else convert_html(lines[i]) + '\n'
        ## 总体去除一些无用的换行
        apart_text = re.sub('\n\n+', '\n\n', apart_text)
    return apart_text


def convert_html(line):
    return line
    # return cgi.html.escape(line)


