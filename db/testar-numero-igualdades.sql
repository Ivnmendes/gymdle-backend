SELECT
    "targetMuscles",
    "bodyParts",
    "equipments",
    "secondaryMuscles",
    COUNT(*) AS total_ocorrencias
FROM
    exercises_exercises
GROUP BY
    "targetMuscles",
    "bodyParts",
    "equipments",
    "secondaryMuscles"
HAVING
    COUNT(*) > 1
ORDER BY
    total_ocorrencias DESC;