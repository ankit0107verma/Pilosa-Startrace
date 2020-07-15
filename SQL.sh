###1
SELECT language_repository FROM stargazer
WHERE user_id=14;

###2
SELECT COUNT(user_id), language_repository FROM stargazer
GROUP BY language_repository
ORDER BY COUNT(user_id) DESC
LIMIT 5;

##3
SELECT language_repository FROM stargazer
WHERE user_id=14 OR user_id=19;

##4
SELECT language_repository FROM stargazer
WHERE (user_id=14 OR user_id=19) AND language_repository=1;