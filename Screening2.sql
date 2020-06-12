SELECT c.name,revenue,count(location_id) AS NumOfOffices
FROM companies c
LEFT JOIN offices o ON o.company_id = c.company_id
GROUP BY c.company_id
HAVING NumOfOffices < 5
ORDER BY NumOfOffices;
