import sqlalchemy
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'Student_Sentiment_Analysis'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/student', methods =['GET','POST'])
def student():
    if request.method == 'POST':
        name = request.form['Name']
        reg = request.form['Reg']
        Department = request.form['Department']
        Review_Teaching = request.form['Review_teaching']
        Review_Course = request.form['Review_course']
        Review_exam = request.form['Review_exam']
        Review_lab = request.form['Review_lab']
        Review_library = request.form['Review_library']
        Review_extracurricular = request.form['Review_extracurricular']

        cur = mysql.connection.cursor()
        sql = "INSERT INTO final_Review(Name, Register_Number, Department, Review_Teaching, Review_Course, Review_Examination, Review_Lab, Review_Library, Review_extracurricular) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,[name,reg,Department,Review_Teaching,Review_Course,Review_exam,Review_lab,Review_library,Review_extracurricular])
        mysql.connection.commit()
        cur.close()
        return "Thank you for your Review"

    return render_template('index.html')

@app.route('/report')
def report():
    import pandas as pd
    import pickle
    import matplotlib.pyplot as plt

    engine = sqlalchemy.create_engine('mysql+pymysql://root:12345@localhost:3306/Student_Sentiment_Analysis')
    df = pd.read_sql_table('final_review', engine)
    df.to_csv('review.csv')

    df1 = pd.read_csv("review.csv")

    def teaching(data):
        Model = pickle.load(open('teaching.pkl', 'rb'))
        prediction_teaching = Model.predict(data)
        return prediction_teaching

    def course(data):
        Model = pickle.load(open('course.pkl', 'rb'))
        prediction_course = Model.predict(data)
        return prediction_course

    def Exam(data):
        Model = pickle.load(open('exam.pkl', 'rb'))
        prediction_exam = Model.predict(data)
        return prediction_exam

    def lab(data):
        Model = pickle.load(open('lab.pkl', 'rb'))
        prediction_lab = Model.predict(data)
        return prediction_lab

    def library(data):
        Model = pickle.load(open('library.pkl', 'rb'))
        prediction_library = Model.predict(data)
        return prediction_library

    def extra_curricular(data):
        Model = pickle.load(open('extra.pkl', 'rb'))
        prediction_extracurricular = Model.predict(data)
        return prediction_extracurricular

    output_teach = teaching(df1['Review_Teaching'])
    output_course = course(df1['Review_Course'])
    output_exam = Exam(df1['Review_Examination'])
    output_lab = lab(df1['Review_Lab'])
    output_library = library(df1['Review_Library'])
    output_extra = extra_curricular(df1['Review_extracurricular'])

    f_teach = output_teach.tolist()
    happy_teach = f_teach.count(1)
    sad_teach = f_teach.count(-1)
    neutral_teach = f_teach.count(0)
    anger_teach = f_teach.count(4)
    fear_teach = f_teach.count(5)
    joy_teach = f_teach.count(6)
    surprise_teach = f_teach.count(7)


    mylabels = ['Happy','Sad','Anger','Fear','Joy','Surprise']


    review_result_teach = [happy_teach,sad_teach,anger_teach,fear_teach,joy_teach,surprise_teach]

    f_course = output_course.tolist()
    happy_course = f_course.count(1)
    sad_course = f_course.count(-1)
    neutral_course = f_course.count(0)
    anger_course = f_course.count(4)
    fear_course = f_course.count(5)
    joy_course = f_course.count(6)
    surprise_course = f_course.count(7)

    review_result_course = [happy_course,sad_course,anger_course,fear_course,joy_course,surprise_course]

    f_exam = output_exam.tolist()
    happy_exam = f_exam.count(1)
    sad_exam = f_exam.count(-1)
    neutral_exam = f_exam.count(0)
    anger_exam = f_exam.count(4)
    fear_exam = f_exam.count(5)
    joy_exam = f_exam.count(6)
    surprise_exam = f_exam.count(7)

    review_result_exam = [happy_exam,sad_exam,anger_exam,fear_exam,joy_exam,surprise_exam]

    f_lab = output_lab.tolist()
    happy_lab = f_lab.count(1)
    sad_lab = f_lab.count(-1)
    neutral_lab = f_lab.count(0)
    anger_lab = f_lab.count(4)
    fear_lab = f_lab.count(5)
    joy_lab = f_lab.count(6)
    surprise_lab = f_lab.count(7)

    review_result_lab = [happy_lab,sad_lab,anger_lab,fear_lab,joy_lab,surprise_lab]
    print(review_result_lab)

    f_library = output_library.tolist()
    happy_library = f_library.count(1)
    sad_library = f_library.count(-1)
    neutral_library = f_library.count(0)
    anger_library = f_library.count(4)
    fear_library = f_library.count(5)
    joy_library = f_library.count(6)
    surprise_library = f_library.count(7)

    review_result_library = [happy_library,sad_library,anger_library,fear_library,joy_library,surprise_library]

    f_extra = output_extra.tolist()
    happy_extra = f_extra.count(1)
    sad_extra = f_extra.count(-1)
    neutral_extra = f_extra.count(0)
    anger_extra = f_extra.count(4)
    fear_extra = f_extra.count(5)
    joy_extra = f_extra.count(6)
    surprise_extra = f_extra.count(7)

    review_result_extra = [happy_extra,sad_extra,anger_extra,fear_extra,joy_extra,surprise_extra]

    overall_happy = happy_teach + happy_course + happy_library + happy_lab + happy_extra + happy_exam
    overall_sad = sad_teach + sad_course + sad_library + sad_lab + sad_extra + sad_exam
    overall_anger = anger_teach + anger_course + anger_library + anger_lab + anger_extra + anger_exam
    overall_fear = fear_teach + fear_course + fear_library + fear_lab + fear_extra + fear_exam
    overall_joy = joy_teach + joy_course + joy_library + joy_lab + joy_extra + joy_exam
    overall_surprise = surprise_teach + surprise_course + surprise_library + surprise_lab + surprise_extra + surprise_exam


    overall_review = [overall_happy,overall_sad, overall_anger, overall_fear, overall_joy ,overall_surprise ]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ffb244', '#8B4513']


    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    plt.pie(review_result_teach,autopct='%1.1f%%')
    plt.title("Review about Teaching")
    plt.legend(mylabels)
    plt.savefig("static/teach_img.jpg")

    fig = plt.figure()
    ax_1 = fig.add_axes([0, 0, 1, 1])
    ax_1.axis('equal')
    plt.pie(review_result_course,autopct='%1.1f%%')
    plt.title("Review about Course")
    plt.legend(mylabels)
    plt.savefig("static/course_img.jpg")

    fig = plt.figure()
    ax_2 = fig.add_axes([0, 0, 1, 1])
    ax_2.axis('equal')
    plt.pie(review_result_exam, autopct='%1.1f%%')
    plt.title("Review about Examination")
    plt.legend(mylabels)
    plt.savefig("static/exam_img.jpg")

    fig = plt.figure()
    ax_3 = fig.add_axes([0, 0, 1, 1])
    ax_3.axis('equal')
    plt.pie(review_result_lab,autopct='%1.1f%%')
    plt.title("Review about Lab")
    plt.legend(mylabels)
    plt.savefig("static/lab_img.jpg")

    fig = plt.figure()
    ax_4 = fig.add_axes([0, 0, 1, 1])
    ax_4.axis('equal')
    plt.pie(review_result_library,autopct='%1.1f%%')
    plt.title("Review about Library")
    plt.legend(mylabels)
    plt.savefig("static/library_img.jpg")

    fig = plt.figure()
    ax_5 = fig.add_axes([0, 0, 1, 1])
    ax_5.axis('equal')
    plt.pie(review_result_extra, autopct='%1.0f%%')
    plt.title("Review about Extracurricular")
    plt.legend(mylabels)
    plt.savefig("static/extra_img.jpg")

    fig = plt.figure()
    ax_6 = fig.add_axes([0, 0, 1, 1])
    ax_6.axis('equal')
    explode = (0.05, 0.05, 0.05,0.05,0.05,0.05)
    plt.pie(overall_review,autopct='%1.1f%%',startangle=90, pctdistance=0.85, explode = explode,colors = colors)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.legend(mylabels)
    plt.savefig("static/overall_img.jpg")

    return render_template('visualize.html')

