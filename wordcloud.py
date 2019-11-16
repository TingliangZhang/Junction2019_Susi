# 导入wordcloud模块和matplotlib模块
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
# 读取一个txt文件
text = open('test1.txt','r').read()
# 读入背景图片
bg_pic = imread('3.png')
# 生成词云
wordcloud = WordCloud(mask=bg_pic,background_color='white',scale=1.5).generate(text)
# image_colors = ImageColorGenerator(bg_pic)
# 显示词云图片
plt.imshow(wordcloud)
plt.axis('off')
plt.show()