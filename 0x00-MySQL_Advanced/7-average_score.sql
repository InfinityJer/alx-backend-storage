-- 7-average_score.sql
-- Task: Average score

-- Create a stored procedure ComputeAverageScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;

    -- Compute the total score and total number of projects for the user
    SELECT SUM(score), COUNT(DISTINCT project_id) INTO total_score, total_projects
    FROM corrections
    WHERE user_id = user_id;

    -- Update the average score for the user
    UPDATE users
    SET average_score = IF(total_projects > 0, total_score / total_projects, 0)
    WHERE id = user_id;
END;
//
DELIMITER ;
