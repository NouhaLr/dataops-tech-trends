select *
from {{ ref('int_hn_stories_checked') }}
where reject_reason is not null