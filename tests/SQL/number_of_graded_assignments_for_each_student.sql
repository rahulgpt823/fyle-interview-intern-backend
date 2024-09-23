-- Write query to get number of graded assignments for each student:

SELECT 
    a.student_id,
    COUNT(*) as graded_assignments_count
FROM 
    assignments a
WHERE 
    a.state = 'GRADED'
GROUP BY 
    a.student_id
ORDER BY 
    a.student_id;