select
    hour(created_at)            as hour_utc,
    count(*)                    as n_stories,
    round(avg(points), 1)       as avg_points,
    round(avg(num_comments), 1) as avg_comments
from {{ ref('stories_clean') }}
group by 1
order by 1