-- A data test passes when it returns no rows.
select story_id, points
from {{ ref('stories_clean') }}
where points < 0