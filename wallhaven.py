import requests
from lxml import etree
import threading

# 获取需要壁纸的网页源码
def get_content(search,page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    url = 'https://wallhaven.cc/search?'
    data = {
        'q': search,
        'page': page
    }
    response = requests.get(url=url, params=data, headers=headers)
    content = response.text
    return content

# 获取总页数
def how_page(content):
    tree = etree.HTML(content)
    pages = tree.xpath('//section[@class="thumb-listing-page"]//h2/text()')[1].split(' ')[-1]
    return pages

# 下载
def get_image_url(content):
    tree = etree.HTML(content)
    # 获取 图片名字 与 url
    name = tree.xpath('//div[@id="thumbs"]//li/figure/@data-wallpaper-id')
    url = tree.xpath('//div[@id="thumbs"]//li/figure/img/@data-src')

    image_url_list = []
    for i in range(len(name)):
        image_name = name[i]
        # 得到高清大图的 url
        bast_url = url[i].replace('/th.','/w.').replace('small','full').replace(image_name,'wallhaven-'+ image_name)

        # 获取png图片的信息
        png_get = tree.xpath('//figure[@data-wallpaper-id="%s"]//span[@class="png"]/span/text()' % image_name)

        # 将 jpg 和 png 的图片分开处理
        if png_get:
            image_url = bast_url.replace('.jpg', '.png')
        else:
            image_url = bast_url
        # print(image_url)
        image_url_list.append(image_url)

    # print(image_url_list)
    return image_url_list

def down_load(image_url_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
        # 获取图片源码
    for i in image_url_list:
        url_code = requests.get(url=i,headers=headers)
        image_code = url_code.content
        file_name = './15.wallhaven 自定义壁纸/' + i.split('/')[-1]
        # 写入文件夹
        with open(file_name,'wb')as fp:
            fp.write(image_code)


if __name__ == '__main__':
    search = input("需要哪种的壁纸：") # 必须为英文
    content = get_content(search,page=2)
    pages = how_page(content)
    page_li = int(input('总共有 %s 页，需要几页：'  %pages)) + 1
    for page in range(1,page_li):
        # 获取网页源码
        content = get_content(search,page)
        # 获取图片高清大图
        image_url_list = get_image_url(content)
        # 多线程下载
        down_thread = threading.Thread(target=down_load,args=(image_url_list,))
        down_thread.start()