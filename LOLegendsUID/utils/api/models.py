from typing import Dict, List, Union, Literal, TypedDict


class ResultInfo(TypedDict):
    error_code: int
    error_message: str


class PlayerInfo(TypedDict):
    openid: str
    '''真正的用户UID'''
    area: int
    '''大区信息'''
    icon_id: int
    level: int
    '''用户等级(456)'''
    tier: int
    '''段位信息(255 -> 无段位)'''
    queue: int
    '''段位信息(0 -> I)'''


class ExtInfo(TypedDict):
    lpl: str


class SummonerInfo(TypedDict):
    id: int
    '''用户的ID'''
    name: str
    '''用户的名称'''
    level: int
    '''用户等级(456)'''
    experience: int
    '''用户经验'''
    icon_id: int
    praise: int
    '''点赞数'''
    discredit: int
    '''点踩数'''
    top_of_canyon: bool
    '''是否开启峡谷之巅'''
    openid: str
    '''真正的用户UID'''
    ext: ExtInfo


class GameLevelInfo(TypedDict):
    tier: str
    league_points: str
    rank: str


class BattleInfo(TypedDict):
    game_id: str
    game_start_time: str
    game_time_played: int
    map_id: int
    game_queue_id: int
    was_mvp: int
    was_svp: int
    was_early_surrender: int
    play_gt25_mask: int
    game_server_version: str
    champion_id: int
    position: str
    skin_index: int
    game_score: int
    team_id: str
    win: Literal['Win', 'Fail']
    kills: int
    deaths: int
    assists: int
    gold_earned: int
    was_surrender: int
    was_afk: int
    most_kills: int
    most_assists: int
    most_minions_killed: int
    most_gold_earned: int
    most_damage_dealt_to_champions: int
    most_total_damage_taken: int
    most_turrets_killed: int
    double_kills: int
    triple_kills: int
    quadra_kills: int
    penta_kills: int
    unreal_kills: int
    game_level: str
    win_with_less_teammate: int
    team_made_size: int
    battle_type: int
    player_subteam: str
    player_subteam_placement: str


class CommonChampionInfo(TypedDict):
    key: int
    '''单个英雄ID'''
    value: int
    '''使用次数'''


class CommonPositionInfo(TypedDict):
    Key: Literal['UTILITY', 'JUNGLE', 'MIDDLE', 'TOP', 'BOTTOM']
    '''位置'''
    Value: int
    '''所有位置这个value加起来等于20, 可用于计算百分比'''


class RecentStateInfo(TypedDict):
    kill_30days: int
    death_30days: int
    assist_30days: int
    win_times: int
    play_times: int
    last_game_id: str
    '''最后一场比赛的Game_id'''
    kda: int
    '''KDA(9270 = 9.3)除100并四舍五入保留一位小数'''
    last_game_time: str
    '''最后一场比赛的时间戳, 1705390492179'''
    common_use_champions: List[CommonChampionInfo]
    common_position: List[CommonPositionInfo]


class GameCareerInfo(TypedDict):
    total_mvp_times: int
    '''总MVP次数'''
    total_svp_times: int
    '''总SVP次数'''
    total_god_likes: int
    '''总超神次数'''
    total_penta_kills: int
    '''总五杀次数'''
    total_quadra_kills: int
    '''总四杀次数'''
    total_triple_kills: int
    '''总三杀次数'''
    max_consecutive_wins: int
    '''最高连胜次数'''
    highest_game_score: int
    '''最高评分(167138 = 16.7)除10000并保留一位小数'''
    most_kills_num: int
    '''最高杀人次数'''
    most_assists_num: int
    '''最高助攻数'''
    most_spree_kills_num: int
    '''最高连杀数'''
    most_damage_num: int
    '''最高伤害数'''
    most_damage_taken_num: int
    '''最高承伤数'''
    most_gold_earned_num: int
    '''最高经济数'''
    most_minions_kill_num: int
    '''最高补刀数'''
    most_turrets_kill_num: int
    '''最高拆塔数'''
    total_kills: int
    '''全部击杀数量'''
    total_assists: int
    '''全部助攻数量'''
    total_ward_placed: int
    '''不知道是啥'''
    longest_game_num: int
    '''较长对局数量'''
    shortest_game_num: int
    '''较短对局数量'''


class PlayerStatsApiResponse(TypedDict):
    result: ResultInfo
    recent_state: RecentStateInfo
    game_career: GameCareerInfo


class ChampionInfo(TypedDict):
    champion_id: int
    '''英雄的ID'''
    total: int
    '''总对局数'''
    wins: int
    '''总获胜数'''
    expire_day: int
    '''还有多少天到期, 永久的话是0'''
    used_exp: int
    '''英雄熟练度'''
    instance_id: str
    '''唯一的实例ID'''
    lanes: List[str]
    '''这个是可能存在的分录, 例如mid、support等等'''
    sid_exp: int
    '''不知道是啥'''


