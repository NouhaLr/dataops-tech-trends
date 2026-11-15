select * exclude (reject_reason)
from {{ ref('int_hn_stories_checked') }}
where reject_reason is null