-- 8-index_my_names.sql
-- Task: Optimize simple search

-- Create an index idx_name_first on the first letter of the name column
CREATE INDEX idx_name_first ON names(name(1));
