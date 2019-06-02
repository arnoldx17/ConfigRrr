from flask import Flask, render_template, request
import pymysql
import sql
import mikrotikApi
import datetime

app = Flask(__name__)

app.secret_key = 'randomstring'


@app.route('/')
def index():
    connection = pymysql.connect(host=sql.dbHost, port=sql.dbPort,
                                 user=sql.dbUser, passwd=sql.dbPassword, db=sql.dbName)
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute(""" SELECT
                        COUNT(*) AS routerboardCount,
                        COUNT(CASE WHEN `apiok` LIKE '1' THEN 1 END) AS apiok,
                        COUNT(CASE WHEN `apiok` LIKE '0' THEN 1 END) AS apinotok
                    FROM `routerboards`; """)
    data = cur.fetchall()
    cur.close()
    connection.close()
    return render_template('index.html', data=data)


@app.route('/routerboards', methods=['POST', 'GET'])
def routerboards():

    connection = pymysql.connect(host=sql.dbHost, port=sql.dbPort,
                                 user=sql.dbUser, passwd=sql.dbPassword, db=sql.dbName)
    cur = connection.cursor()

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
    connection.close()

    return render_template('routerboards.html', routerboards=routerboards)


@app.route('/routerboards/id/<id>', methods=['POST', 'GET'])
def routerboard_details(id):

    connection = pymysql.connect(host=sql.dbHost, port=sql.dbPort,
                                 user=sql.dbUser, passwd=sql.dbPassword, db=sql.dbName)
    cur = connection.cursor()
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
                rbDetails = mikrotikApi.getInfo(username, password, host)

                apiTime = datetime.datetime.now()
                apiTime = apiTime.strftime("%Y-%m-%d %I:%M:%S")

                cur.execute(""" UPDATE `routerboards` SET
                                `identity` = '""" + rbDetails["rbIdentity"] + """',
                                `routerosversion` = '""" + rbDetails["routerOsVersion"] + """',
                                `boardname` = '""" + rbDetails["boardName"] + """',
                                `architecturename` = '""" + rbDetails["architectureName"] + """',
                                `currentfirmware` = '""" + rbDetails["currentFirmware"] + """',
                                `model` = '""" + rbDetails["model"] + """',
                                `serialnumber` = '""" + rbDetails["serialNumber"] + """',
                                `apiok` = '1',
                                `apitime` = '""" + apiTime + """'
                                WHERE `routerboards`.`id` = """ + id + """;""")
                cur.execute(
                    "SELECT * FROM `routerboards` WHERE id = " + id + "")
                routerboardDetails = cur.fetchall()
            except Exception as e:
                print(e)

    cur.close()
    connection.close()

    return render_template('routerboard_details.html', routerboardDetails=routerboardDetails)


if __name__ == "__main__":
    app.run(debug=True)
