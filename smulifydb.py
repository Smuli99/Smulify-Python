import psycopg2
import sys

conn = psycopg2.connect(host="localhost", database="tjta3501", user="samu", password="")

def find_account(uid):
    try:
        cur = conn.cursor()
        sql = "SELECT fname, sname FROM users WHERE user_id = %s LIMIT 1;"
        cur.execute(sql, (uid,))
        account_name = cur.fetchone()
        cur.close()

        if account_name == None:
            print("No user found.")
            return None
        else:
            print("Hello ", account_name[0], " ", account_name[1], "!", sep= "")
            return uid
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Etistään kappale käyttäjän antaman nimen mukaan
def find_song(song):
    try:
        cur = conn.cursor()
        sql = "SELECT song_id, song_name, likes, release_date FROM song WHERE song_name ILIKE %s LIMIT 10;"
        cur.execute(sql, ('%' + song + '%',))
        songs = cur.fetchall()
        cur.close()

        if len(songs) == 0:
            print()
            print("No songs found.")
            what_next()
        else:
            print()
            print("Found these songs:")
            for s in songs:
                print(s)
            return songs[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etsitään artisti käyttäjän antaman nimen mukaan
def find_artist(artist):
    try:
        cur = conn.cursor()
        sql = "SELECT artist_id, artist_name, monthly_listeners FROM artist WHERE artist_name ILIKE %s LIMIT 5;"
        cur.execute(sql, ('%' + artist + '%',))
        artists = cur.fetchall()
        cur.close()

        if len(artists) == 0:
            print()
            print("No artist found.")
            what_next()
        else:
            print()
            print("Found these artists:")
            for a in artists:
                print(a)
            return artist[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etstiään albumi käyttäjän antaman nimen mukaan
def find_album(album):
    try:
        cur = conn.cursor()
        sql = "SELECT album_id, album_name, release_date FROM album WHERE album_name ILIKE %s LIMIT 3;"
        cur.execute(sql, ('%' + album + '%',))
        albums = cur.fetchall()
        cur.close()

        if len(albums) == 0:
            print()
            print("No albums found.")
            what_next()
        else:
            print()
            print("Found these albums:")
            for a in albums:
                print(a)
            return albums[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etsitään annetun artistin kaikki kappaleet
def show_songs_from_artist(artist):
    try:
        cur = conn.cursor()
        sql = "SELECT s.song_name AS \"Song\", a.artist_name AS \"Artist\" FROM song s, artist a \
               WHERE a.artist_name ILIKE %s AND a.artist_id = s.artist_id;"
        cur.execute(sql, ('%' + artist + '%',))
        songs = cur.fetchall()
        cur.close()

        if len(songs) == 0:
            print()
            print("No songs found.")
            what_next()
        else:
            print()
            print("Found these songs:")
            for s in songs:
                print(s)
        return songs[0]
      
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  

# Etsitään artistin kaikki albumit
def show_albums_from_artist(artist):
    try:
        cur = conn.cursor()
        sql = "SELECT a.album_id AS \"ID\", a.album_name AS \"Album\" FROM album a, artist ar\
               WHERE ar.artist_name ILIKE %s AND ar.artist_id = a.artist_id;"
        cur.execute(sql, ('%' + artist + '%',))
        albums = cur.fetchall()
        cur.close()

        if len(albums) == 0:
            print()
            print("No albums found.")
            what_next()
        else:
            print()
            print("These albums found:")
            for a in albums:
                print(a)
            return albums[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etsitään kappaleen tehnyt artisti
def show_artist(song):
    try:
        cur = conn.cursor()
        sql = "SELECT a.artist_name AS \"Artist\", monthly_listeners AS \"Monthlty Listeners\"\
               FROM song s, artist a WHERE s.song_name ILIKE %s AND s.artist_id = a.artist_id;"
        cur.execute(sql, ('%' + song + '%',))
        artist = cur.fetchall()
        cur.close()

        if len(artist) == 0:
            print()
            print("No artist found.")
            what_next()
        else:
            print()
            print("These artist found:")
            for a in artist:
                print(a)
            return artist[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etsitään albumi mihin tietty kappale kuuluu
def show_album(song):
    try:
        cur = conn.cursor()
        sql = "SELECT a.album_id, a.album_name FROM album a, song s WHERE s.song_name ILIKE %s \
               AND s.album_id = a.album_id LIMIT 1;"
        cur.execute(sql, ('%' + song + '%',))
        album = cur.fetchall()
        cur.close()

        if len(album) == 0:
            print()
            print("No albums found.")
            what_next()
        else:
            print()
            print("Found this album:")
            print(album)
            return album[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etsitään soittolistat mihin jonkin tietty kappale kuuluu
def show_playlists(song):
    try:
        cur = conn.cursor()
        sql = "SELECT p.playlist_id, p.playlist_name FROM playlist p, song s, songsonplaylists sop\
               WHERE s.song_name ILIKE %s AND s.song_id = sop.song_id AND sop.playlist_id = p.playlist_id;"
        cur.execute(sql, ('%' + song + '%',))
        playlists = cur.fetchall()
        cur.close()

        if len(playlists) == 0:
            print()
            print("No playlists found.")
            what_next()
        else:
            print()
            print("Found these playlists:")
            for p in playlists:
                print(p)
        return playlists[0]
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etistään tietyn albumin kaikki kappaleet
def show_songs_from_album(album):
    try:
        cur = conn.cursor()
        sql = "SELECT a.album_name, s.song_name FROM album a, song s, artist ar \
               WHERE a.album_name ILIKE %s AND a.artist_id = ar.artist_id\
               AND ar.artist_id = s.artist_id AND s.album_id = a.album_id;"
        cur.execute(sql, ('%' + album + '%',))
        songs = cur.fetchall()
        cur.close()

        if len(songs) == 0:
            print()
            print("No songs found.")
            what_next()
        else:
            print()
            print("Found these songs:")
            for s in songs:
                print(s)
            return songs[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Etistään tietyn albumin tehnyt artisti
def show_artist_from_album(album):
    try:
        cur = conn.cursor()
        sql = "SELECT ar.artist_name, ar.country, ar.monthly_listeners FROM album a, artist ar\
               WHERE a.album_name ILIKE %s AND a.artist_id = ar.artist_id;"
        cur.execute(sql, ('%' + album + '%',))
        artists = cur.fetchall()
        cur.close()

        if len(artists) == 0:
            print()
            print("No artists found.")
            what_next()
        else:
            print()
            print("Found these artists:")
            for a in artists:
                print(a)
            return artists[0]
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def song_choises(song):
    mid = find_song(song)
    print("1) Show artist")
    print("2) Show album")
    print("3) Show playlists")
    print("4) Quit")
    choise = int(input("What do you want to do? "))
    if choise == 1:
        show_artist(song)
        show_main()
    elif choise == 2:         
        show_album(song)
        show_main()
    elif choise == 3:     
        show_playlists(song)
        show_main()
    elif choise == 4:
        exit()


def artist_choises(artist):
    mid = find_artist(artist)
    print("1) Show songs from artist")
    print("2) Show albums from artist")
    print("3) Quit")
    choise = int(input("What do you want to do? "))
    if choise == 1:
        show_songs_from_artist(artist)
        show_main()
    elif choise == 2:         
        show_albums_from_artist(artist)
        show_main()
    elif choise == 3:     
        exit()

def album_choises(album):
    mid = find_album(album)
    print("1) Show songs from album")
    print("2) Show artist")
    print("3) Quit")
    choise = int(input("What do you want to do? "))
    if choise == 1:
        show_songs_from_album(album)
        show_main()
    elif choise == 2:         
        show_artist_from_album(album)
        show_main()
    elif choise == 3:     
        exit()

# Etsitään viimeisin artisti ID
def find_latest_artistid():
    try:
        cur = conn.cursor()
        sql = ("SELECT artist_id FROM artist ORDER BY artist_id DESC LIMIT 1;")
        cur.execute(sql)
        id = cur.fetchone()
        cur.close()

        if len(id) == 0:
            print()
            print("Problems finding artist ID.")
            return None
        else:
            return id
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Etsitään viimeisin kappale ID
def find_latest_songid():
    try:
        cur = conn.cursor()
        sql = "SELECT song_id FROM song ORDER BY song_id DESC LIMIT 1;"
        cur.execute(sql)
        id = cur.fetchone()
        cur.close()

        if len(id) == 0:
            print("Problems finding song ID")
            return None
        else:
            return id
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Etsitään viimeisin albumi ID
def find_latest_albumid():
    try:
        cur = conn.cursor()
        sql = "SELECT album_id FROM album ORDER BY album_id DESC LIMIT 1;"
        cur.execute(sql)
        id = cur.fetchone()
        cur.close()

        if len(id) == 0:
            print("Problems finding album ID")
            return None
        else:
            return id
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Lisätään uusi artisti tietokantaan
def new_artist():
    # Kysytään tiedot
    try:
        latest_id         = find_latest_artistid()
        id                = input("Insert new ID. ID needs to be bigger than last one : " + str(latest_id) + ": ")
        name              = input("Artist name: ")
        country           = input("Country: ")
        followers         = int(input("Followers: "))
        monthly_listeners = int(input("Monthly listeners: "))

        cur = conn.cursor()
        sql = "INSERT INTO artist (artist_id, artist_name, country, followers, monthly_listeners)\
               VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (id, name, country, followers, monthly_listeners))
        conn.commit()
        
        sql = "SELECT * FROM artist ORDER BY artist_id DESC LIMIT 1;"
        cur.execute(sql)
        artist = cur.fetchone()
        cur.close()

        print("New artist added successfully!")
        print(artist)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Lisätään uusi kappale tietokantaan
def new_song():
    # Kysytään tiedot
    try:
        latest_id = find_latest_songid()
        id = input("Insert new ID. ID needs to be bigger than last one : " + str(latest_id) + ": ")
        title = input("Song title: ")
        duration = float(input("Song duration (like 3.20): "))
        release_date = input("Released on (in format: YYYY-MM-DD HH:MM:SS): ")
        likes = int(input("Likes: "))
        artist_id = input("Artist ID (like ar50 or null): ")
        album_id = input("Album ID (like al50 or null): ")

        cur = conn.cursor()
        sql = "INSERT INTO song (song_id, song_name, duration, release_date, likes, artist_id, album_id)\
               VALUES (%s, %s, %s, %s, %s, %s, %s);"
        cur.execute(sql, (id, title, duration, release_date, likes, artist_id, album_id))
        conn.commit()
        
        sql = "SELECT * FROM song ORDER BY song_id DESC LIMIT 1;"
        cur.execute(sql)
        song = cur.fetchone()
        cur.close()

        print("New artist added successfully!")
        print(song)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# Lisätään uusi albumi
def new_album():
    # Kysytään tiedot
    try:
        latest_id = find_latest_albumid()
        id = input("Insert new ID. ID needs to be bigger than last one : " + str(latest_id) + ": ")
        title = input("Album title: ")
        released_on = input("Released on (in format: YYYY-MM-DD HH:MM:SS): ")
        duration = float(input("Album duration (like 43.20): "))
        artist_id = input("Artist ID (like ar50 or null): ")

        cur = conn.cursor()
        sql = "INSERT INTO album (album_id, album_name, release_date, duration, artist_id)\
               VALUES (%s, %s, %s, %s, %s);"
        cur.execute(sql, (id, title, released_on, duration, artist_id))
        conn.commit()

        sql = "SELECT * FROM album ORDER BY album_id DESC LIMIT 1;"
        cur.execute(sql)
        album = cur.fetchone()
        cur.close()

        print("New album added successfully!")
        print(album)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



# Kysytään käyttäjältä mitä hän haluaa tehdä seuraavaksi
def what_next():
    print()
    print("1) Insert a new artist")
    print("2) Insert a new song")
    print("3) Insert a new album")
    print("4) I want to search")
    print("5) Quit")
    choise = int(input("What do you want to do? "))
    if choise == 1:
        new_artist()
        show_main()
    elif choise == 2:
        new_song() 
        show_main()
    elif choise == 3:
        new_album()
        show_main()  

def exit():
    if conn is not None: conn.close()
    sys.exit()

def show_main():
    print("1) Find a song")
    print("2) Find a artist")
    print("3) Find a album")
    print("4) Quit")
    choise = int(input("What do you want to do? "))
    if choise == 1:
        song = input("Type a search term: ")
        song_choises(song)
    elif choise == 2:
        artist = input("Type a search term: ")
        artist_choises(artist)
    elif choise == 3:
        album = input("Type a search term: ")
        album_choises(album)
    elif choise == 4:
        exit()

uid = (input("What is your user id? User id like u001. "))
uid = find_account(uid)
if uid: show_main()