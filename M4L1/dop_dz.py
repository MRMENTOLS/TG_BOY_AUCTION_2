import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('movie.db')  # Замените 'your_database.db' на имя вашей базы данных
cursor = conn.cursor()

# 1. Выбрать самый популярный фильм из списка
cursor.execute('''
    SELECT title, budget
    FROM movies
    ORDER BY popularity DESC
    LIMIT 1
''')
most_popular_movie = cursor.fetchone()
print(f"Самый популярный фильм: {most_popular_movie[0]}, Бюджет: {most_popular_movie[1]}")

# 2. Выбрать самый дорогой фильм, который вышел в декабре 2009 года
cursor.execute('''
    SELECT title
    FROM movies
    WHERE release_date BETWEEN '2009-12-01' AND '2009-12-31'
    ORDER BY budget DESC
    LIMIT 1
''')
most_expensive_december_movie = cursor.fetchone()
print(f"Самый дорогой фильм декабря 2009 года: {most_expensive_december_movie[0]}")

# 3. Выбрать фильм со слоганом "The battle within."
cursor.execute('''
    SELECT title
    FROM movies
    WHERE tagline = 'The battle within.'
''')
tagline_movie = cursor.fetchone()
print(f"Фильм со слоганом 'The battle within.': {tagline_movie[0]}")

# 4. Выбрать фильмы с датой выпуска до 1980 года и рейтингом больше 8
cursor.execute('''
    SELECT title, vote_average
    FROM movies
    WHERE release_date < '1980-01-01' AND vote_average > 8
    ORDER BY vote_average DESC
    LIMIT 1
''')
highest_voted_old_movie = cursor.fetchone()
print(f"Фильм с максимальным количеством голосов до 1980 года: {highest_voted_old_movie[0]}")

# Закрываем соединение с базой данных
conn.close()