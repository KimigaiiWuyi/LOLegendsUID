HOST = 'https://www.wegame.com.cn'
LOL_API = '/api/v1/wegame.pallas.game.LolBattle'
TFT_API = '/api/v1/wegame.pallas.game.TftBattle'

SearchAPI = f"{HOST}{LOL_API}/SearchPlayer"
SummonerAPI = f'{HOST}{LOL_API}/GetSummonerInfo'
BattleListAPI = f'{HOST}{LOL_API}/GetBattleList'
UserLabelAPI = f'{HOST}{LOL_API}/GetUserLabel'
PlayerRecentAPI = f'{HOST}{LOL_API}/GetPlayerRecentStat'
PlayerProfileAPI = f'{HOST}{LOL_API}/GetPlayerProfile'
PlayerChampionAPI = f'{HOST}{LOL_API}/GetChampion'
PlayerSkinAPI = f'{HOST}{LOL_API}/GetSkin'
BattleReportAPI = f'{HOST}{LOL_API}/GetBattleReport'
BattleDetailAPI = f'{HOST}{LOL_API}/GetBattleDetail'
UserSnapshotAPI = f'{HOST}{LOL_API}/GetUserSnapshot'

TFTGameCareerAPI = f'{HOST}{TFT_API}/GetGameCareer'
TFTBattleListAPI = f'{HOST}{TFT_API}/GetBattleList'
TFTBattleReportAPI = f'{HOST}{TFT_API}/GetBattleReport'
TFTBattleDetailAPI = f'{HOST}{TFT_API}/GetBattleDetail'

QQ101_BASE = 'https://game.gtimg.cn/images/lol/act/img/js'
HERO_LIST_API = f'{QQ101_BASE}/heroList/hero_list.js'
HERO_DETAIL = f'{QQ101_BASE}/hero/' + '{}.js'

IMG_BASE = 'https://wegame.gtimg.com/g.26-r.c2d3c/helper'
IMG_HOST = f'{IMG_BASE}/lol/assis'
ResAPI = f'{IMG_HOST}/images/resources'
SkinLoadingAPI = 'https://game.gtimg.cn/images/lol/act/img/skinloading'
# 物品 40*40px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/items/1058.png
# 英雄竖版 180*327px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/card/201.jpg
# 天赋ICON 108*108px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/runesperk/9923.png
# 皮肤立绘 1280*720px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/skins/splash/53-036.jpg
# 皮肤load 308*560px
# https://game.gtimg.cn/images/lol/act/img/skinloading/382b165c-6e15-472e-952e-87a6bd022346.jpg
# 原始皮肤立绘 900*620px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/skins/original/119-000.jpg
# 用户头像 70*70px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/usericon/4661.png
# 英雄的头像 74*74px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/champions/136.png
# 召唤师技能ICON 40*40px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/assis/images/resources/summonability/32.png
# 段位ICON 130*130px
# https://wegame.gtimg.com/g.26-r.c2d3c/helper/lol/v2/tier/tier-7.png
