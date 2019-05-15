# TODO LIST

### 数据库设计+ORM  :heavy_check_mark:

- <del>UserRecord</del> 【optional】​
  - userId：Char
  - inTime：Datetime
  - outTime：Datetime
  - 说明：进店时插入userId,inTime（outTime NULL），离店时更新outTime
- RunLog
  - currenttime：DATETIME
  - userid：CHAR
  - roomid：CHAR
  - temperature：FLOAT
  - windspeed：INT
  - status：INT   （0：关机 1：制冷  -1：制热）



### Logger 日志模块

url:`localhost:/logger/?method=X&....`

- QueryReport ：查询报表

  - url：`localhost:/logger/?method=query&rooms=XXX&date=XXX&type=XXX`

  - room格式："-"分割

  - date格式：`YY-MM-DD-HH-mm-SS`

  - type格式：“month”or“week”or“day”

  - 返回json格式

    ```json
    {
       "roomLength": 1~4,
        "roomDetails":[
            {"roomId":X,""}
        ]
    }
    ```

    



### Statistic 统计（计费）模块

- 临时费用公式：$\sum_{each second} (50+status*temperature*windspeed)*0.1$
- 