class SkinInfo(TypedDict):
    id: int
    '''皮肤的ID'''
    expire_day: int
    '''还有多少天到期, 永久的话是0'''
    instance_id: str
    '''唯一的实例ID'''
    create_time: str
    '''获得时间戳 1610081250'''
    chromas: int
    '''是否是炫彩皮肤'''
    hero_id: int
    '''原本API不提供，自己加入的'''


class SkinChampionInfo(TypedDict):
    id: int
    expire_day: int
    skins: List[SkinInfo]
    instance_id: str


class PlayerSkinAPIResponse(TypedDict):
    result: ResultInfo
    championSkins: List[SkinChampionInfo]
    champion_num: int
    skin_num: int


class ChampionSkin(TypedDict):
    heroId: str
    skinId: str


class Profiles(TypedDict):
    cardbg: str
    '''{bgType:1,championSkin:{heroId:887,skinId:887011}}'''
    label: str
    ''''''
    showExpType: str
    '''0'''
    skincabinet: str
    '''[{heroId:887,skinId:887011}, ... ,] * 4'''
    skincabinetshow: str
    '''1'''
    tag: str
    ''''''


class SeasonInfo(TypedDict):
    sid: int
    total: int
    wins: int
    losses: int
    tier: int
    win_point: int
    queue: int
    team_total: int
    team_wins: int
    team_losses: int
    team_tier: int
    team_win_point: int
    team_queue: int


class PlayerStats(TypedDict):
    total_match_games: int
    total_match_wins: int
    total_match_losts: int
    total_arm_games: int
    total_arm_wins: int
    total_arm_losts: int
    total_rank_games: int
    total_rank_wins: int
    total_rank_losts: int
    total_teamrank_games: int
    total_teamrank_wins: int
    total_teamrank_losts: int
    total_games: int
    total_wins: int
    total_losts: int
    total_ai_games: int
    total_ai_wins: int
    total_ai_losts: int
    total_clash_games: int
    total_clash_wins: int
    total_clash_losts: int


class BattleReportAPIResponse(TypedDict):
    result: ResultInfo
    battle_count: PlayerStats
    season_list: List[SeasonInfo]


class BattleHonour(TypedDict):
    gameLevel: str
    isDoubleKills: int
    isGodlike: int
    isLargestAllMinionsKilled: int
    isLargestAssists: int
    isLargestChampionsKilled: int
    isLargestGoldEarned: int
    isLargestTotalDamageDealtToChampions: int
    isLargestTotalDamageTaken: int
    isLargestTurretsKilled: int
    isMvp: int
    isPentaKills: int
    isQuadraKills: int
    isSvp: int
    isTripleKills: int
    isUnrealKills: int
    isWinWithLessTeammate: int
    isZeroDeath: int


class PlayerDetails(TypedDict):
    PERK0: int
    PERK1: int
    PERK2: int
    PERK3: int
    PERK4: int
    PERK5: int
    STAT_PERK_0: int
    STAT_PERK_1: int
    STAT_PERK_2: int
    allMinionsKilled: int
    assists: int
    baronKills: int
    barracksKilled: int
    battleHonour: BattleHonour
    championId: int
    championUsedExp: int
    championsKilled: int
    consumablesPurchased: int
    doubleKills: int
    dragonKills: int
    exp: int
    gameScore: int
    goldEarned: int
    goldSpent: int
    hqKilled: int
    item0: int
    item1: int
    item2: int
    item3: int
    item4: int
    item5: int
    item6: int
    itemsPurchased: int
    keystoneId: int
    killingSpress: int
    largestCriticalStrike: int
    largestKillingSpree: int
    largestMultiKill: int
    level: int
    loginIp: str
    lolId: str
    lpl: str
    magicDamageDealtPlayer: int
    magicDamageTaken: int
    magicDamageToChampions: int
    minionsKilled: int
    name: str
    neutralMinionsKilled: int
    numDeaths: int
    openid: str
    original_area_id: str
    original_lol_id: str
    original_puu_id: str
    pentaKills: int
    perkStyle: int
    perkSubStyle: int
    physicalDamageDealtPlayer: int
    physicalDamageTaken: int
    physicalDamageToChampions: int
    playerAugment1: int
    playerAugment2: int
    playerAugment3: int
    playerAugment4: int
    playerSubteam: str
    playerSubteamPlacement: str
    position: str
    puuId: str
    quadraKills: int
    sightWardsBoughtInGame: int
    skinIndex: int
    skinInfoFor2V2Json: str
    spell1Cast: int
    spell2Cast: int
    spell3Cast: int
    spell4Cast: int
    summonSpell1Cast: int
    summonSpell1Id: int
    summonSpell2Cast: int
    summonSpell2Id: int
    teamId: str
    teamMadeSize: int
    timeCcingOthers: int
    totalDamageDealt: int
    totalDamageTaken: int
    totalDamageToChampions: int
    totalHealth: int
    totalTimeSpentDead: int
    translate_areaId: str
    tripleKills: int
    trueDemageToChampions: int
    turretsKilled: int
    uinId: str
    unrealKills: int
    visionScore: int
    visionWardsBoughtInGame: int
    wardKilled: int
    wardPlaced: int
    wardPlacedDetector: int
    wardSkinIndex: int
    wasAfk: int
    win: str


