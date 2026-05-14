SELECT
    first_name ,
    middle_name ,
    last_name ,
    age ,
    city ,
    state
FROM 
    ----------------------------------------------------------
    -- MERGING STRATEGY
    ----------------------------------------------------------

    -- merge person_details table with law_details
    person_details A
        LEFT JOIN law_details B
            USING (sno) -- using common identifier variable sno

WHERE
    ----------------------------------------------------------
    -- QUERYING STRATEGY
    ----------------------------------------------------------
    
    -- 1) full name search
    full_name = 'James Colby Baylor' OR 
        
    -- and if that does not yield results, search for ...
        (
            -- 1) either failed the bar or fired from job
            (bar_exam_status = 'Fail' OR fired_from_job = 'YES') AND
        
            -- 2) initials is JCB
        
            -- a) using GLOB function
            full_name GLOB 'J* C* B*' 
        
            -- b) using LIKE function
            -- full_name LIKE 'J% C% B%' 
        
            -- c) using substring search
            /*
            (
                SUBSTR(first_name, 1, 1) = 'J' AND 
                SUBSTR(middle_name, 1, 1) = 'C' AND
                SUBSTR(last_name, 1, 1) = 'B' 
            )
            */
        )
;