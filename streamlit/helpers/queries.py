raw_data_query = """
    SELECT *
    FROM kafka_311_request
    ORDER BY updated_datetime DESC
    LIMIT 50;
    """

main_query = """
    SELECT date(tb1.requested_datetime) AS date, 
    tb1.police_district,
    tb1.service_type,
    tb2.latitude,
    tb2.longitude,
    count(*)
    FROM historical_311_request tb1
    LEFT JOIN sf_police_district tb2
    ON tb1.police_district = tb2.police_district
    WHERE tb1.police_district IS NOT NULL and tb1.service_type IS NOT NULL
    GROUP BY 1, 2, 3, 4, 5
    ORDER BY 1, 2, 3, 4, 5;
    """