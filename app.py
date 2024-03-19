import sqlite3
from flask import Flask, render_template, request, jsonify, url_for, redirect
import json
from student import Student

app = Flask(__name__)


@app.route('/', methods=['GET'])
def go_home():
    c = sqlite3.connect("student.db").cursor()
    c.execute("CREATE TABLE IF NOT EXISTS STUDENTS("
              "id TEXT, firstname TEXT, lastname TEXT, department TEXT)"
              )
    c.connection.close()
    
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def get_students():
    c = sqlite3.connect("student.db").cursor()
    c.execute("SELECT * FROM STUDENTS")
    students = c.fetchall()
    return render_template('students.html', students=students)

# @app.route('/getStudentById/<student_id>', methods=['GET'])
#def get_student_by_id(student_id):
 #       c = sqlite3.connect("student.db").cursor()
  ###    return jsonify(student) if student else jsonify({"message": "Student not found"})

@app.route('/addStudent', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        db = sqlite3.connect("student.db")
        c = db.cursor()
        student = Student(request.form["firstname"],
                          request.form["lastname"],
                          request.form["department"]
                          )
        c.execute("INSERT INTO STUDENTS VALUES(?,?,?,?)",
                  (student.id, student.firstname, student.lastname, student.department))
        db.commit()
        db.close()

        return redirect(url_for('get_students'))

    return render_template('addStudent.html')

@app.route('/updateStudent/<student_id>', methods=['POST', 'GET'])
def update_student(student_id):
    if request.method == 'POST':
        db = sqlite3.connect("student.db")
        c = db.cursor()
        student = Student(request.form["firstname"],
                          request.form["lastname"],
                          request.form["department"]
                          )
        c.execute("UPDATE STUDENTS SET firstname = ?, lastname =?, department =? WHERE id=?",
                  (student.firstname, student.lastname, student.department, student_id))
        db.commit()
        db.close()
        return redirect(url_for('get_students'))

    # Fetch the existing student data and pass it to the template for display or editing
    c = sqlite3.connect("student.db").cursor()
    c.execute("SELECT * FROM STUDENTS WHERE id=?", (student_id,))
    student = c.fetchone()
    return render_template('updateStudent.html', student = student)

@app.route('/deleteStudent/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    if request.method == 'DELETE':
        db = sqlite3.connect("student.db")
        c = db.cursor()
        c.execute("DELETE FROM STUDENTS WHERE id=?", (student_id,))
        db.commit()
        return jsonify({"message": "Record was successfully deleted"})

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=8888, debug=True)
