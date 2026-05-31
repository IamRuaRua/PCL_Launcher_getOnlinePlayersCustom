# get_online_players

一个用于查询 Minecraft Java 版服务器在线玩家，并生成 `Custom.xaml` 布局内容的 Flask 服务，可在PCL启动器中自动更新在线玩家。

## 文件说明

- `xaml_server.py`：Flask 服务入口
- `layout_generator.py`：根据玩家列表生成 XAML 字符串
- `Custom.xaml`：生成后的布局文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
python xaml_server.py
```

服务启动后监听 `5001` 端口。

## 接口说明使用说明

```
http://127.0.0.1:5001/onlineplayers?server=192.168.1.1:25565
```

在PCL启动器中 "设置>主页>联网更新"下方的输入框输入此链接，刷新主页后即可显示布局
