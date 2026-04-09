#!/usr/bin/env python3
import argparse
import asyncio
import aiohttp
import time
import requests
from urllib.parse import urlparse

async def test_latency(session, proxy, target='http://httpbin.org/ip', timeout=5):
    start = time.time()
    try:
        async with session.get(target, proxy=proxy, timeout=timeout) as resp:
            latency = time.time() - start
            return latency, resp.status == 200
    except:
        return float('inf'), False

async def bench_proxy(proxy_url, speed=False, timeout=5):
    connector = aiohttp.TCPConnector(limit=1)
    async with aiohttp.ClientSession(connector=connector) as session:
        latency, success = await test_latency(session, proxy_url, timeout=timeout)
        print(f'Latency: {latency:.2f}s, Success: {success}')
        if speed:
            # Download speed test
            start = time.time()
            async with session.get('http://httpbin.org/bytes/1024', proxy=proxy_url, timeout=timeout) as resp:
                data = await resp.read()
                speed = len(data) / (time.time() - start) / 1024
                print(f'Speed: {speed:.2f} KB/s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('proxy', help='Proxy URL e.g. socks5://127.0.0.1:1080')
    parser.add_argument('--speed', action='store_true')
    parser.add_argument('--timeout', type=int, default=5)
    args = parser.parse_args()
    asyncio.run(bench_proxy(args.proxy, args.speed, args.timeout))

