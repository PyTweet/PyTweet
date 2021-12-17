from enum import Enum


class RelationsTypeEnum(Enum):
    PENDING = 0
    ACCEPT = 1
    LIKED = 2
    RETWEETED = 3
    HIDE = 4
    NULL = None


class MessageTypeEnum(Enum):
    DIRECT_MESSAGE = 0
    MESSAGE_TWEET = 1
    MESSAGE_WELCOME_MESSAGE = 2
    MESSAGE_WELCOME_MESSAGE_RULE = 3
    NULL = None


class MessageEventTypeEnum(Enum):
    MESSAGE_CREATE = "message_create"
    MESSAGE_DELETE = "message_delete"
    NULL = None


class ButtonType(Enum):
    web_url = "web_url"


class SpaceState(Enum):
    live = "live"
    scheduled = "scheduled"


class ReplySetting(Enum):
    everyone = "everyone"
    mention_users = "mentionedUsers"
    following = "following"


class MediaType(Enum):
    photo = "photo"
    video = "video"
    gif = "gif"


class ActionEventType(Enum):
    direct_message_read = "direct_message_mark_read_events"
    direct_message_typing = "direct_message_indicate_typing_events"


class UserActionEventType(Enum):
    follow = "follow_events"
    block = "block_events"
    unmute = "mute_events"


