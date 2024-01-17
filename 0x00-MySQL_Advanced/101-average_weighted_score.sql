-- 101-average_weighted_score.sql
-- Task: Average Weighted Score for All

-- Create the stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_var INT;
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open the cursor
    OPEN cur;

    -- Loop through each user
    user_loop: LOOP
        -- Fetch the next user ID
        FETCH cur INTO user_id_var;

        -- Exit the loop if no more users
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Call the procedure to compute the average weighted score for the current user
        CALL ComputeAverageWeightedScoreForUser(user_id_var);
    END LOOP;

    -- Close the cursor
    CLOSE cur;
END //

DELIMITER ;
