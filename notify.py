#!/usr/bin/env python3
"""把 GLaDOS 签到结果通过邮件发送（仅用标准库 + mailer.py）。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mailer

LOG = os.environ.get('CHECKIN_LOG', 'checkin_result.log')
STATUS = os.environ.get('CHECKIN_STATUS', 'unknown')


def main():
    try:
        text = open(LOG, encoding='utf-8', errors='replace').read().strip()
    except OSError:
        text = ''
    if len(text) > 1600:
        text = '...(前略)...\n' + text[-1600:]
    content = 'GLaDOS 签到通知（任务状态：{})\n{}'.format(
        STATUS, text or '（签到脚本无输出）')
    subject = 'GLaDOS 签到通知 - ' + ('成功' if STATUS == 'success' else '失败')
    try:
        mailer.send_mail(subject, content)
    except Exception as e:
        print('[邮件] 发送异常:', e)


if __name__ == '__main__':
    main()
