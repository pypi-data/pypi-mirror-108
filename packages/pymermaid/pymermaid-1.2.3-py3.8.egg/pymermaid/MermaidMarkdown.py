from pymermaid import mermaid_js
#import mermaid_js #发布时候将本条注释，取消上一条注释

#构造Markdown代码
tags = '''
graph TD
    A[构造markdown代码]-->B[构造HTML网页代码]
    B-->C[浏览器渲染]
    C-->D[返回png字节]
    C-->F
    D-->E[转换为plot图像]
    E-->F[plot显示]
'''

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

    html_footer = '''
         </div>
         <script src="/storage_data/个人/20210427龙根星/20210000安排/附件/NAS/JUPYTER_MERMAID/js/mermaid.min.js"></script>
         <script>mermaid.initialize({startOnLoad:true});</script>
        </body>
        </html>
    '''

    html_page_source = html_header + "<script type='text/javascript>'" + mermaid_js.mermaid_js + "</script>" + html_graph_start + tags +  html_footer

    #保存这个网页
    with open("/tmp/mermaid_js.html", "w+") as f:
        f.write(html_page_source)

    from selenium import webdriver

    opts = webdriver.chrome.options.Options()
    opts.add_argument('--headless')

    wdobj = webdriver.Chrome(options=opts)
    file = "file:///tmp/mermaid_js.html"
    res = wdobj.get(file)
    
    #调整窗口大小，截取元素的全图
    width = wdobj.execute_script(
            "return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
    height = wdobj.execute_script(
            "return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

    wdobj.set_window_size(width, height)
    
    pic = wdobj.find_element_by_class_name("mermaid")
        
    png1 = pic.screenshot_as_png
    pic.screenshot("/storage_data/个人/20210427龙根星/20210000安排/附件/NAS/JUPYTER_MERMAID/src/pymermaid/test.png")

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