# -*- coding: utf-8 -*-

import subprocess

CMD_PREFIX = 'source ~/.bash_profile && '

def execute_shell(cmd):
    """执行命令并获得返回的值
    执行通过给与的命令
    
    Args:
        cmd: 需要执行的操作系统命令
    Return: 
        True/False, stdout, stderr
        返回是否执行成功, 已经相关输出
    Raise: None
    """

    cmd = '{prefix} {cmd}'.format(
          prefix = CMD_PREFIX,
          cmd = cmd)
    child = subprocess.Popen(cmd, 
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    child.wait()
    err_code = child.poll()
    stdout = child.stdout.read()
    stderr = child.stderr.read()

    is_ok = False

    if err_code == 0:
        is_ok = True
    
    return is_ok, stdout, stderr