class BanInfo(TypedDict):
    championId: int
    pickTurn: int
    teamId: str


class TeamDetails(TypedDict):
    banInfoList: List[BanInfo]
    isSurrender: int
    teamElo: int
    teamId: str
    totalAssists: int
    totalBaronKills: int
    totalBaseKilled: int
    totalDampenKilled: int
    totalDeaths: int
    totalDragonKills: int
    totalGoldEarned: int
    totalKills: int
    totalTurretsKilled: int
    win: str


class BattleDetail(TypedDict):
    area_id: str
    game_id: str
    game_start_time: str
    game_time_played: int
    map_id: int
    game_queue_id: int
    game_mode: str
    game_type: str
    platform_id: str
    was_early_surrender: int
    play_gt25_mask: int
    game_server_version: str
    team_details: List[TeamDetails]
    player_details: List[PlayerDetails]


class UserSnapshot(TypedDict):
    category: int
    game_time: int
    file_url: str
    auth_url: str
    desc: str
    game_id: str
    commit_time: str
    ss_idx: int
    action_type: int
    game_type: int
    champion_id: int
    player_name: str
    killed_champion_id: int
    killed_player_name: str
    killed_enemy_count: int
    team_color: int
    queue_id: int
    exdata: str


class TFTGameCareer(TypedDict):
    total: int
    '''总共游玩次数'''
    top1: int
    '''第一名次数'''
    win_rate: str
    '''登顶率 / 870（8.70%）（需要除10000）'''
    top3: int
    '''前三次数'''
    top_three_rate: str
    '''前三率 / 2464（24.64%）（需要除10000）'''
    average_ranking: str
    '''平均排名 / 393（3.93）（需要除100）'''


class TFTItem(TypedDict):
    id: int
    name: str
    character_id: str
    chosen: str
    items: List[str]
    star_num: int
    base_price: int
    piece_price: int
    itemNames: List[str]


class TFTBattleList(TypedDict):
    area: int
    game_id: str
    game_match_type: int
    ranking: int
    end_time: str
    achievements: List[Union[int, str]]
    pieces: List[TFTItem]
    game_score: int
    snapshot: bool


class TFTSeasonItem(TypedDict):
    game_type: int
    total: int
    top1: int
    win_rate: str
    top3: int
    top_three_rate: str
    tier: int
    queue: int
    win_point: int
    turbo_rank_title: str


class TFTSeason(TypedDict):
    sid: int
    name: str
    items: List[TFTSeasonItem]


class TFTMatch(TypedDict):
    game_type: int
    total: int
    top1: int
    win_rate: str
    top3: int
    top_three_rate: str
    tier: int
    queue: int
    win_point: int
    turbo_rank_title: str


class TFTBattleReport(TypedDict):
    result: ResultInfo
    match: TFTMatch
    seasons: List[TFTSeason]


class Trait(TypedDict):
    name: str
    num_units: int
    style: int
    tier_current: int
    tier_total: int
    id: int


class Companion(TypedDict):
    content_id: str
    skin_id: int
    species: str


class Piece(TypedDict):
    id: int
    name: str
    character_id: str
    chosen: str
    items: List[str]
    star_num: int
    base_price: int
    piece_price: int
    itemNames: List[str]


class MemberExploit(TypedDict):
    openid: str
    nickname: str
    head_icon_id: str
    total_damage_to_players: int
    gold_left: int
    blood: int
    total_trait_num: int
    active_trait_num: int
    traits: List[Trait]
    companion: Companion
    time_eliminated: float
    ranking: int
    game_score: int
    piece_list_price: int
    level: int
    players_eliminated: int
    piece_list: List[Piece]
    augmentsStr: str
    game_rank_list: List[Dict]


class TFTBattleDetail(TypedDict):
    game_id: str
    end_time: str
    game_match_type: int
    duration: int
    tft_set_number: int
    set_name: str
    member_exploit_list: List[MemberExploit]
    areaId: int
