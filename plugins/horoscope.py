import logging

from random import randint

import plugins

logger = logging.getLogger( __name__ )
bot = plugins.tracking.bot

@bot.message_handler( func=lambda message: True )
def horoscope( message ):
    keyword = [ "今日運勢", "今天運勢", "明日運勢", "明天運勢", "今晚運勢", "明晚運勢", "後天運勢", "後日運勢" ]
    keyword2 = [ "昨日運勢", "昨天運勢" ]
    keyword3 = [ "中秋節運勢", "中秋運勢" ]

    for x in range( len( keyword ) ):
        if message.text.find( keyword[ x ] ) > -1:
            if randint( 0, 2000 ) == 0:
                bot.reply_to( message, "你的{}為農到一個女朋友".format( keyword[x] ) )
                return
            elif randint( 0, 2000 ) == 0:
                bot.reply_to( message, "你的{}為農到一個男朋友".format( keyword[x] ) )
                return
            _horoscope_day( keyword[x], message )
            return

    for x in range( len( keyword2 ) ):
        if message.text.find( keyword2[ x ] ) > -1:
            bot.reply_to( message, "昨天都過完了你還問！！" )
            return

def _horoscope_day( day, message ):
    horoscope_list = [ \
"大吉：出門農塔都是VERY RARE", \
"大吉：檢舉的飛人帳號已經被鎖，爽！", \
"大吉：獲得成就黑金一面", \
"大吉：農塔姿勢太帥被告白", \
"中吉：農到爆倉", \
"小吉：遇見藍軍行動八塔團", \
"小吉：收到過點通知Portal Live!!!", \
"小吉：Destroy金牌就在今天", \
"小吉：解任務遇到好心藍軍幫忙", \
"小吉：路邊捕獲野生新手", \
"吉：看見帥哥玩家", \
"吉：農到紅桶", \
"吉：可以撿尾刀補CF"]
    horoscope_list2 = [ \
"凶：申請的Portal全部被Reject", \
"凶：撞到休閒玩家", \
"凶：改名打錯字，r打成t", \
"凶：link錯塔", \
"凶：上錯mod，上到LA", \
"凶：農塔農到一半遇到下雨", \
"凶：花光所有us，沒掉半個盾", \
"凶：上了一個hs還是完全沒key", \
"凶：點被移除", \
"凶：手機沒電", \
"凶：與到藍軍互刷刷光所有物資", \
"凶：邊開車邊滑手機，被警察開單", \
"大凶：不小心把成就塔的 KEY 燒了", \
"大凶：每次計劃都會卡到自己的成就點（切身之痛T_T）", \
"大凶：玩 ingress 太晚回家，被另一半誤認為有小三XD", \
"大凶：邊騎車邊滑手機，手機想不開跳樓", \
"大凶：手機不慎掉入水中", \
"大凶：馬桶上四LA被轉綠", \
"大凶：上了兩個hs還是完全沒key", \
"大凶：馬桶點被移除", \
"大凶：燒錯mod，燒到VR的", \
"大凶：recycle到塞滿八砲的膠囊", \
"大凶：連行動電源也沒電", \
"大凶：被盜帳號，飛去南極然後被鎖帳號", \
"超凶：遇到脾氣不好的正妹" ]
    if randint( 0, 10 ) >= 3:
        bot.reply_to( message, "你的{}為{}".format( day,horoscope_list[ randint( 0, len(horoscope_list)-1 )] ) )
    else:
        bot.reply_to( message, "你的{}為{}".format( day,horoscope_list2[ randint( 0, len(horoscope_list2)-1 )] ) )

def _moon_festival ( message ):
    horoscope_list = [ \
"吉：農塔農到一半掉落一盒月餅" ,\
"吉：農塔農到一半掉落一盒綠豆椪" ,\
"吉：撿到月餅" ,\
"吉：撿到烤肉" ,\
"吉：撿到柚子" ,\
"吉：撿到野生的柚子，帶回家養" ,\
"吉：有玩家送你柚子" ,\
"吉：月亮出來露臉" ,\
"吉：老闆給的禮品獎金特別多" ,\
"吉：有友軍玩家邀請到他家過中秋" ,\
"吉：農到玉兔" ,\
"吉：吃掉玉兔" ,\
"吉：農到吳剛" ,\
"吉：農到嫦娥" ,\
"吉：吃掉嫦娥（？" ,\
"中：被天上掉下來的嫦娥壓到" ,\
"凶：農塔農到一半掉落一盒被吃過的月餅" ,\
"凶：月餅吃到吐" ,\
"凶：烤肉吃到吐" ,\
"凶：肉跟你裝熟" ,\
"大兇：吃太多月餅拉肚子"
]