class Timezone(Enum):
    international_date_line_west = "Etc/GMT+12"
    midway_island = "Pacific/Midway"
    american_samoa = "Pacific/Pago_Pago"
    hawaii = "Pacific/Honolulu"
    alaska = "America/Juneau"
    pacific_time = "America/Los_Angeles"
    tijuana = "America/Tijuana"
    mountain_time = "America/Denver"
    arizona = "America/Phoenix"
    chihuahua = "America/Chihuahua"
    mazatlan = "America/Mazatlan"
    central_time = "America/Chicago"
    saskatchewan = "America/Regina"
    guadalajara = "America/Mexico_City"
    mexicoCity = "America/Mexico_City"
    monterrey = "America/Monterrey"
    central_america = "America/Guatemala"
    eastern_time = "America/New_York"
    indiana = "America/Indiana/Indianapolis"
    bogota = "America/Bogota"
    lima = "America/Lima"
    quito = "America/Lima"
    atlantic_time = "America/Halifax"
    caracas = "America/Caracas"
    lapaz = "America/La_Paz"
    santiago = "America/Santiago"
    newfoundland = "America/St_Johns"
    brasilia = "America/Sao_Paulo"
    buenos_aires = "America/Argentina/Buenos_Aires"
    montevideo = "America/Montevideo"
    georgetown = "America/Guyana"
    puerto_rico = "America/Puerto_Rico"
    greenland = "America/Godthab"
    mid_atlantic = "Atlantic/South_Georgia"
    azores = "Atlantic/Azores"
    cape_verde = "Atlantic/Cape_Verde"
    dublin = "Europe/Dublin"
    edinburgh = "Europe/London"
    lisbon = "Europe/Lisbon"
    london = "Europe/London"
    casablanca = "Africa/Casablanca"
    monrovia = "Africa/Monrovia"
    utc = "Etc/UTC"
    belgrade = "Europe/Belgrade"
    bratislava = "Europe/Bratislava"
    budapest = "Europe/Budapest"
    ljubljana = "Europe/Ljubljana"
    prague = "Europe/Prague"
    sarajevo = "Europe/Sarajevo"
    skopje = "Europe/Skopje"
    warsaw = "Europe/Warsaw"
    zagreb = "Europe/Zagreb"
    brussels = "Europe/Brussels"
    copenhagen = "Europe/Copenhagen"
    madrid = "Europe/Madrid"
    paris = "Europe/Paris"
    amsterdam = "Europe/Amsterdam"
    berlin = "Europe/Berlin"
    bern = "Europe/Zurich"
    zurich = "Europe/Zurich"
    rome = "Europe/Rome"
    stockholm = "Europe/Stockholm"
    vienna = "Europe/Vienna"
    westCentralAfrica = "Africa/Algiers"
    bucharest = "Europe/Bucharest"
    cairo = "Africa/Cairo"
    helsinki = "Europe/Helsinki"
    kyiv = "Europe/Kiev"
    riga = "Europe/Riga"
    sofia = "Europe/Sofia"
    tallinn = "Europe/Tallinn"
    vilnius = "Europe/Vilnius"
    athens = "Europe/Athens"
    istanbul = "Europe/Istanbul"
    minsk = "Europe/Minsk"
    jerusalem = "Asia/Jerusalem"
    harare = "Africa/Harare"
    pretoria = "Africa/Johannesburg"
    kaliningrad = "Europe/Kaliningrad"
    moscow = "Europe/Moscow"
    StPetersburg = "Europe/Moscow"
    volgograd = "Europe/Volgograd"
    samara = "Europe/Samara"
    kuwait = "Asia/Kuwait"
    riyadh = "Asia/Riyadh"
    nairobi = "Africa/Nairobi"
    baghdad = "Asia/Baghdad"
    tehran = "Asia/Tehran"
    abuDhabi = "Asia/Muscat"
    muscat = "Asia/Muscat"
    baku = "Asia/Baku"
    tbilisi = "Asia/Tbilisi"
    yerevan = "Asia/Yerevan"
    kabul = "Asia/Kabul"
    ekaterinburg = "Asia/Yekaterinburg"
    islamabad = "Asia/Karachi"
    karachi = "Asia/Karachi"
    tashkent = "Asia/Tashkent"
    chennai = "Asia/Kolkata"
    kolkata = "Asia/Kolkata"
    mumbai = "Asia/Kolkata"
    newDelhi = "Asia/Kolkata"
    kathmandu = "Asia/Kathmandu"
    astana = "Asia/Dhaka"
    dhaka = "Asia/Dhaka"
    sriJayawardenepura = "Asia/Colombo"
    almaty = "Asia/Almaty"
    novosibirsk = "Asia/Novosibirsk"
    rangoon = "Asia/Rangoon"
    bangkok = "Asia/Bangkok"
    hanoi = "Asia/Bangkok"
    jakarta = "Asia/Jakarta"
    krasnoyarsk = "Asia/Krasnoyarsk"
    beijing = "Asia/Shanghai"
    chongqing = "Asia/Chongqing"
    hongKong = "Asia/Hong_Kong"
    urumqi = "Asia/Urumqi"
    kualaLumpur = "Asia/Kuala_Lumpur"
    singapore = "Asia/Singapore"
    taipei = "Asia/Taipei"
    perth = "Australia/Perth"
    irkutsk = "Asia/Irkutsk"
    ulaanbaatar = "Asia/Ulaanbaatar"
    seoul = "Asia/Seoul"
    osaka = "Asia/Tokyo"
    sapporo = "Asia/Tokyo"
    tokyo = "Asia/Tokyo"
    yakutsk = "Asia/Yakutsk"
    darwin = "Australia/Darwin"
    adelaide = "Australia/Adelaide"
    canberra = "Australia/Melbourne"
    melbourne = "Australia/Melbourne"
    sydney = "Australia/Sydney"
    brisbane = "Australia/Brisbane"
    hobart = "Australia/Hobart"
    vladivostok = "Asia/Vladivostok"
    guam = "Pacific/Guam"
    portMoresby = "Pacific/Port_Moresby"
    magadan = "Asia/Magadan"
    srednekolymsk = "Asia/Srednekolymsk"
    solomon = "Pacific/Guadalcanal"
    newCaledonia = "Pacific/Noumea"
    fiji = "Pacific/Fiji"
    kamchatka = "Asia/Kamchatka"
    marshall = "Pacific/Majuro"
    auckland = "Pacific/Auckland"
    wellington = "Pacific/Auckland"
    nukualofa = "Pacific/Tongatapu"
    tokelau = "Pacific/Fakaofo"
    chatham = "Pacific/Chatham"
    samoa = "Pacific/Apia"
