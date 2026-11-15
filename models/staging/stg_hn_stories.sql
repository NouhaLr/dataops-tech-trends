-- Staging: repair what can be repaired. No row is removed here.
select
    story_id,
    nullif(trim(title), '')   as title,
    url,
    author,
    points,
    num_comments,
    created_at,
    _loaded_at
from {{ source('raw', 'hn_stories') }}