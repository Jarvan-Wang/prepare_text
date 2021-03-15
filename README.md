用于处理训练集与测试集text文本
训练集： 
1、尝试对中文使用jiema进行分词，若失败，则尝试将词分为字，若再失败则跳过此行 
2、对英文单词进行全角转半角、大写转小写 
3、去除标点符号 
4、若行中出现不存在于symtab中的词（OOV），则不输出此行 
示例：
python3 ~/prepare_text/prepare_train_text.py data/lang_chain_2y_hunshu/words.txt data/train/text data/train/text.nooov

测试集： 
1、将中文词转换为字，并用空格隔开 
2、在中文和英文之间插入空格 
3、对英文单词进行全角转半角、大写转小写 
4、去除标点符号
示例：
python3 ~/prepare_text/prepare_test_text.py data/lang_chain_2y_hunshu/words.txt data/test/text data/test/text.nooov