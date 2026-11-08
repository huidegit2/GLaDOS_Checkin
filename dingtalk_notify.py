#!/usr/bin/env python3
"""把 GLaDOS 签到结果推送到钉钉机器人（支持加签，仅用标准库）。"""
import os, time, hmac, hashlib, base64, urllib.parse, json, urllib.request

WEBHOOK = os.environ.get('DINGTALK_WEBHOOK', '').strip()
SECRET = os.environ.get('DINGTALK_SECRET', '').strip()
LOG = os.environ.get('CHECKIN_LOG', 'checkin_result.log')
STATUS = os.environ.get('CHECKIN_STATUS', 'unknown')


def main():
    if not WEBHOOK:
        print('[钉钉] 未配置 DINGTALK_WEBHOOK，跳过通知')
        return
    try:
        text = open(LOG, encoding='utf-8', errors='replace').read().strip()
    except OSError:
        text = ''
    if len(text) > 1600:
        text = '...(前略)...\n' + text[-1600:]
    content = 'GLaDOS 签到通知（任务状态：{})\n{}'.format(STATUS, text or '（签到脚本无输出）')
    url = WEBHOOK
    if SECRET:
        ts = str(round(time.time() * 1000))
        string_to_sign = '{}\n{}'.format(ts, SECRET)
        sign = urllib.parse.quote_plus(base64.b64encode(
            hmac.new(SECRET.encode(), string_to_sign.encode(), hashlib.sha256).digest()
        ))
        sep = '&' if '?' in url else '?'
        url = '{}{}timestamp={}&sign={}'.format(url, sep, ts, sign)
    payload = json.dumps({'msgtype': 'text', 'text': {'content': content}}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print('[钉钉] 推送结果:', r.status, r.read().decode('utf-8', 'replace')[:200])
    except Exception as e:
        print('[钉钉] 推送失败:', e)


if __name__ == '__main__':
    main()
