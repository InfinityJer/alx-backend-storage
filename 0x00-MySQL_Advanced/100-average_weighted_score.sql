-- 100-average_weighted_score.sql
-- Task: Average Weighted Score

-- Create the stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN p_user_id INT)
BEGIN
    DECLARE total_score FLOAT DEFAULT 0;
    DECLARE total_weight INT DEFAULT 0;

    -- Calculate the weighted sum and total weight for the user
    SELECT SUM(c.score * p.weight), SUM(p.weight)
    INTO total_score, total_weight
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = p_user_id;

    -- Update the average_score for the user
    UPDATE users
    SET average_score = CASE
                            WHEN total_weight > 0 THEN total_score / total_weight
                            ELSE 0
                        END
    WHERE id = p_user_id;
END //

DELIMITER ;
