from flask import Flask, render_template, flash, request, session
import mysql.connector

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = 'abc'


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('Newuser.html')


@app.route("/Newuser", methods=['GET', 'POST'])
def Newuser():
    if request.method == 'POST':
        Name = request.form['name']
        Age = request.form['age']
        Gender = request.form['gender']
        Mobile = request.form['mobile']

        Email = request.form['email']

        Address = request.form['address']

        Username = request.form['username']
        Password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + Name + "','" + Gender + "','" + Age + "' , '" + Email + "','" + Mobile + "','" + Address + "','" + Username + "','" + Password + "')")
        conn.commit()
        conn.close()
        flash(' USER REGISTER SUCCESSFULLY')

    return render_template('Userlogin.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':

            flash("LOGIN SUCCESSFULLY")

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data1 = cur.fetchall()
            return render_template('AdminHome.html', data=data1)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb ")
    data1 = cur.fetchall()

    return render_template('Adminhome.html', data=data1)



@app.route("/Report")
def Report():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  reporttb ")
    data1 = cur.fetchall()
    return render_template('AReport.html', data=data1)



@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")
    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['uname'] = request.form['username']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('Userlogin.html')
        else:

            session['mob'] = data[2]
            session['email'] = data[3]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data1 = cur.fetchall()
            flash("LOGIN SUCCESSFULLY")

            return render_template('Userhome.html', data=data1)


@app.route("/ImPredict")
def ImPredict():
    return render_template('ImPredict.html')




@app.route("/userlogin1", methods=['GET', 'POST'])
def userlogin1():
    if request.method == 'POST':
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "' ")
        data1 = cur.fetchall()
        return render_template('Userhome.html', data=data1)

@app.route("/Userhome")
def Userhome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "' ")
    data1 = cur.fetchall()
    return render_template('Userhome.html', data=data1)

@app.route("/UReport")
def UReport():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25studentattendb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reporttb where username='" + session['uname'] + "' ")
    data1 = cur.fetchall()
    return render_template('UReport.html', data=data1)

@app.route("/Predict")
def Predict():
    import cv2
    from ultralytics import YOLO

    # Load the YOLOv8 model
    model = YOLO('runs/detect/stuatt/weights/best.pt')
    # Open the video file
    cap = cv2.VideoCapture(0)
    dd1 = 0

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.4)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name != 'awake':
                        dd1 += 1

                    if dd1 == 20:
                        dd1 = 0

                        import winsound
                        filename = 'alert.wav'
                        winsound.PlaySound(filename, winsound.SND_FILENAME)

                        annotated_frame = results[0].plot()

                        import random
                        loginkey = random.randint(1111, 9999)
                        imgg = "static/upload/" + str(loginkey) + ".jpg"

                        cv2.imwrite("alert.jpg", annotated_frame)
                        cv2.imwrite(imgg, annotated_frame)
                        sendmail()
                        sendmsg(session['mob'], "Prediction Name:" + object_name)

                        import datetime
                        date = datetime.datetime.now().strftime('%Y-%m-%d')

                        time = datetime.datetime.now().strftime('%H:%M:%S')

                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='25studentattendb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO  reporttb VALUES ('','" + session[
                                'uname'] + "','" + date + "','" + time + "','" + str(
                                imgg) + "','"+object_name +"')")
                        conn.commit()
                        conn.close()

                        return render_template('Result.html', org=imgg, out=object_name)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLO11 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()




@app.route("/impredict", methods=['GET', 'POST'])
def impredict():
    if request.method == 'POST':
        import os
        import cv2
        file = request.files['file']
        import random
        loginkey = random.randint(1111, 9999)
        file.save('static/upload/' + str(loginkey) + '.jpg')


        imgg = "static/upload/" + str(loginkey) + ".jpg"


        image = cv2.imread(imgg)

        from ultralytics import YOLO
        model = YOLO('runs/detect/stuatt/weights/best.pt')

        # Run YOLOv8 inference on the image
        results = model(image, conf=0.1)

        # Annotate the image
        annotated_image = image.copy()


        object_name = ''
        pre = ''

        for result in results:
            if result.boxes:
                for box in result.boxes:
                    # Extract class ID and name
                    class_id = int(box.cls)
                    object_name = model.names[class_id]

                    # Extract bounding box coordinates (x1, y1, x2, y2)
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Calculate bounding box area
                    width = x2 - x1
                    height = y2 - y1
                    area = width * height

                    # Draw the bounding box and label
                    cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f"{object_name}"
                    cv2.putText(
                        annotated_image, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                    )

                    print(f"Detected: {object_name}")







        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        time = datetime.datetime.now().strftime('%H:%M:%S')

        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                       database='25studentattendb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  reporttb VALUES ('','" + session[
                'uname'] + "','" + date + "','" + time + "','" + str(
                imgg) + "','"+object_name+"')")
        conn.commit()
        conn.close()


        cv2.imshow("YOLOv8 Prediction", annotated_image)
        #cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.imwrite(imgg, annotated_image)

        cv2.destroyAllWindows()

        return render_template('Result.html', org=imgg, out=object_name)





def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


def sendmail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr =  session['email']

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = "Student Attention Detection"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "alert.jpg"
    attachment = open("alert.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "kkvz xxke jmeb pcyb")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
