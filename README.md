
## Usage
### 1. install python3
### 2. install pip and markdown
```
pip install pelican
pip install markdown
```
### 3. write a blog in md
```
Title: 文章标题
Date: 创建日期
Modified: 修改日期
Category: 文章分类，标志本文处于该分类下
Tags: 文章标签，标志本文处于该标签下
Slug: URL中该文章的链接地址
Author: 作者
```
save in path `./content/`

### 4. make html
```
make html
```
or 
```
pelican ./content/ -o ./output -s ./pelicanconf.py
```
> If you don't have `make` command, the second command can work.
### 5 start blog 
```
make server
```
or 
```
cd ./output
python -m pelican.server
```

### 6. visit blog
open your browser, and visit http://localhost:8000
