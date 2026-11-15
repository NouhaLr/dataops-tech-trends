-- Quality rules. The first rule that matches wins.
select
    *,
    case
        when title is null                                      then 'missing_title'
        when points is null or points < 0                       then 'invalid_points'
        when num_comments < 0                                   then 'invalid_comments'
        when created_at is null
          or created_at > timezone('UTC', current_timestamp) + interval 1 hour
                                                                then 'invalid_date'
    end as reject_reason
from {{ ref('stg_hn_stories') }}