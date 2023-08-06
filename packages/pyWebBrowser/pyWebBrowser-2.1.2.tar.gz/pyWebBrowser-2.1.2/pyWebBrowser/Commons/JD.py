# -*- coding: utf-8 -*-

import cv2
import numpy as np
from pyzbar.pyzbar import decode
from time import sleep
from base64 import b64decode
from collections import Counter

class BusinessBG:
    def __init__(self):
        self = self

    def Login(self, pattern: dict):
        '''
        JD 商家后台登录。
        注意: 仅作为学习交流之用, 不得作为包含但不限于恶意或非法采集, 攻击, 售卖等行为的操作载体。
        让我们携手共建安全友好的互联网数据采集分析环境。
        如果有幸能被 JD 的小伙伴指导一二, 将不胜荣幸。 
        如果 JD 的小伙伴发现且认为该功能不宜公开, 可通过邮件告知, 将第一时间下架, 万分感谢。

        『强烈注意：由于无法确定是否可以进行长期维护, 建议仅作为代码的交流, 最好不要引入项目。造成任何不良影响恕无法承担。』
        :param pattern: 登录参数。必填, 且格式必须正确。
                        screenWidth  : 屏幕宽度
                        screenHeight : 屏幕高度
                        browserWidth : 浏览器宽度
                        browserHeight: 浏览器高度
                        loginName    : 登录名
                        loginPassword: 登录密码
                        browserObj   : 浏览器对象。仅支持 pyWebBrowser.Browser()
                        screenshotObj: 屏幕截图对象。仅支持 pyWebBrowser.Screenshot()
                        mouseObj     : 鼠标控制对象。仅支持 pyWebBrowser.Mouse()
                        keyboardObj  : 键盘控制对象。仅支持 pyWebBrowser.Keyboard()
                        clipboardObj : 剪切板对象。仅支持 pyWebBrowser.Clipboard()
        '''
        screenWidth = pattern['screenWidth']
        screenHeight = pattern['screenHeight']

        browserWidth = pattern['browserWidth']
        browserHeight = pattern['browserHeight']

        offsetX = int((screenWidth - browserWidth) / 2)
        offsetY = int((screenHeight - browserHeight) / 2)

        loginName = pattern['loginName']
        loginPassword = pattern['loginPassword']

        browser = pattern['browserObj']
        screenshot = pattern['screenshotObj']
        mouse = pattern['mouseObj']
        keyboard = pattern['keyboardObj']
        clipboard = pattern['clipboardObj']

        # 打开京东登录页面
        browser.Open('https://passport.shop.jd.com/login/index.action')
        sleep(2)

        # 图像识别等待切换登录输入框
        loginAreaX = -1
        loginAreaY = -1
        while True:
            loginType = self.__loginType(
                screenshotObj = screenshot,
                startX = offsetX,
                startY = offsetY,
                endX = offsetX + browserWidth,
                endY = offsetY + browserHeight
            )

            if loginType['type'] == 'qrcode':
                loginAreaX = offsetX + loginType['x']
                loginAreaY = offsetY + loginType['y']
                mouse.Move(loginAreaX + 320, loginAreaY + 20)
                sleep(1)

                mouse.LeftClick()
                sleep(1)
            elif loginType['type'] == 'inputbox':
                break

        # 输入登录账号
        clipboard.Set(loginName)
        mouse.SmoothMove(loginAreaX + 320, loginAreaY + 20, loginAreaX + 263, loginAreaY + 109, 5)
        sleep(1)
        mouse.LeftClick()
        sleep(1)
        keyboard.KeyCombination(['ctrl', 'v'])
        sleep(1)

        # 输入登录密码
        clipboard.Set(loginPassword)
        mouse.SmoothMove(loginAreaX + 263, loginAreaY + 109, loginAreaX + 268, loginAreaY + 157, 5)
        sleep(1)
        mouse.LeftClick()
        sleep(1)
        keyboard.KeyCombination(['ctrl', 'v'])
        sleep(1)

        # 回车执行登录
        keyboard.KeyPress('enter')
        sleep(3)

        # 执行验证码识别
        while True:
            img_base64 = screenshot.AnySize(loginAreaX + 36, loginAreaY + 113, loginAreaX + 316, loginAreaY + 221)
            img_base64Decode = b64decode(img_base64.replace('data:image/png;base64,', ''))
            VerificationOffsetX = self.__imageVerification(imgBase64 = img_base64Decode)

            if VerificationOffsetX == None: break
            
            mouse.SmoothMove(loginAreaX + 268, loginAreaY + 157, loginAreaX + 61, loginAreaY + 252, 5)
            sleep(0.5)
            mouse.LeftDown()
            sleep(0.5)
            mouse.SmoothMove(loginAreaX + 61, loginAreaY + 252, loginAreaX + 61 + 39 * 1.4 + VerificationOffsetX, loginAreaY + 252, 5)
            sleep(0.5)
            mouse.SmoothMove(loginAreaX + 61 + 39 * 1.4 + VerificationOffsetX, loginAreaY + 252, loginAreaX + 61 + 39 + VerificationOffsetX, loginAreaY + 252, 5)
            sleep(0.5)
            mouse.LeftUp()

            sleep(2)

    def __loginArea(self, imgPath: str = None, imgBase64: str = None):
        '''
        选择登录区域
        '''
        img = None
        if imgPath != None:
            imagePath = imgPath
            img = cv2.imread(imagePath)
        elif imgBase64 != None:
            img_array = np.fromstring(imgBase64, np.uint8)
            img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
        
        result = []
        try:
            # 灰度化
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # 二值化
            ret3, img_threshold = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # 寻找区域
            contours, w1 = cv2.findContours(img_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for item in contours:
                x, y, width, height = cv2.boundingRect(item)

                # 返回宽高均在 300 ~ 500 之间的色块
                if 300 < width < 500 and 300 < height < 500:
                    imgItem = img[y :  y + height, x : x + width]
                    result.append(
                        {
                            'img': imgItem,
                            'x': x,
                            'y': y
                        }
                    )
        except: pass

        return result

    def __qrcode(self, img):
        '''
        识别二维码登录类型
        '''
        # 灰度化
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 边缘检测
        img_sobel = cv2.Sobel(img_gray, cv2.CV_8UC1, 1, 1, ksize = 5)
        # 二值化
        ret3, img_threshold = cv2.threshold(img_sobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # 闭合零散边缘
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
        img_morphologyEx = cv2.morphologyEx(img_threshold, cv2.MORPH_CLOSE, kernelX)
        # 边缘膨胀使其形成完整区域
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        img_dilate = cv2.dilate(img_morphologyEx, kernelX)
        img_erode = cv2.erode(img_dilate, kernelX)

        # 寻找区域
        contours, w1 = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for item in contours:
            x, y, width, height = cv2.boundingRect(item)

            # 返回宽高均满足 130 ~ 160 之间的色块
            if 130 < width < 160 and 130 < height < 160:
                imgItem = img[y :  y + height, x : x + width]

                # 识别二维码内容是否为 JD 登录链接
                try:
                    qrcodeInfo = decode(imgItem)[0].data.decode()
                    if 'https://jm.jd.com?login' in qrcodeInfo: return True
                except:
                    pass
        
        return False
    
    def __inputbox(self, img):
        '''
        识别输入框登录类型
        '''
        # 灰度化
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 边缘检测
        img_sobel = cv2.Sobel(img_gray, cv2.CV_8UC1, 0, 1, ksize = 3)
        # 二值化
        ret3, img_threshold = cv2.threshold(img_sobel, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # 闭合零散边缘
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 35))
        img_morphologyEx = cv2.morphologyEx(img_threshold, cv2.MORPH_CLOSE, kernelX)
        # 边缘膨胀
        kernelX = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        img_dilate = cv2.dilate(img_morphologyEx, kernelX)
        img_erode = cv2.erode(img_dilate, kernelX)

        # 寻找区域
        contours, w1 = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for item in contours:
            x, y, width, height = cv2.boundingRect(item)

            # 返回宽满足 300 ~ 315 之间且高满足 200 ~ 215 之间的色块
            if 300 < width < 315 and 200 < height < 215:
                if width / height > 1:
                    return True
        
        return False

    def __imageVerification(self, demoPath: str = 'demo.png', imgPath: str = None, imgBase64: str = None):
        '''
        获取图像验证位置
        '''
        img = None
        if imgPath != None:
            imagePath = imgPath
            img = cv2.imread(imagePath)
        elif imgBase64 != None:
            img_array = np.fromstring(imgBase64, np.uint8)
            img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)

        # 裁剪图像验证码的识别区域
        height, width, channel = img.shape
        img = img[:height, 39 : width]

        # 灰度化
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 图像转数组
        img_array = np.array(img_gray)
        # 计算图像色值的中位数、平均值、众数、极差
        # 最后将这几个数字取平均数, 作为基数
        # 在二值化计算时通过逐步分解来达到从图像中分离出缺块的目的
        median = np.median(img_array)
        mean = np.mean(img_array)
        mode = int(Counter([str(x) for x in [*img_array.flat]]).most_common(1)[0][0])
        max_min = (np.max(img_array) - np.min(img_array)) / 2

        threshold = np.mean([median, mean, mode, max_min])

        # 读取 demo 图
        demoBase64 = 'iVBORw0KGgoAAAANSUhEUgAAACYAAAAmAQAAAACARtQDAAAATElEQVR4nJXOoQ2AMBgF4S9tJQMgSNh/C0bpCBUIRNMfgQQSMGfe5eVEXaMntZFsB0KOnsCdkF/XZ9+iYdJRdDBAfPi5nIGSdsx/G07HxBTTeGT9XAAAAABJRU5ErkJggg=='
        demo_array = np.fromstring(b64decode(demoBase64), np.uint8)
        img_demo = cv2.imdecode(demo_array, cv2.COLOR_RGB2BGR)
        demoImgWidth, demoImgHeight = img_demo.shape

        # demo 图转数组
        demoImgArray = np.array(img_demo / 255, dtype = np.int)
        # 计算 demo 图的总像素数量
        demoImgTotal = demoImgWidth * demoImgHeight

        # 根据实测结果以及对识别系数分布情况的统计
        # 结合识别效率, 将识别系数区间设置为 0.5 ~ 4 之间
        diffRateDict = {}
        for cofficient in range(5, 40):
            # 根据不同系数对主图进行二值化
            ret3, img_threshold = cv2.threshold(img_gray, threshold / (cofficient / 10), 255, cv2.THRESH_BINARY)

            # 读取图片宽高
            # 根据图片宽高每隔 3 个像素点剪切一个与 demo 图尺寸一致的图片
            # 以此图片与 demo 图做盖印对比
            # 如果同位置的像素点一致, 盖印结果为 0, 否则为 1 或 -1
            # 通过统计盖印结果为 0 的数量, 与 demo 图的总像素数量对比, 此为识别率
            # 识别率为 85% 及以上的直接判定为『直接识别有效』, 直接返回结果
            # 否则将识别率为 70% 及以上的存入识别字典
            # 在无识别结果满足『直接识别有效』要求时
            # 最后以识别字典中识别率最高的最为『间接识别有效』, 输出结果
            imgWidth, imgHeight = img_threshold.shape
            for width in range(0, imgWidth, 3):
                for height in range(0, imgHeight, 3):
                    cropImg = img_threshold[height : height + demoImgHeight, width : width + demoImgWidth]
                    cropImgArray = np.array(cropImg / 255, dtype = np.int)

                    if len(cropImg) == 38:
                        if np.sum(demoImgArray) * 0.9 < np.sum(cropImgArray) < np.sum(demoImgArray) * 1.1:
                            diffArray = demoImgArray - cropImgArray
                            diff = Counter([str(x) for x in [*diffArray.flat]])['0']
                            diffRate = diff / demoImgTotal
                            
                            if diffRate >= 0.85:
                                return width
                            elif diffRate >= 0.7:
                                diffRateDict[diffRate] = width

        if len(diffRateDict) > 0:
            best = sorted(diffRateDict, reverse = True)[0]
            return diffRateDict[best]

    def __loginType(self, screenshotObj, startX, startY, endX, endY) -> str:
        while True:
            img_base64 = screenshotObj.AnySize(startX, startY, endX, endY)
            img_base64Decode = b64decode(img_base64.replace('data:image/png;base64,', ''))

            loginAreaList = self.__loginArea(imgBase64 = img_base64Decode)
            if len(loginAreaList) > 0:
                for item in loginAreaList:
                    img = item['img']
                    x = item['x']
                    y = item['y']

                    if self.__qrcode(img): return { 'type': 'qrcode', 'x': x, 'y': y }
                    if self.__inputbox(img): return { 'type': 'inputbox', 'x': x, 'y': y }
            sleep(1)