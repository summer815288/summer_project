#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:Lijiacai
Email:1050518702@qq.com
===========================================
CopyRight@JackLee.com
===========================================
"""
import base64
import os
import sys
import json
import asyncio
import time
import numpy as np
import cv2
from pyppeteer import launch
from PIL import Image, ImageChops
import matplotlib.pyplot as plt

launch_args = {
    "headless": False,
    "args": [
        # "--start-maximized",
        # "--disable-infobars",
        # "--ignore-certificate-errors",
        # "--log-level=3",
        # "--enable-extensions",
        # "--window-size=1920,1080",
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
    ],
}


async def get_decode_image(filename, data):
    _, img = data.split(",")
    img = base64.b64decode(img)
    with open(filename, "wb") as f:
        f.write(img)


async def main():
    browser = await launch(**launch_args)
    page = await browser.newPage()
    await page.setJavaScriptEnabled(enabled=True)
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    # 设置浏览器语言
    await page.evaluate(
        '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en-US', 'en'] }); }''')
    # 设置插件
    await page.evaluate(
        '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    await page.setViewport({"width": 1920, "height": 1080})
    await page.goto(url="http://sd.gsxt.gov.cn/index.html")
    page.setDefaultNavigationTimeout(0)
    await page.waitForXPath("//input[@id='keyword']")
    print(1)
    await asyncio.sleep(2)
    print(2)
    elem = await page.xpath("//input[@id='keyword']")
    print(3)
    await elem[0].type("百度")
    print(4)
    await asyncio.sleep(2)
    print(5)
    await page.waitForXPath("//img[@id='btn_query']")
    print(6)
    elem = await page.xpath("//img[@id='btn_query']")
    print(7)
    await elem[0].click()
    print(8)
    await asyncio.sleep(3)
    print(9)

    fulljs = """
        () => { return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png") }
        """
    fadejs = """
        () => { 
                return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png")}
        """
    full_img = await page.evaluate(fulljs)
    await get_decode_image(filename="fullbg.png", data=full_img)
    await asyncio.sleep(0.1)
    fade_img = await page.evaluate(fadejs)
    await get_decode_image(filename="fadebg.png", data=fade_img)
    await asyncio.sleep(0.1)
    a = await compute_gap(img1="fullbg.png", img2="fadebg.png")
    elem = await page.xpath("//div[@class='geetest_slider_button']")
    await elem[0].hover()
    await page.mouse.down()
    await page.mouse.move(int(840 + a), 450)
    await page.mouse.up()

    await asyncio.sleep(1000)
    await browser.close()


async def compute_gap(img1, img2):
    """计算缺口偏移 这种方式成功率很高"""
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    # 将图片修改为RGB模式
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # 计算差值
    diff = ImageChops.difference(img1, img2)

    plt.figure('pokemon')
    plt.imshow(diff, cmap='gray')
    plt.show()
    table = []
    for i in range(256):
        if i < 50:
            table.append(0)
        else:
            table.append(1)
    # 灰度图
    diff = diff.convert("L")
    #
    # # 二值化
    diff = diff.point(table, '1')
    # print(diff.getbbox())  # 这里可以直接获取差异坐标点坐标顺序为左上右下
    #
    left = 43
    # # 这里做了优化为减少误差 纵坐标的像素点大于5时才认为是找到
    # # 防止缺口有凸起时有误差
    for w in range(left, diff.size[0]):
        lis = []
        for h in range(diff.size[1]):
            if diff.load()[w, h] == 1:
                lis.append(w)
            if len(lis) > 5:
                return w


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())