# Expansions & Fields use for extend object data.
TWEET_EXPANSION = "attachments.poll_ids,attachments.media_keys,author_id,geo.place_id,in_reply_to_user_id,referenced_tweets.id,entities.mentions.username,referenced_tweets.id.author_id"
SPACE_EXPANSION = "invited_user_ids,speaker_ids,creator_id,host_ids,topic_ids"
LIST_EXPANSION = "owner_id"
PINNED_TWEET_EXPANSION = "pinned_tweet_id"

TWEET_FIELD = "attachments,author_id,context_annotations,conversation_id,created_at,geo,entities,in_reply_to_user_id,lang,possibly_sensitive,public_metrics,referenced_tweets,reply_settings,source,text,withheld"
USER_FIELD = "created_at,description,entities,id,location,name,profile_image_url,protected,public_metrics,url,username,verified,withheld,pinned_tweet_id"
SPACE_FIELD = "host_ids,created_at,creator_id,id,lang,invited_user_ids,participant_count,speaker_ids,started_at,state,title,updated_at,scheduled_start,is_ticketed"
COMPLETE_SPACE_FIELD = SPACE_FIELD + ",subscriber_count"
MEDIA_FIELD = "duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
PLACE_FIELD = "contained_within,country,country_code,full_name,geo,id,name,place_type"
POLL_FIELD = "duration_minutes,end_datetime,id,options,voting_status"
TOPIC_FIELD = "id,name,description"
LIST_FIELD = "created_at,follower_count,member_count,private,description,owner_id"

# Indicator for the return_when argument in wait_for_futures method.
FIRST_COMPLETED = "FIRST_COMPLETED"
FIRST_EXCEPTION = "FIRST_EXCEPTION"
ALL_COMPLETED = "ALL_COMPLETED"

# Language codes for subtitle that based on BCP47 style.
LANGUAGES_CODES = {
    "ar-SA": "Arabic",
    "bn-BD": "Bangla",
    "bn-IN": "Bangla",
    "cs-CZ": "Czech",
    "da-DK": "Danish",
    "de-AT": "German",
    "de-CH": "German",
    "de-DE": "German",
    "el-GR": "Greek",
    "en-AU": "English",
    "en-CA": "English",
    "en-GB": "English",
    "en-IE": "English",
    "en-IN": "English",
    "en-NZ": "English",
    "en-US": "English",
    "en-ZA": "English",
    "es-AR": "Spanish",
    "es-CL": "Spanish",
    "es-CO": "Spanish",
    "es-ES": "Spanish",
    "es-MX": "Spanish",
    "es-US": "Spanish",
    "fi-FI": "Finnish",
    "fr-BE": "French",
    "fr-CA": "French",
    "fr-CH": "French",
    "fr-FR": "French",
    "he-IL": "Hebrew",
    "hi-IN": "Hindi",
    "hu-HU": "Hungarian",
    "id-ID": "Indonesian",
    "it-CH": "Italian",
    "it-IT": "Italian",
    "jp-JP": "Japanese",
    "ko-KR": "Korean",
    "nl-BE": "Dutch",
    "nl-NL": "Dutch",
    "no-NO": "Norwegian",
    "pl-PL": "Polish",
    "pt-BR": "Portugese",
    "pt-PT": "Portugese",
    "ro-RO": "Romanian",
    "ru-RU": "Russian",
    "sk-SK": "Slovak",
    "sv-SE": "Swedish",
    "ta-IN": "Tamil",
    "ta-LK": "Tamil",
    "th-TH": "Thai",
    "tr-TR": "Turkish",
    "zh-CN": "Chinese",
    "zh-HK": "Chinese",
    "zh-TW": "Chinese",
}
