-- 3-glam_rock.sql
-- Task: Old school band

-- List bands with Glam rock as their main style, ranked by longevity
SELECT band_name,
       IF(splitted[2] = 0, 0, 2022 - CAST(splitted[2] AS SIGNED) + 1) as lifespan
FROM (
    SELECT band_name,
           SPLIT_STR(SPLIT_STR(formed, '-', 1), ' ', 3) as splitted
    FROM metal_bands
    WHERE FIND_IN_SET('Glam rock', style) > 0
) as subquery
ORDER BY lifespan DESC, band_name;

