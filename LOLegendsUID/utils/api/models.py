from typing import List, TypedDict


class ResultInfo(TypedDict):
    error_code: int
    error_message: str


class PlayerInfo(TypedDict):
    openid: str
    area: int
    icon_id: int
    level: int
    tier: int
    queue: int


class ExtInfo(TypedDict):
    lpl: str


class SummonerInfo(TypedDict):
    id: int
    name: str
    level: int
    experience: int
    icon_id: int
    praise: int
    discredit: int
    top_of_canyon: bool
    openid: str
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
    win: str
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
    value: int


class CommonPositionInfo(TypedDict):
    Key: str
    Value: int


class RecentStateInfo(TypedDict):
    kill_30days: int
    death_30days: int
    assist_30days: int
    win_times: int
    play_times: int
    last_game_id: str
    kda: int
    last_game_time: str
    common_use_champions: List[CommonChampionInfo]
    common_position: List[CommonPositionInfo]


class GameCareerInfo(TypedDict):
    total_mvp_times: int
    total_svp_times: int
    total_god_likes: int
    total_penta_kills: int
    total_quadra_kills: int
    total_triple_kills: int
    max_consecutive_wins: int
    highest_game_score: int
    most_kills_num: int
    most_assists_num: int
    most_spree_kills_num: int
    most_damage_num: int
    most_damage_taken_num: int
    most_gold_earned_num: int
    most_minions_kill_num: int
    most_turrets_kill_num: int
    total_kills: int
    total_assists: int
    total_ward_placed: int
    longest_game_num: int
    shortest_game_num: int


class PlayerStatsApiResponse(TypedDict):
    result: ResultInfo
    recent_state: RecentStateInfo
    game_career: GameCareerInfo


class ChampionInfo(TypedDict):
    champion_id: int
    total: int
    wins: int
    expire_day: int
    used_exp: int
    instance_id: str
    lanes: List[str]
    sid_exp: int


class SkinInfo(TypedDict):
    id: int
    expire_day: int
    instance_id: str
    create_time: str
    chromas: int


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


class BanInfo(TypedDict):
    champion_id: int
    ban_turn: int
    ban_type: str


class BattleHonour(TypedDict):
    player_id: int
    honors: int
    double_kills: int
    triple_kills: int
    quadra_kills: int
    penta_kills: int
    legendary_kills: int
    total_damage_dealt: int
    total_damage_taken: int
    total_healing_done: int
    total_gold_earned: int
    total_minions_killed: int
    vision_score: int


class PlayerDetails(TypedDict):
    account_id: str
    sum_id: str
    exp: int
    level: int
    level_xp: int
    rank_xp: int
    ranked: int
    league_id: int
    loss: int
    wins: int
    order_num: int
    games: int
    league: int
    name: str
    division: int
    placement_games: int
    is_placement: int
    variation_lvl: int
    battle_royale_wins: int
    placement_games_team: int
    is_placement_team: int
    variation_lvl_team: int
    created: str
    updated: str
    game_name: str
    is_oob_available: bool
    is_ability_haste_active: bool
    ban_info: List[BanInfo]
    battle_honours: List[BattleHonour]


class TeamDetails(TypedDict):
    account_id: str
    sum_id: str
    exp: int
    level: int
    level_xp: int
    rank_xp: int
    ranked: int
    league_id: int
    loss: int
    wins: int
    order_num: int
    games: int
    league: int
    name: str
    division: int
    placement_games: int
    is_placement: int
    variation_lvl: int
    battle_royale_wins: int
    placement_games_team: int
    is_placement_team: int
    variation_lvl_team: int
    created: str
    updated: str
    game_name: str
    is_oob_available: bool
    is_ability_haste_active: bool
    ban_info: List[BanInfo]
    battle_honours: List[BattleHonour]


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
