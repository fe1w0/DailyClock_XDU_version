# DailyClock_XDU_version

本项目，只用测试使用。
若造成麻烦或者其他问题，概不负责，也请issues联系。

# Usage

需要先在`config.py`中设置账户。

## 打卡

![](https://imgapp.xidian.edu.cn/image/3/c79542c7e343b40237be127b328846f0.jpg)

```bash
python clock.py
```

推荐crontab，定时打卡

```bash
0 7-21/3 * * * /root/miniconda3/bin/python /root/Tools/life/DailyClock_XDU_version/clock.py >> /root/Tools/life/DailyClock_XDU_version/xidiandailyup_log
```

```json
{"e":0,"m":"操作成功","d":{"amstart":"6:00","amend":"12:00","pmstart":"12:01","pmend":"18:00","image":"image/3/c79542c7e343b40237be127b328846f0.jpg","title":"晨午晚检","desc":"温馨提示： 不外出、不聚集、 戴口罩、勤洗手、开窗通风、发热就诊"}}
```

## 生成课程表

生成的课程表，可以直接导入到 wake up 课程表中

```bash
python courseQuery.py
```
![image](https://user-images.githubusercontent.com/50180586/188258290-95dbf261-a669-44d6-bb04-fbe861d5f22b.png)

课程表导入后
![image](https://user-images.githubusercontent.com/50180586/188258572-3c0c020a-1067-4b73-b935-115dfcd53335.png)

## 抢课

在选择系统登录后获取复制想要抢课的课程代码即可粘贴到`config.py`

```python
course_KCDM = "X1HA0001"     # 需要抢课的课程代码
sleep_time = 60 			# 刷新的频率60s，可以根据需要更改
```

刷新频率可以根据需要设置，建议间隔长一些

```python
python courseChoose.py
```

当课程容量已经满的时候，输入结果如下

```
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
[+] 当前课程容量已满!
```

选课成果如下

```
[+] 选课成功!
[+] 课程信息如下:
[+] 课程名称: 人工智能01
[+] 上课时间和地点: 2-5,7-9周 星期四[5-8节]1-104<br>2-5周 星期五[1-2节]1-104<br>7-9周 星期五[1-4节]1-104
[+] 任课教师: 陈璞花,李玲玲
```