# Pinyin2Chinese
Self complemented Pinyin2Chinese demo use algorithms including Trie and HMM model , 基于隐马尔科夫模型与Trie树的拼音切分与拼音转中文的简单demo实现。  
# 项目介绍  
Pinyin2Chinese ，基于隐马尔科夫模型与Trie树的进行拼音切分与中文转换两个任务。   
# 1、拼音切分    
类似于中文分词，需要将用户输入的字母拼音转换成对应的拼音列表，如‘woaini’--> ['wo', 'ai', 'ni']，这是拼音转文字的第一步，这一步包括跨音节的问题，如xian,可以对应['xi', 'an'] 以及['xian']两种切分结果。本项目利用可能的拼音集合，构建trie字典树，随后采用字典树查找的方式完成切分。  
# 2、拼音转文字  
完成步骤1）后，需要基于给定的拼音序列，计算得出符合拼音序列以及概率最大化的汉字序列。  
本项目采用的HMM模型，并用viterbi算法计算最大化概率。  
具体流程包括：  
1）基于抓取的搜狗输入法词库，一共是770W个词条，作为训练语料    
2）利用汉字拼音标注工具，pypinyin进行拼音转换    
3）分别计算拼音到汉字的发射概率，如p(wo|我);汉字到汉字的转移概率，如p(欢|喜)，p(喜|B)，p(欢|E),其中B表示词条的开始，E表示词条的末尾。  
4) 计算拼音序列的最大化生成概率，此处使用维特比算法进行求解。  
例如，从['wo', 'ai' ,'ni'] -> ['我'，'爱'，'你']  
p(我爱你|wo ai ni) = p(我|wo)p(我|B)p(爱|ai)p(爱|我)p(你|ni)p(你|爱)p(你|E)  
此处涉及到的转移概率较为重要，对效果影响很大，对于较长的句子转换，效果还不是很好。   
# 使用简介
# 拼音序列切分    
from pinyincut import *  
cuter = PinyinCut()  
cuter.cut(sent)  
----------------------------------------------------------  
yiqungaoguiqizhidechairenzaichufaweizhangdongwu  
['yi', 'qun', 'gao', 'gui', 'qi', 'zhi', 'de', 'chai', 'ren', 'zai', 'chu', 'fa', 'wei', 'zhang', 'dong', 'wu']  
lianggehuanglimingcuiliu  
['liang', 'ge', 'huang', 'li', 'ming', 'cui', 'liu']  
yihangbailushangqingtian  
['yi', 'hang', 'bai', 'lu', 'shang', 'qing', 'tian']  
renshengdeyixunjinhuanmoshijinzunkongduiyue  
['ren', 'sheng', 'de', 'yi', 'xun', 'jin', 'huan', 'mo', 'shi', 'jin', 'zun', 'kong', 'dui', 'yue']  
ziranyuyanchulishiyigelishinantideyuyanzhedetianxia  
['zi', 'ran', 'yu', 'yan', 'chu', 'li', 'shi', 'yi', 'ge', 'li', 'shi', 'nan', 'ti', 'de', 'yu', 'yan', 'zhe', 'de', 'tian', 'xia']  

# 拼音转文字  
from pinyin2chinese import *    
transer = PinyinWordTrans()      
transer.trans(sent) 
----------------------------------------------------------  
woshizhongguoren   
['我', '是', '中', '国', '人']  
beijingkejidaxue  
['北', '京', '科', '技', '大', '学']  
zhongguokexueyuanruanjianyanjiusuo  
['中', '国', '科', '学', '院', '软', '件', '研', '究', '所']  
lianggehuanglimingcuiliu  
['梁', '个', '黄', '丽', '明', '翠', '柳']  
woainizhongguo  
['我', '爱', '你', '中', '国']  

