from pymermaid import mermaid_js
#import mermaid_js #发布时候将本条注释，取消上一条注释

#构造Markdown代码
tags='''
graph TD
    start_proc>开始]-->detecting[系统检测]
    detecting-->reachable{目标IP是否可达}
    reachable--IP可达-->detecting
    
    reachable--IP不可达-->confirm[运行通知程序]
    
    confirm--选择-->weichat_or_sms{选择短信或微信}
    
    weichat_or_sms--0-->send_sms[短信发送]
    weichat_or_sms--1-->send_weichat[微信发送]
    
    send_sms-->shutdown
    send_weichat-->shutdown[运行]
    shutdown-->end_proc>结束]
    
    end_proc-->A
    A-->B
    B-->C
    C-->D
    D-->E
    E-->F
'''
#放到浏览器中去渲染出图像，并且使用selenium截图节点获得图像
def render(tags=tags,conf_axis="off",figsize=False, dpi=72):
    import os
    cpath = os.getcwd()
    
    #构造HTML网页代码
    html_header = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
        </head>
        <body>
    '''

    html_graph_start = '''
    <div class='mermaid'>
    '''
    
    html_graph_end = '''
    </div>
    '''
    html_footer = '''
        <script src="file://{0}/mermaid.min.js"></script>
        <script>mermaid.initialize({{startOnLoad:true}});</script>
        </body>
        </html>
    '''.format(cpath)

    html_page_source = html_header  + html_graph_start + tags + html_graph_end  +  html_footer
    
    
    #保存这个js脚本
    with open("{0}/mermaid.min.js".format(cpath), "w+") as f:
        f.write(mermaid_js.mermaid_js)

    #保存这个网页
    with open("{0}/mermaid_js.html".format(cpath), "w+") as f:
        f.write(html_page_source)

    from selenium import webdriver

    #opts = webdriver.chrome.options.Options()
    #opts.add_argument('--headless')
    opts = webdriver.firefox.options.Options()
    opts.add_argument('-headless')

    #wdobj = webdriver.Chrome(options=opts)
    wdobj = webdriver.Firefox(options=opts)
    file = "file://{0}/mermaid_js.html".format(cpath)
    res = wdobj.get(file)
    
    #调整窗口大小，截取元素的全图
    width = wdobj.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
    height = wdobj.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

    wdobj.set_window_size(width, height)
    
    pic = wdobj.find_element_by_class_name("mermaid")
        
    png1 = pic.screenshot_as_png
    
    from PIL import Image
    from io import BytesIO
    import matplotlib.pyplot as plt

    png2 =Image.open(BytesIO(png1))
    
    #检测图像的大小
    if not figsize:
        w, h = png2.size
        figsize = (w/dpi, h/dpi)    
    
    plt.figure(figsize=figsize, dpi=dpi)

    plt.axis(conf_axis)
    plt.imshow(png2)

    plt.show()

#test
if __name__ == '__main__':
    render()