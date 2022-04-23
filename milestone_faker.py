import mysql.connector
from faker import Faker
import random
import datetime

fake = Faker()


UNAME = "root"
PASSWORD = ""

con = mysql.connector.connect(
    host = "localhost",
    database = "",
    user = UNAME, 
    password = PASSWORD
)

if con.is_connected():
    cursor = con.cursor()
    cursor.execute("""DROP DATABASE IF EXISTS m2""");
    cursor.execute("""CREATE DATABASE m2""");
    cursor.execute("""USE m2""");
    cursor.execute("""DROP TABLE IF EXISTS orang;""")
    cursor.execute(
        """CREATE TABLE orang(
            idOrang VARCHAR(255) UNIQUE PRIMARY KEY,
            namaDepan VARCHAR(255),
            namaBelakang VARCHAR(255),
            tanggalLahir DATE,
            kewarganegaraan VARCHAR(255)
        );"""
    )
    
    # insert data orang
    id_orang_tersedia = []

    for i in range(2000):
        id_orang_tersedia.append(str("ORG" + str("{:03d}".format(i))))
        cursor.execute(""" INSERT INTO orang (idOrang, namaDepan, namaBelakang, tanggalLahir, kewarganegaraan)\
            VALUES ("{}", "{}", "{}", "{}", "{}"); """\
            .format(str("ORG" + str("{:03d}".format(i))), fake.first_name(), fake.last_name(), fake.date_between(\
                start_date = datetime.date(1970, 1, 1), end_date = datetime.date(1997, 12, 31)), fake.country()))
        
    
    cursor.execute("""DROP TABLE IF EXISTS wasit;""")
    cursor.execute(
        """CREATE TABLE wasit(
            idOrang VARCHAR(255) PRIMARY KEY,
            tipeWasit VARCHAR(255),
            FOREIGN KEY (idOrang) REFERENCES orang(idOrang)
        );"""
    )
    
    # id_pelatih_arr = []
    id_wasit_arr = []
    # add pelatih dan wasit berbarengan
        
    for i in range(100):
        id_wasit = fake.random_element(id_orang_tersedia)
        tipe_wasit = fake.random_element(["Hakim Utama", "Hakim Garis", "Wasit Cadangan"])
        id_wasit_arr.append([id_wasit, tipe_wasit])
        id_orang_tersedia.remove(id_wasit)
        cursor.execute(
            """ INSERT INTO wasit (idOrang, tipeWasit) \
                VALUES ("{}", "{}"); """\
                .format(id_wasit, tipe_wasit)
        )
        
    cursor.execute("""DROP TABLE IF EXISTS tim;""")
    cursor.execute(
        """CREATE TABLE tim(
            idTim VARCHAR(255) UNIQUE PRIMARY KEY,
            namaTim VARCHAR(255),
            negara VARCHAR(255),
            URLJerseyHome VARCHAR(255),
            URLJerseyAway VARCHAR(255),
            URLJerseyKetiga VARCHAR(255),
            idPelatih VARCHAR(255),
            goalDifference INT,
            FOREIGN KEY (idPelatih) REFERENCES orang(idOrang)
        );"""
    )
    
    id_tim_arr = []
    for i in range(32):
        id_pelatih =  fake.random_element(id_orang_tersedia)
        id_orang_tersedia.remove(id_pelatih)
        id_tim_arr.append(str("TIM" + str("{:03d}".format(i))))
        cursor.execute(
            """ INSERT INTO tim (idTim, namaTim, negara, URLJerseyHome, URLJerseyAway, URLJerseyKetiga, idPelatih, goalDifference)
            VALUES("{}", "{}", "{}", "{}", "{}", "{}", "{}", 0); """\
            .format((str("TIM" + str("{:03d}".format(i)))), fake.company(), fake.country(), fake.url(), fake.url(), fake.url(), id_pelatih)
        )
        
    cursor.execute("""DROP TABLE IF EXISTS pemain;""")
    cursor.execute(
        """CREATE TABLE pemain(
            idOrang VARCHAR(255) UNIQUE PRIMARY KEY,
            idTim VARCHAR(255),
            noPunggung INT,
            posisi VARCHAR(255),
            jumlahGoal INT,
            FOREIGN KEY (idOrang) REFERENCES orang(idOrang),
            FOREIGN KEY (idTim) REFERENCES tim(idTim)
        );"""
    )
    
    cursor.execute("""DROP TABLE IF EXISTS goalkeeper;""")
    cursor.execute(
        """CREATE TABLE goalkeeper(
            idOrang VARCHAR(255) PRIMARY KEY,
            jumlahSave INT,
            FOREIGN KEY (idOrang) REFERENCES pemain(idOrang)
        );"""
    )
    
    cursor.execute("""DROP TABLE IF EXISTS nonkeeper;""")
    cursor.execute(
        """CREATE TABLE nonkeeper(
            idOrang VARCHAR(255) PRIMARY KEY,
            tipe VARCHAR(255),
            FOREIGN KEY (idOrang) REFERENCES pemain(idOrang)
        );"""
    )
    
    pemain_dict = {}
    
    for i in range(32):
        pemain_arr = []
        for j in range(20):
            id_orang_pemain = fake.random_element(id_orang_tersedia)
            id_orang_tersedia.remove(id_orang_pemain)
            if (j != (20 - 1)):
                
                # tambahkan pemain yang BUKAN keeper
                cursor.execute(
                    """ INSERT INTO pemain (idOrang, idTim, noPunggung, posisi, jumlahGoal)
                    VALUES("{}", "{}", {}, "{}", {}); """\
                    .format(id_orang_pemain, id_tim_arr[i], random.randrange(2, 50, 1), "NONKEEPER", 0)
                )
                cursor.execute(
                    """ INSERT INTO nonkeeper (idOrang, tipe)
                    VALUES("{}", "{}"); """\
                    .format(id_orang_pemain, fake.random_element(["Striker", "Defense", "Mid"]))
                )
                
                # tambahkan pemain YANG KEEPER (no punggung 1)?
            else:
                cursor.execute(
                    """ INSERT INTO pemain (idOrang, idTim, noPunggung, posisi, jumlahGoal)
                    VALUES("{}", "{}", {}, "{}", {}); """\
                    .format(id_orang_pemain, id_tim_arr[i], 1, "KEEPER", 0)
                )
                
                cursor.execute(
                    """ INSERT INTO goalkeeper (idOrang, jumlahSave)
                    VALUES("{}", {}); """\
                    .format(id_orang_pemain, random.randrange(0, 100, 1))
                )
                
            pemain_arr.append(id_orang_pemain)
        pemain_dict[id_tim_arr[i]] = pemain_arr

                
    # insert grup dan babak, data sudah dihardcode
    cursor.execute("DROP TABLE IF EXISTS grup");
    cursor.execute(
        """CREATE TABLE grup(
            idGrup VARCHAR(255) UNIQUE PRIMARY KEY,
            namaGrup VARCHAR(255)
        );""")
    
    cursor.execute("""INSERT INTO grup VALUES
                ('A', 'Grup A'),
                ('B', 'Grup B'),
                ('C', 'Grup C'),
                ('D', 'Grup D'),
                ('E', 'Grup E'),
                ('F', 'Grup F'),
                ('G', 'Grup G'),
                ('H', 'Grup H');""")
    
    cursor.execute("""DROP TABLE IF EXISTS babak;""")
    
    cursor.execute(
        """CREATE TABLE babak(
            idBabak VARCHAR(255) UNIQUE PRIMARY KEY,
            namaBabak VARCHAR(255)
        );""")
    cursor.execute(
        """INSERT INTO babak VALUES
            ('B32', 'PerGrup'),
            ('B16', 'Per16'),
            ('B08', 'Per8'),
            ('B04', 'Semifinal'),
            ('B02', 'Final');
        """)
    
    cursor.execute("""DROP TABLE IF EXISTS tim_berada_di_grup;""")
    cursor.execute(
        """CREATE TABLE tim_berada_di_grup(
            idTim VARCHAR(255) PRIMARY KEY,
            idGrup VARCHAR(255),
            menangGrup INT,
            kalahGrup INT,
            seriGrup INT,
            FOREIGN KEY (idTim) REFERENCES tim(idTim),
            FOREIGN KEY (idGrup) REFERENCES grup(idGrup)
        );""")
    
    tim_dict = {
        "A": [],
        "B": [],
        "C": [],
        "D": [],
        "E": [],
        "F": [],
        "G": [],
        "H": []
    }
    
    for i in range(8):
        for j in range(4):
            cursor.execute("""INSERT INTO tim_berada_di_grup VALUES
                        ("{}", "{}", 0, 0, 0);"""\
                        .format(id_tim_arr[(i) * 4 + j], chr(i + 65)))
            tim_dict[chr(i + 65)] += [[id_tim_arr[(i) * 4 + j], 0]]

    # buat tabel pertandingan
    cursor.execute("""DROP TABLE IF EXISTS pertandingan""")
    cursor.execute("""CREATE TABLE pertandingan(
            idPertandingan VARCHAR(255) UNIQUE PRIMARY KEY,
            waktu DATETIME,
            idPihakHome VARCHAR(255),
            idPihakAway VARCHAR(255),
            golHome INT,
            golAway INT,
            idStadion VARCHAR(255),
            idBabak VARCHAR(255),
            FOREIGN KEY (idBabak) REFERENCES babak(idBabak)

        );""")
    
    cursor.execute("""DROP TABLE IF EXISTS pihak""")
    cursor.execute("""CREATE TABLE pihak(
        idPihak VARCHAR(255) UNIQUE PRIMARY KEY,
        idTim VARCHAR(255),
        idOrang1 VARCHAR(255),
        idOrang2 VARCHAR(255),
        idOrang3 VARCHAR(255),
        idOrang4 VARCHAR(255),
        idOrang5 VARCHAR(255),
        idOrang6 VARCHAR(255),
        idOrang7 VARCHAR(255),
        idOrang8 VARCHAR(255),
        idOrang9 VARCHAR(255),
        idOrang10 VARCHAR(255),
        idOrang11 VARCHAR(255),
        FOREIGN KEY (idTim) REFERENCES tim(idTim),
        FOREIGN KEY (idOrang1) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang2) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang3) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang4) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang5) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang6) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang7) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang8) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang9) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang10) REFERENCES pemain(idOrang),
        FOREIGN KEY (idOrang11) REFERENCES pemain(idOrang)
    )""")
    
    
    cursor.execute("""DROP TABLE IF EXISTS gol_home""")
    cursor.execute("""CREATE TABLE gol_home(
        idPertandingan VARCHAR(255),
        idOrang VARCHAR(255),
        FOREIGN KEY (idPertandingan) REFERENCES pertandingan(idPertandingan),
        FOREIGN KEY (idOrang) REFERENCES pemain(idOrang)
    );""")
    
    cursor.execute("""DROP TABLE IF EXISTS gol_away""")
    cursor.execute("""CREATE TABLE gol_away(
        idPertandingan VARCHAR(255),
        idOrang VARCHAR(255),
        FOREIGN KEY (idPertandingan) REFERENCES pertandingan(idPertandingan),
        FOREIGN KEY (idOrang) REFERENCES pemain(idOrang)
    );""")
    
    cursor.execute("""DROP TABLE IF EXISTS stadion""")
    cursor.execute("""CREATE TABLE stadion(
        idStadion VARCHAR(255) UNIQUE PRIMARY KEY,
        namaStadion VARCHAR(255),
        kapasitas INT,
        lokasi VARCHAR(255)
    );""")
    id_stadion = []
    
    for i in range(5):
        id_stadion.append(str("ST" + str("{:03d}".format(i + 1))))
        cursor.execute("""INSERT INTO STADION VALUES\
            ("{}", "{}", {}, "{}");"""\
            .format(str("ST" + str("{:03d}".format(i + 1))), fake.company(), 1009 * random.randrange(1, 100, 5), fake.city()))

    cursor.execute(
        """CREATE FUNCTION calculate_goal_difference(homegoal INT, awaygoal INT, pihak VARCHAR(4))
        RETURNS INT
        
        BEGIN
        
            DECLARE goal INT;
                SET goal = 0;
                
                IF pihak = 'HOME' then
                    SET goal = homegoal - awaygoal;
                ELSE
                    SET goal = awaygoal - homegoal;
            END IF;
            
            RETURN goal;
        END;"""
    )# Time(Waktu) < DATE_ADD(NEW.Waktu, INTERVAL 3 HOUR)
    # trigger di sini
    cursor.execute(
        """CREATE TRIGGER before_pertandingan_insert
            BEFORE INSERT ON pertandingan
            FOR EACH ROW
            BEGIN
                IF (EXISTS(SELECT * FROM pertandingan WHERE ABS(TIMESTAMPDIFF(HOUR, waktu, NEW.waktu))< 3 AND idStadion = NEW.idStadion))
                THEN 
                    SIGNAL sqlstate '45001' SET message_text = 'Tidak bisa memasukkan pertandingan yang berlangsung di waktu yang sama di stadion yang sama';
                ELSEIF ((SELECT idTim FROM pihak WHERE idpihak = NEW.idPihakHome) = (SELECT idTim FROM pihak WHERE idPihak = NEW.idPihakAway))
                THEN 
                    SIGNAL sqlstate '45002' SET message_text = 'Pihak home dan pihak away mempunyai tim yang sama.';
                END IF;
            END;"""
    )
    cursor.execute(
        """CREATE TRIGGER after_pertandingan_insert
            AFTER INSERT ON pertandingan 
            FOR EACH ROW
            UPDATE tim 
                SET goalDifference = CASE
                WHEN idTim IN (SELECT idTim FROM pihak WHERE idPihak = NEW.idPihakHome) THEN goalDifference + calculate_goal_difference(NEW.golHome, NEW.golAway, 'HOME')
                WHEN idTim IN (SELECT idTim FROM pihak WHERE idPihak = NEW.idPihakAway) THEN goalDifference + calculate_goal_difference(NEW.golHome, NEW.golAway, 'AWAY')
                ELSE goalDifference
                END
            WHERE goalDifference is not null;
        """
        )

    # sisa 16 tim jadi 8 pertandingan 16 besar
    # 8 besar ada 4 pertandingan
    # semifinal 2 pertandingan 4 tim
    # final 1 pertandingan 2 tim
    # juara 3 ad 2 tim 1 pertandingan
    
    # masukkan pertandingan babak per grup, 8 grup x 2 pertandingan
    pertandingan_count = 0
    dtime_arr =[]
    for i in range(8):
        curr_group = chr(i + 65)
        grp_arr = tim_dict[curr_group]
        for j in range(0, 4):
            tim_home = grp_arr[j]
            for k in range(j + 1, 4):
                pertandingan_count += 1
                home_score = random.randrange(1, 10, 1)
                away_score = random.randrange(1, 10, 1)

                tim_away = grp_arr[k]
                
                pemain_home = []
                pemain_away = []
                
                for i in range(10):
                    appended_home = pemain_dict[tim_home[0]][random.randrange(0, len(pemain_dict[tim_home[0]]) - 1, 1)]
                    appended_away = pemain_dict[tim_away[0]][random.randrange(0, len(pemain_dict[tim_away[0]]) - 1, 1)]
                    pemain_home.append(appended_home)
                    pemain_away.append(appended_away)
                    pemain_dict[tim_home[0]].remove(appended_home)
                    pemain_dict[tim_away[0]].remove(appended_away)
                pemain_home.append(pemain_dict[tim_home[0]][-1])
                pemain_away.append(pemain_dict[tim_away[0]][-1])
                
                for i in range(11):
                    pemain_dict[tim_home[0]].append(pemain_home[i])
                    pemain_dict[tim_away[0]].append(pemain_away[i])
                
                cursor.execute("""INSERT INTO pihak VALUES\
                    ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");"""\
                    .format("PHK-H" + str("{:03d}".format(pertandingan_count)),
                            tim_home[0],
                            pemain_home[0],
                            pemain_home[1],
                            pemain_home[2],
                            pemain_home[3],
                            pemain_home[4],
                            pemain_home[5],
                            pemain_home[6],
                            pemain_home[7],
                            pemain_home[8],
                            pemain_home[9],
                            pemain_home[10]
                            ))
                
                cursor.execute("""INSERT INTO pihak VALUES\
                    ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");"""\
                    .format("PHK-A" + "{:03d}".format(pertandingan_count),
                            tim_away[0],
                            pemain_away[0],
                            pemain_away[1],
                            pemain_away[2],
                            pemain_away[3],
                            pemain_away[4],
                            pemain_away[5],
                            pemain_away[6],
                            pemain_away[7],
                            pemain_away[8],
                            pemain_away[9],
                            pemain_away[10]
                    ))
                dtime = fake.date_time_between_dates(datetime_start = datetime.datetime(2022, 2, 1), \
                    datetime_end = datetime.datetime(2022, 2, 28)) 
                if (dtime.date() in [x.date() for x in dtime_arr]):
                    date_arr = [x for x in dtime_arr if x.date() == dtime.date()]
                    date_arr.sort(reverse = True)
                    dtime += datetime.timedelta(hours = date_arr[0].hour + 5)
                dtime_arr.append(dtime)
                print(dtime)
                
                cursor.execute("""INSERT INTO pertandingan VALUES\
                    ("{}", "{}", "{}", "{}", {}, {}, "{}", "B32");"""\
                    .format(str("PT" + str("{:03d}".format(pertandingan_count))), \
                            dtime, \
                            "PHK-H" + "{:03d}".format(pertandingan_count), \
                            "PHK-A" + "{:03d}".format(pertandingan_count), \
                            home_score, away_score, fake.random_element(id_stadion)))

                for i in range(home_score):
                    curr_pemain = fake.random_element(pemain_home)
                    cursor.execute("""INSERT INTO gol_home VALUES ("{}", "{}");"""\
                        .format("PT" + "{:03d}".format(pertandingan_count), 
                                curr_pemain))
                    cursor.execute("""UPDATE pemain SET jumlahGoal = jumlahGoal + 1 WHERE idOrang = "{}";"""\
                        .format(curr_pemain))
                    
                for i in range(away_score):
                    curr_pemain = fake.random_element(pemain_away)
                    cursor.execute("""INSERT INTO gol_away VALUES ("{}", "{}");"""\
                    .format("PT" + "{:03d}".format(pertandingan_count), 
                            curr_pemain))
                    cursor.execute("""UPDATE pemain SET jumlahGoal = jumlahGoal + 1 WHERE idOrang = "{}";"""\
                        .format(curr_pemain))
                
                
                if (home_score > away_score):
                    cursor.execute("""UPDATE tim_berada_di_grup SET menangGrup = menangGrup + 1 WHERE idTim = "{}";"""\
                        .format(tim_home[0]))
                    cursor.execute("""UPDATE tim_berada_di_grup SET kalahGrup = kalahGrup + 1 WHERE idTim = "{}";"""\
                        .format(tim_away[0]))
                    tim_home[1] += 3
                    
                    
                elif (home_score < away_score):
                    cursor.execute("""UPDATE tim_berada_di_grup SET menangGrup = menangGrup + 1 WHERE idTim = "{}";"""\
                        .format(tim_away[0]))
                    cursor.execute("""UPDATE tim_berada_di_grup SET kalahGrup = kalahGrup + 1 WHERE idTim = "{}";"""\
                        .format(tim_home[0]))
                    tim_away[1] += 3
                # TODO: kalo seri gimana?
                # apa bomat terus lanjutin
                else:
                    cursor.execute("""UPDATE tim_berada_di_grup SET seriGrup = seriGrup + 1 WHERE idTim = "{}";"""\
                        .format(tim_away[0]))
                    cursor.execute("""UPDATE tim_berada_di_grup SET seriGrup = seriGrup + 1 WHERE idTim = "{}";"""\
                        .format(tim_home[0]))
                    tim_home[1] += 1
                    tim_away[1] += 1
    
    for value in tim_dict.values():
        value = value.sort(key = lambda x: x[1], reverse = True)

    postgrup_arr = []
    for keys in tim_dict:
        tim_dict[keys] = tim_dict[keys][0:2]
        postgrup_arr += tim_dict[keys]
    random.shuffle(postgrup_arr)
    #per16

    num = 8
    start_date = 1
    while (True):
        dtime_arr = []
        start_date += 1
        for i in range(0, num):
            pertandingan_count += 1

            home_score = random.randrange(1, 10, 1)
            away_score = random.randrange(1, 10, 1)
            tim_home = postgrup_arr[i]
            tim_away = postgrup_arr[i + 1]
            

            
            pemain_home = []
            pemain_away = []
            
            for i in range(10):
                appended_home = pemain_dict[tim_home[0]][random.randrange(0, len(pemain_dict[tim_home[0]]) - 1, 1)]
                appended_away = pemain_dict[tim_away[0]][random.randrange(0, len(pemain_dict[tim_away[0]]) - 1, 1)]
                pemain_home.append(appended_home)
                pemain_away.append(appended_away)
                pemain_dict[tim_home[0]].remove(appended_home)
                pemain_dict[tim_away[0]].remove(appended_away)
            pemain_home.append(pemain_dict[tim_home[0]][-1])
            pemain_away.append(pemain_dict[tim_away[0]][-1])
            
            for i in range(11):
                pemain_dict[tim_home[0]].append(pemain_home[i])
                pemain_dict[tim_away[0]].append(pemain_away[i])
                

            
            cursor.execute("""INSERT INTO pihak VALUES\
                ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");"""\
                .format("PHK-H" + str("{:03d}".format(pertandingan_count)),
                        tim_home[0],
                        pemain_home[0],
                        pemain_home[1],
                        pemain_home[2],
                        pemain_home[3],
                        pemain_home[4],
                        pemain_home[5],
                        pemain_home[6],
                        pemain_home[7],
                        pemain_home[8],
                        pemain_home[9],
                        pemain_home[10]
                        ))
            
            cursor.execute("""INSERT INTO pihak VALUES\
                ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}");"""\
                .format("PHK-A" + "{:03d}".format(pertandingan_count),
                        tim_away[0],
                        pemain_away[0],
                        pemain_away[1],
                        pemain_away[2],
                        pemain_away[3],
                        pemain_away[4],
                        pemain_away[5],
                        pemain_away[6],
                        pemain_away[7],
                        pemain_away[8],
                        pemain_away[9],
                        pemain_away[10]
                ))

            dtime =  fake.date_time_between_dates(datetime_start = datetime.datetime(2022, 3, start_date), \
                datetime_end = datetime.datetime(2022, 3, start_date + num))
            
            if (dtime.date() in [x.date() for x in dtime_arr]):
                    date_arr = [x for x in dtime_arr if x.date() == dtime.date()]
                    date_arr.sort(reverse = True)
                    dtime += datetime.timedelta(hours = date_arr[0].hour + 3)
            dtime_arr.append(dtime)
            print(dtime)
            
            cursor.execute("""INSERT INTO pertandingan VALUES\
                ("{}", "{}", "{}", "{}", {}, {}, "{}", "B{}");"""\
                .format(str("PT" + str("{:03d}".format(pertandingan_count))), \
                    dtime,
                    "PHK-H" + "{:03d}".format(pertandingan_count), \
                    "PHK-A" + "{:03d}".format(pertandingan_count), \
                    home_score, away_score,\
                    fake.random_element(id_stadion), str("{:02d}".format(num * 2))))
            
            for i in range(home_score):
                curr_pemain = fake.random_element(pemain_home)
                cursor.execute("""INSERT INTO gol_home VALUES ("{}", "{}");"""\
                    .format("PT" + "{:03d}".format(pertandingan_count), 
                            curr_pemain))
                cursor.execute("""UPDATE pemain SET jumlahGoal = jumlahGoal + 1 WHERE idOrang = "{}";"""\
                    .format(curr_pemain))
                
            for i in range(away_score):
                curr_pemain = fake.random_element(pemain_away)
                cursor.execute("""INSERT INTO gol_away VALUES ("{}", "{}");"""\
                .format("PT" + "{:03d}".format(pertandingan_count), 
                        curr_pemain))
                cursor.execute("""UPDATE pemain SET jumlahGoal = jumlahGoal + 1 WHERE idOrang = "{}";"""\
                    .format(curr_pemain))
                
            if (home_score > away_score):
                postgrup_arr.remove(tim_away)
                
                
            elif (home_score < away_score):
                postgrup_arr.remove(tim_home)

            else:
                kalah_gacha = random.choice([tim_away, tim_home])
                if (kalah_gacha == tim_away):
                    menang_gacha = tim_home
                    cursor.execute("""UPDATE pertandingan SET golHome = golHome + 1
                            WHERE idPertandingan = "{}";"""\
                            .format("PT" + "{:03d}".format(pertandingan_count)))
                else:
                    menang_gacha = tim_away
                    cursor.execute("""UPDATE pertandingan SET golAway = golAway + 1
                            WHERE idPertandingan = "{}";"""\
                            .format("PT" + "{:03d}".format(pertandingan_count)))
                    
                postgrup_arr.remove(kalah_gacha)
                    
                
        if (num == 1):
            break
        else:
            start_date += num
            num //= 2

    # stadion

    
    # wasit 
    cursor.execute("""DROP TABLE IF EXISTS diWasitiOleh""")
    cursor.execute("""CREATE TABLE diwasitiOleh(
        idPertandingan VARCHAR(255) PRIMARY KEY,
        idHakimUtama VARCHAR(255),
        idHakimGaris1 VARCHAR(255),
        idHakimGaris2 VARCHAR(255),
        idCadangan VARCHAR(255),
        FOREIGN KEY (idPertandingan) REFERENCES pertandingan(idPertandingan),
        FOREIGN KEY (idHakimUtama) REFERENCES wasit(idOrang),
        FOREIGN KEY (idHakimGaris1) REFERENCES wasit(idOrang),
        FOREIGN KEY (idHakimGaris2) REFERENCES wasit(idOrang),
        FOREIGN KEY (idCadangan) REFERENCES wasit(idOrang)
    );""")
    
    hakim_utama_arr = [elmt[0] for elmt in id_wasit_arr if elmt[1] == "Hakim Utama"]
    hakim_garis_arr = [elmt[0] for elmt in id_wasit_arr if elmt[1] == "Hakim Garis"]
    cadangan_arr = [elmt[0] for elmt in id_wasit_arr if elmt[1] == "Wasit Cadangan"]
    for i in range(pertandingan_count - 1):
        cursor.execute("""INSERT INTO diWasitiOleh VALUES
            ("{}", "{}", "{}", "{}", "{}");"""\
            .format(str("PT" + str("{:03d}".format(i + 1))), fake.random_element(hakim_utama_arr),
            fake.random_element(hakim_garis_arr), fake.random_element(hakim_garis_arr),
            fake.random_element(cadangan_arr)))

    # buat partisipan dan "dihadiri oleh"
    cursor.execute("""DROP TABLE IF EXISTS tiketPartisipan""")
    cursor.execute("""CREATE TABLE tiketPartisipan(
        idTiket VARCHAR(255) PRIMARY KEY,
        idOrang VARCHAR(255),
        FOREIGN KEY (idOrang) REFERENCES orang(idOrang)
    );""")
    cursor.execute("""DROP TABLE IF EXISTS dihadiriOleh""")
    cursor.execute("""CREATE TABLE dihadiriOleh(
        idPertandingan VARCHAR(255),
        idPenonton VARCHAR(255),
        FOREIGN KEY (idPertandingan) REFERENCES pertandingan(idPertandingan)
        );""")
    
    for i in range(len(id_orang_tersedia)):
        for j in range(random.randrange(1, 6, 1)):   
            cursor.execute("""INSERT INTO dihadiriOleh VALUES\
                ("{}", "{}");"""\
                .format(str("PT" + "{:03d}".format(random.randrange(1, pertandingan_count, 1))),\
               id_orang_tersedia[i]))   
            cursor.execute("""INSERT INTO tiketPartisipan VALUES\
                ("{}", "{}");"""\
                .format(fake.pystr(), id_orang_tersedia[i]))

    # buat view
    cursor.execute("""CREATE VIEW mvptim AS(
        select 
            idorang, 
            concat(namadepan, " ", namabelakang) as namalengkap, 
            max(jumlahGoal) as JumlahGoal, 
            negara as negaraTim,
            idtim
        from pemain 
        natural join orang 
        natural join tim 
        group by idTim order by idTim
    );""")

        
    con.commit()