@app.route('/next')
def next():
    import pandas as pd
    import pickle
    import matplotlib.pyplot as plt

    engine = sqlalchemy.create_engine('mysql+pymysql://root:12345@localhost:3306/Student_Sentiment_Analysis')
    df = pd.read_sql_table('final_review', engine)
    df.to_csv('review.csv')

    df1 = pd.read_csv("review.csv")

    def teaching(data):
        Model = pickle.load(open('teaching.pkl', 'rb'))
        prediction_teaching = Model.predict(data)
        return prediction_teaching

    def course(data):
        Model = pickle.load(open('teaching.pkl', 'rb'))
        prediction_course = Model.predict(data)
        return prediction_course

    def Exam(data):
        Model = pickle.load(open('teaching.pkl', 'rb'))
        prediction_exam = Model.predict(data)
        return prediction_exam

    def lab(data):
        Model = pickle.load(open('teaching.pkl', 'rb'))
        prediction_lab = Model.predict(data)
        return prediction_lab

    def library(data):
        Model = pickle.load(open('teaching.pkl', 'rb'))
        prediction_library = Model.predict(data)
        return prediction_library

    def extra_curricular(data):
        Model = pickle.load(open('teaching.pkl', 'rb'))
        prediction_extracurricular = Model.predict(data)
        return prediction_extracurricular

    output_teach = teaching(df1['Review_Teaching'])
    output_course = course(df1['Review_Course'])
    output_exam = Exam(df1['Review_Examination'])
    output_lab = lab(df1['Review_Lab'])
    output_library = library(df1['Review_Library'])
    output_extra = extra_curricular(df1['Review_extracurricular'])

    f_teach = output_teach.tolist()
    happy_teach = f_teach.count(1)
    sad_teach = f_teach.count(-1)
    neutral_teach = f_teach.count(0)
    anger_teach = f_teach.count(4)
    fear_teach = f_teach.count(5)
    joy_teach = f_teach.count(6)
    surprise_teach = f_teach.count(7)


    mylabels = ['Positive','Negative','Neutral']
    positive_teaching = happy_teach+joy_teach+surprise_teach
    negative_teaching = sad_teach+anger_teach+fear_teach


    review_result_teach = [positive_teaching,negative_teaching,neutral_teach]

    f_course = output_course.tolist()
    happy_course = f_course.count(1)
    sad_course = f_course.count(-1)
    neutral_course = f_course.count(0)
    anger_course = f_course.count(4)
    fear_course = f_course.count(5)
    joy_course = f_course.count(6)
    surprise_course = f_course.count(7)

    positive_course = happy_course + joy_course + surprise_course
    negative_course = sad_course + anger_course + fear_course

    review_result_course = [positive_course,negative_course,neutral_course]

    f_exam = output_exam.tolist()
    happy_exam = f_exam.count(1)
    sad_exam = f_exam.count(-1)
    neutral_exam = f_exam.count(0)
    anger_exam = f_exam.count(4)
    fear_exam = f_exam.count(5)
    joy_exam = f_exam.count(6)
    surprise_exam = f_exam.count(7)

    positive_exam = happy_exam + joy_exam + surprise_exam
    negative_exam = sad_exam + anger_exam + fear_exam
    review_result_exam = [positive_exam,negative_exam,neutral_exam]

    f_lab = output_lab.tolist()
    happy_lab = f_lab.count(1)
    sad_lab = f_lab.count(-1)
    neutral_lab = f_lab.count(0)
    anger_lab = f_lab.count(4)
    fear_lab = f_lab.count(5)
    joy_lab = f_lab.count(6)
    surprise_lab = f_lab.count(7)

    positive_lab = happy_lab + joy_lab + surprise_lab
    negative_lab = sad_lab + anger_lab + fear_lab
    review_result_lab = [positive_lab,negative_lab,neutral_lab]

    f_library = output_library.tolist()
    happy_library = f_library.count(1)
    sad_library = f_library.count(-1)
    neutral_library = f_library.count(0)
    anger_library = f_library.count(4)
    fear_library = f_library.count(5)
    joy_library = f_library.count(6)
    surprise_library = f_library.count(7)

    positive_library = happy_library + joy_library + surprise_library
    negative_library = sad_library + anger_library + fear_library
    review_result_library = [positive_library,negative_library,neutral_library]

    f_extra = output_extra.tolist()
    happy_extra = f_extra.count(1)
    sad_extra = f_extra.count(-1)
    neutral_extra = f_extra.count(0)
    anger_extra = f_extra.count(4)
    fear_extra = f_extra.count(5)
    joy_extra = f_extra.count(6)
    surprise_extra = f_extra.count(7)

    positive_extra = happy_extra + joy_extra + surprise_extra
    negative_extra = sad_extra + anger_extra + fear_extra
    review_result_extra = [positive_extra,negative_extra,neutral_extra]

    overall_positive = positive_teaching + positive_course + positive_library + positive_lab + positive_extra + positive_exam
    overall_negative = negative_teaching + negative_course + negative_library + negative_lab + negative_extra + negative_exam
    overall_neutral = neutral_teach + neutral_course + neutral_library + neutral_lab + neutral_extra + neutral_exam


    overall_review = [overall_positive,overall_negative, overall_neutral]


    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('equal')
    plt.pie(review_result_teach,autopct='%1.1f%%')
    plt.title("Review about Teaching")
    plt.legend(mylabels)
    plt.savefig("static/teach_img_PNN.jpg")

    fig = plt.figure()
    ax_1 = fig.add_axes([0, 0, 1, 1])
    ax_1.axis('equal')
    plt.pie(review_result_course,autopct='%1.1f%%')
    plt.title("Review about Course")
    plt.legend(mylabels)
    plt.savefig("static/course_img_PNN.jpg")

    fig = plt.figure()
    ax_2 = fig.add_axes([0, 0, 1, 1])
    ax_2.axis('equal')
    plt.pie(review_result_exam, autopct='%1.1f%%')
    plt.title("Review about Examination")
    plt.legend(mylabels)
    plt.savefig("static/exam_img_PNN.jpg")

    fig = plt.figure()
    ax_3 = fig.add_axes([0, 0, 1, 1])
    ax_3.axis('equal')
    plt.pie(review_result_lab,autopct='%1.1f%%')
    plt.title("Review about Lab")
    plt.legend(mylabels)
    plt.savefig("static/lab_img_PNN.jpg")

    fig = plt.figure()
    ax_4 = fig.add_axes([0, 0, 1, 1])
    ax_4.axis('equal')
    plt.pie(review_result_library,autopct='%1.1f%%')
    plt.title("Review about Library")
    plt.legend(mylabels)
    plt.savefig("static/library_img_PNN.jpg")

    fig = plt.figure()
    ax_5 = fig.add_axes([0, 0, 1, 1])
    ax_5.axis('equal')
    plt.pie(review_result_extra, autopct='%1.0f%%')
    plt.title("Review about Extracurricular")
    plt.legend(mylabels)
    plt.savefig("static/extra_img_PNN.jpg")

    fig = plt.figure()
    ax_6 = fig.add_axes([0, 0, 1, 1])
    ax_6.axis('equal')
    explode = (0.05, 0.05, 0.05)
    plt.pie(overall_review,autopct='%1.1f%%',startangle=90, pctdistance=0.85, explode = explode)
    plt.legend(mylabels)
    plt.savefig("static/overall_img_PNN.jpg")

    return render_template('next.html')

if __name__ =='__main__':
    app.run(debug=True)