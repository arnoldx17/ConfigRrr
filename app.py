from flask import Flask, render_template, request
import pymysql
import sql
import mikrotikApi
import datetime

app = Flask(__name__)

app.secret_key = 'randomstring'


@app.route('/')
def index():
    conn = pymysql.connect(host=sql.dbHost, port=sql.dbPort,
                           user=sql.dbUser, passwd=sql.dbPassword, db=sql.dbName)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM routerboards")
    routerboardCount = cur.fetchall()
    cur.close()
    conn.close()
    routerboardCount = routerboardCount[0][0]
    return render_template('index.html', routerboardCount=routerboardCount)


@app.route('/routerboards', methods=['POST', 'GET'])
def routerboards():

    conn = pymysql.connect(host=sql.dbHost, port=sql.dbPort,
                           user=sql.dbUser, passwd=sql.dbPassword, db=sql.dbName)
    cur = conn.cursor()

    if request.method == 'POST':

        reqValue = request.form['submit']

        if reqValue == "Add":

            rb_identity = request.form['rb_identity']
            rb_ipAddress = request.form['rb_ipAddress']
            rb_Locality = request.form['rb_Locality']
            rb_Username = request.form['rb_Username']
            rb_Password = request.form['rb_Password']

            cur.execute("INSERT INTO `routerboards` (`id`, `identity`, `ipaddress`, `locality`, `username`, `password`) VALUES (NULL, '" +
                        rb_identity + "', '" + rb_ipAddress + "', '" + rb_Locality + "', '" + rb_Username + "', '" + rb_Password + "');")

        if reqValue.startswith('delButton'):
            rbId = reqValue[9:]
            cur.execute(
                "DELETE FROM `routerboards` WHERE `routerboards`.`id` = " + rbId + "")

    cur.execute("SELECT id, identity, ipaddress, locality FROM routerboards")
    routerboards = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('routerboards.html', routerboards=routerboards)


@app.route('/routerboards/id/<id>', methods=['POST', 'GET'])
def routerboard_details(id):

    conn = pymysql.connect(host=sql.dbHost, port=sql.dbPort,
                           user=sql.dbUser, passwd=sql.dbPassword, db=sql.dbName)
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM `routerboards` WHERE id = " + id + "")
    routerboardDetails = cur.fetchall()

    if request.method == 'POST':
        reqValue = request.form['submit']

        if reqValue == "reloadApiButton":
            username = routerboardDetails[0][4]
            password = routerboardDetails[0][5]
            host = routerboardDetails[0][2]

            try:
                details = mikrotikApi.getInfo(username, password, host)

                apiTime = datetime.datetime.now()
                apiTime = apiTime.strftime("%Y-%m-%d %I:%M:%S")

                cur.execute(""" UPDATE `routerboards` SET
                                `identity` = '""" + details[0] + """',
                                `routerosversion` = '""" + details[2] + """',
                                `boardname` = '""" + details[3] + """',
                                `architecturename` = '""" + details[4] + """',
                                `currentfirmware` = '""" + details[5] + """',
                                `model` = '""" + details[6] + """',
                                `serialnumber` = '""" + details[7] + """',
                                `apiok` = '1',
                                `apitime` = '""" + apiTime + """'
                                WHERE `routerboards`.`id` = """ + id + """;""")
                cur.execute(
                    "SELECT * FROM `routerboards` WHERE id = " + id + "")
                routerboardDetails = cur.fetchall()
            except Exception as e:
                print(e)

    cur.close()
    conn.close()

    return render_template('routerboard_details.html', routerboardDetails=routerboardDetails)



if __name__ == "__main__":
    app.run(debug=True)
