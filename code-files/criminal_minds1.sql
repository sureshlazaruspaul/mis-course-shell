WITH temp_data AS
    (
        SELECT
            * ,
            -- creating a variable 'possible_suspects' 
            CASE
                WHEN  (
                    -- either failed the bar or fired from job
                    (bar_exam_status = 'Fail' OR fired_from_job = 'YES') AND
                    -- initials is JCB
                    full_name GLOB 'J* C* B*' 
            ) THEN 1 ELSE 0
            END AS possible_suspects
        FROM 
            ----------------------------------------------------------
            -- MERGING STRATEGY
            ----------------------------------------------------------
        
            -- merge person_details table with law_details tab;e
            person_details A
                LEFT JOIN law_details B
                    USING (sno) -- using common identifier variable sno
    )
    SELECT
        *
    FROM 
        temp_data
    WHERE
        ----------------------------------------------------------
        -- QUERYING STRATEGY
        ----------------------------------------------------------
        
        -- 1) full name eaxct search
        full_name = 'James Colby Baylor' OR 
            
        -- 2) and if that does not yield results, search for ...
        possible_suspects = 1
;