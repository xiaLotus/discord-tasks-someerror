from discord.ext import commands, tasks
from core.classes import Cog_Extension
from datetime import datetime, timezone, timedelta
import asyncio
from pathlib import Path
import os
import discord
import pytz
import datetime

class DailyTasks(Cog_Extension):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.send_message_daily.start()
        self.clean_yesterday_file.start()


    @tasks.loop(seconds = 60)
    async def send_message_daily(self):
        now = datetime.datetime.now()
        # 每天定時新增一個txt
        file_path = f'cmds_log/{now.date()}.txt' 

        # 如果每天的0點0分和文件不存在這兩個因素達成
        if now.hour == 0 and now.minute == 47 and not os.path.exists(file_path):
            print('指令收到')
            channel = self.bot.get_channel(1047167757499768902)
            # 傳送訊息到channel
            await channel.send('大家睡覺囉！')
            # 打開文件寫入
            with open(file_path, 'w', encoding = 'utf-8') as file:
                file.write(f'{now.date()}')
        else:
            print('沒收到')
        
    @tasks.loop(hours = 24)
    async def clean_yesterday_file(self):
        # 得到現在時間
        today = datetime.datetime.now()
        # 找到昨天的日期
        yesterday = today - datetime.timedelta(days = 1)
        # 日期格式化，如2023-10-28
        yesterday_date_str = yesterday.strftime('%Y-%m-%d')

        # 如果檔案在cmds_log內
        for filename in os.listdir('cmds_log'):
            # 檔案開頭是日期 + 檔案結尾是txt
            if filename.startswith(yesterday_date_str) and filename.endswith('.txt'):
                # file_path example -> cmds_log/2023-10-28.txt
                file_path = os.path.join('cmds_log', filename)
                # 刪除該檔案
                os.remove(file_path)
                # 輸出刪除檔案名稱
                print(f'刪除-{file_path}')
    
    # 在clean_yesterday_file這個def運行之前使用
    @clean_yesterday_file.before_loop
    async def before_delete_the_files(self):
        # 等discord bot完全準備就緒後才會開始活動
        await self.bot.wait_until_ready()

        # 找尋現在時間
        now = datetime.datetime.now()
        # 目標時間設置每日的8點5分
        target_time = datetime.time(8, 5)
        # 找尋每日的8點5分
        target_datetime = datetime.datetime(now.year, 
                                            now.month,
                                            now.day, 
                                            target_time.hour,
                                            target_time.minute
                                            )
        # 計算到8點5分有多少秒
        time_until_target = (target_datetime - now).total_seconds()
        # 等待秒數
        await asyncio.sleep(time_until_target)


async def setup(bot: commands.Bot):
    await bot.add_cog(DailyTasks(bot))