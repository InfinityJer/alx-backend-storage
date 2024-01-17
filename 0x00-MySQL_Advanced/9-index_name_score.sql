-- 9-index_name_score.sql
-- Task: Optimize search and score

-- Create an index idx_name_first_score on the first letter of the name and score columns
CREATE INDEX idx_name_first_score ON names (LEFT(name, 1), score);
