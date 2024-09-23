WITH teacher_graded_counts AS (
    SELECT 
        teacher_id,
        COUNT(*) as graded_count,
        SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END) as grade_A_count
    FROM 
        assignments
    WHERE 
        state = 'GRADED'
    GROUP BY 
        teacher_id
)
SELECT 
    grade_A_count
FROM 
    teacher_graded_counts
WHERE 
    graded_count = (SELECT MAX(graded_count) FROM teacher_graded_counts)
ORDER BY 
    teacher_id
LIMIT 1;