#!/usr/bin/python3

# Libs postgres
from wsgiref.handlers import CGIHandler
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for
import copy

app = Flask(__name__)

# SGBD configs
DB_HOST = "db.tecnico.ulisboa.pt"
DB_USER = "ist192470"
DB_DATABASE = DB_USER
DB_PASSWORD = "ph#YH9x"
DB_CONNECTION_STRING = "host={} dbname={} user={} password={}".format(
    DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)


@app.route("/")
def my_form():
    return render_template('main.html')


@app.route("/inst_menu", methods=['GET', 'POST'])
def institution_menu():
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        if request.method == "POST":
            if request.form['button'] == "insert":
                name = request.form['name']
                kind = request.form['kind']
                region_num = request.form['region_num']
                county_num = request.form['county_num']
                query = "INSERT INTO Institution VALUES(%s, %s, %s, %s);"

                cursor.execute(query, (name, kind, region_num, county_num))
            elif request.form['button'] == "edit":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Institution;"
                    cursor.execute(query)
                    return render_template('institution_menu.html', cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "UPDATE Institution SET "
                query_len = len(query)

                data = []

                if request.form["name"] != "":
                    query += "inst_name=%s,"
                    data += [request.form['name']]

                if request.form["kind"] != "":
                    query += "inst_kind=%s,"
                    data += [request.form['kind']]

                if request.form["region_num"] != "":
                    query += "region_num=%s,"
                    data += [request.form['region_num']]

                if request.form["county_num"] != "":
                    query += "county_num=%s,"
                    data += [request.form['county_num']]

                if len(query) == query_len:
                    query = "SELECT * FROM Institution;"
                    cursor.execute(query)
                    return render_template('institution_menu.html',
                                           cursor=cursor)

                query = query[:-1]

                query += " WHERE inst_name=%s and inst_kind=%s and region_num=%s and county_num=%s;"

                data += [to_update[0], to_update[1],
                         to_update[2], to_update[3]]

                cursor.execute(
                    query, tuple(data))
            elif request.form['button'] == "remove":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Institution;"
                    cursor.execute(query)
                    return render_template('institution_menu.html', cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "DELETE FROM Institution WHERE inst_name = %s and inst_kind=%s and region_num=%s and county_num=%s;"

                cursor.execute(query, (to_update[0], to_update[1],
                                       to_update[2], to_update[3]))

            query = "SELECT * FROM Institution;"
            cursor.execute(query)
            return render_template('institution_menu.html', cursor=cursor)

        elif request.method == "GET":
            query = "SELECT * FROM Institution;"
            cursor.execute(query)
            return render_template('institution_menu.html', cursor=cursor)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route("/doc_menu", methods=['GET', 'POST'])
def doctor_menu():
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        if request.method == "POST":
            if request.form['button'] == "insert":
                certificate = request.form['certificate']
                name = request.form['name']
                speciality = request.form['speciality']

                query = "INSERT INTO Doctor VALUES(%s, %s, %s);"

                cursor.execute(query, (certificate, name, speciality))
            elif request.form['button'] == "edit":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Doctor;"
                    cursor.execute(query)
                    return render_template('doctor_menu.html', cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "UPDATE Doctor SET "
                query_len = len(query)

                data = []

                if request.form["certificate"] != "":
                    query += "certificate_num=%s,"
                    data += [request.form["certificate"]]

                if request.form["name"] != "":
                    query += "doc_name=%s,"
                    data += [request.form["name"]]

                if request.form["speciality"] != "":
                    query += "doc_speciality=%s,"
                    data += [request.form["speciality"]]

                if len(query) == query_len:
                    query = "SELECT * FROM Doctor;"
                    cursor.execute(query)
                    return render_template('doctor_menu.html',
                                           cursor=cursor)

                query = query[:-1]

                query += " WHERE certificate_num=%s and doc_name=%s and doc_speciality=%s;"

                data += [to_update[0], to_update[1], to_update[2]]

                cursor.execute(query, tuple(data))
            elif request.form['button'] == "remove":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Doctor;"
                    cursor.execute(query)
                    return render_template('doctor_menu.html', cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "DELETE FROM Doctor WHERE certificate_num = %s and doc_name=%s;"

                cursor.execute(query, (to_update[0], to_update[1]))

            query = "SELECT * FROM Doctor;"
            cursor.execute(query)
            return render_template('doctor_menu.html', cursor=cursor)
        elif request.method == "GET":
            query = "SELECT * FROM Doctor;"
            cursor.execute(query)
            return render_template('doctor_menu.html', cursor=cursor)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route("/presc_menu", methods=['GET', 'POST'])
def prescription_menu():
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        if request.method == "POST":
            if request.form['button'] == "insert":
                certificate_num = request.form['certificate_num']
                patient_num = request.form['patient_num']
                presc_date = request.form['presc_date']
                substance = request.form['substance']
                subs_quant = request.form['subs_quant']

                query = "INSERT INTO Prescription VALUES(%s, %s, %s, %s, %s);"

                cursor.execute(query, (certificate_num, patient_num,
                                       presc_date, substance, subs_quant))
            elif request.form['button'] == "edit":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Prescription;"
                    cursor.execute(query)
                    return render_template('prescription_menu.html', cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "UPDATE Prescription SET "
                query_len = len(query)

                data = []

                if request.form["certificate_num"] != "":
                    query += "certificate_num=%s,"
                    data += [request.form['certificate_num']]

                if request.form["patient_num"] != "":
                    query += "patient_num=%s,"
                    data += [request.form['patient_num']]

                if request.form["presc_date"] != "":
                    query += "presc_date=%s,"
                    data += [request.form['presc_date']]

                if request.form["substance"] != "":
                    query += "substance=%s,"
                    data += [request.form['substance']]

                if request.form["subs_quant"] != "":
                    query += "subs_quant=%s,"
                    data += [request.form['subs_quant']]

                if len(query) == query_len:
                    query = "SELECT * FROM Prescription;"
                    cursor.execute(query)
                    return render_template('prescription_menu.html',
                                           cursor=cursor)

                query = query[:-1]

                query += " WHERE certificate_num=%s and patient_num=%s and presc_date=%s and substance=%s and subs_quant=%s;"

                data += [to_update[0], to_update[1],
                         to_update[2], to_update[3], to_update[4]]

                cursor.execute(query, tuple(data))
            elif request.form['button'] == "remove":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Prescription;"
                    cursor.execute(query)
                    return render_template('prescription_menu.html',
                                           cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "DELETE FROM Prescription WHERE certificate_num=%s and patient_num=%s and presc_date=%s and substance=%s and subs_quant=%s;"

                cursor.execute(
                    query, (to_update[0], to_update[1], to_update[2],
                            to_update[3], to_update[4]))

            query = "SELECT * FROM Prescription;"
            cursor.execute(query)
            return render_template('prescription_menu.html', cursor=cursor)
        elif request.method == "GET":
            query = "SELECT * FROM Prescription;"
            cursor.execute(query)
            return render_template('prescription_menu.html', cursor=cursor)
    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route("/analysis_menu", methods=['GET', 'POST'])
def analysis_menu():
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        if request.method == "POST":
            if request.form['button'] == "insert":
                analysis_num = request.form["analysis_num"]
                analysis_speciality = request.form["analysis_speciality"]
                certificate_num = request.form["certificate_num"]
                patient_num = request.form["patient_num"]
                analysis_date = request.form["analysis_date"]
                reg_date = request.form["reg_date"]
                analysis_name = request.form["analysis_name"]
                subs_quant = request.form["subs_quant"]
                institution_name = request.form["institution_name"]

                query = "INSERT INTO Analysis VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"

                cursor.execute(query, (analysis_num, analysis_speciality,
                                       certificate_num, patient_num,
                                       analysis_date, reg_date,
                                       analysis_name, subs_quant,
                                       institution_name))

            elif request.form['button'] == "edit":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Analysis;"
                    cursor.execute(query)
                    return render_template('analysis_menu.html',
                                           cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "UPDATE Analysis SET "
                query_len = len(query)

                data = []

                if request.form["analysis_num"] != "":
                    query += "analysis_num=%s,"
                    data += [request.form['analysis_num']]

                if request.form["analysis_speciality"] != "":
                    query += "analysis_speciality=%s,"
                    data += [request.form['analysis_speciality']]

                if request.form["certificate_num"] != "":
                    query += "certificate_num=%s,"
                    data += [request.form['certificate_num']]

                if request.form["patient_num"] != "":
                    query += "patient_num=%s,"
                    data += [request.form['patient_num']]

                if request.form["analysis_date"] != "":
                    query += "analysis_date=%s,"
                    data += [request.form['analysis_date']]

                if request.form["reg_date"] != "":
                    query += "reg_date=%s,"
                    data += [request.form['reg_date']]

                if request.form["analysis_name"] != "":
                    query += "analysis_name=%s,"
                    data += [request.form['analysis_name']]

                if request.form["subs_quant"] != "":
                    query += "subs_quant=%s,"
                    data += [request.form['subs_quant']]

                if request.form["institution_name"] != "":
                    query += "institution_name=%s,"
                    data += [request.form['institution_name']]

                if len(query) == query_len:
                    query = "SELECT * FROM Analysis;"
                    cursor.execute(query)
                    return render_template('analysis_menu.html',
                                           cursor=cursor)

                query = query[:-1]

                query += " WHERE analysis_num = %s and analysis_speciality = %s and certificate_num=%s and patient_num=%s and analysis_date = %s and reg_date = %s and analysis_name = %s and subs_quant = %s and institution_name = %s;"

                data += [to_update[0], to_update[1],
                         to_update[2], to_update[3],
                         to_update[4], to_update[5],
                         to_update[6], to_update[7],
                         to_update[8]]

                cursor.execute(query, tuple(data))

            elif request.form['button'] == "remove":
                if "checkbox" not in request.form:
                    query = "SELECT * FROM Analysis;"
                    cursor.execute(query)
                    return render_template('analysis_menu.html',
                                           cursor=cursor)

                to_update = request.form['checkbox'].split("|")

                query = "DELETE FROM Analysis WHERE analysis_num = %s and analysis_speciality = %s and certificate_num=%s and patient_num=%s and analysis_date = %s and reg_date = %s and analysis_name = %s and subs_quant = %s and institution_name = %s;"

                cursor.execute(query, (to_update[0], to_update[1],
                                       to_update[2], to_update[3],
                                       to_update[4], to_update[5],
                                       to_update[6], to_update[7],
                                       to_update[8]))

            else:
                query = "SELECT * FROM Analysis;"
                cursor.execute(query)
                return render_template('analysis_menu.html', cursor=cursor)

            query = "SELECT * FROM Analysis;"
            cursor.execute(query)
            return render_template('analysis_menu.html', cursor=cursor)

        elif request.method == "GET":
            query = "SELECT * FROM Analysis;"
            cursor.execute(query)
            return render_template('analysis_menu.html', cursor=cursor)

    except Exception as e:
        return str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route("/sale_menu", methods=['GET', 'POST'])
def sale_menu():
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        if request.method == "POST":

            if request.form['button'] == "buy":

                if request.form['sale_num'] != "" and request.form['record_date'] != "" and request.form['substance'] != "" and request.form['subs_quant'] != "" and request.form['sale_price'] != "" and request.form['inst_name'] != "":
                    if "checkbox" not in request.form:
                        query = "INSERT INTO PharmacySale VALUES(%s,%s,%s,%s,%s,%s);"
                        cursor.execute(query, (request.form["sale_num"],
                                               request.form["record_date"],
                                               request.form["substance"],
                                               request.form["subs_quant"],
                                               request.form["sale_price"],
                                               request.form["inst_name"]))

                    else:
                        prescription_info = request.form["checkbox"].split("|")
                        sale_num = request.form["sale_num"]
                        certificate_num = prescription_info[0]
                        patient_num = prescription_info[1]
                        presc_date = prescription_info[2]
                        substance = prescription_info[3]

                        return "{}".format(prescription_info)

                        query = "INSERT INTO PharmacySale VALUES(%s,%s,%s,%s,%s,%s);"

                        cursor.execute(query, (sale_num, request.form["record_date"],
                                               substance, request.form["subs_quant"],
                                               request.form["sale_price"],
                                               request.form["inst_name"]))

                        query = "INSERT INTO PrescriptionSale VALUES(%s,%s,%s,%s,%s);"

                        cursor.execute(query, (sale_num, certificate_num,
                                               patient_num, presc_date,
                                               substance))

            query = "SELECT * FROM Prescription;"
            cursor.execute(query)
            return render_template('sale_menu.html', cursor=cursor)

        elif request.method == "GET":
            query = "SELECT * FROM Prescription;"
            cursor.execute(query)
            return render_template('sale_menu.html', cursor=cursor)
    except Exception as e:
        str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route("/list_presc", methods=['POST', 'GET'])
def list_presc():
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        if request.form['doctor'] != "" and request.form['month'] != "" and request.form['year'] != "":
            doctor = request.form['doctor']
            month = request.form['month']
            year = request.form['year']

            query = "SELECT substance FROM Prescription NATURAL JOIN Doctor WHERE doc_name=%s and extract(month from presc_date)=%s and extract(year from presc_date)=%s;"
            cursor.execute(query, (doctor, month, year))
            return render_template('list_prescriptions.html', cursor=cursor)

        else:
            return redirect('./')

    except Exception as e:
        str(e)
    finally:
        dbConn.commit()
        cursor.close()
        dbConn.close()


@app.route("/list_glicemia", methods=['POST', 'GET'])
def list_glicemia():
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor1 = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor2 = dbConn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        query = '''with table1 as (select subs_quant, county_num, patient_num from Analysis inner join Institution on Institution.inst_name=Analysis.institution_name where analysis_name='glicémia' order by county_num) select m.patient_num, m.subs_quant, m.county_num
        from table1 m
            left join table1 b
                on m.county_num=b.county_num
                and m.subs_quant < b.subs_quant
        where b.subs_quant is NULL;'''

        cursor1.execute(query)

        query = '''with table1 as (select subs_quant, county_num, patient_num from Analysis inner join Institution on Institution.inst_name=Analysis.institution_name where analysis_name='glicémia' order by county_num) select m.patient_num, m.subs_quant, m.county_num
        from table1 m
            left join table1 b
                on m.county_num=b.county_num
                and m.subs_quant > b.subs_quant
        where b.subs_quant is NULL;'''
        cursor2.execute(query)

        return render_template('list_glicemia.html', cursor1=cursor1, cursor2=cursor2)
    except Exception as e:
        str(e)
    finally:
        dbConn.commit()
        cursor1.close()
        cursor2.close()
        dbConn.close()


CGIHandler().run(app)
