import MySQLdb
import  sys

#conectando a la base de datos
try:
    db=MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        db='moodle'
    )
except Exception as e:
    sys.exit('no podemos entrar a la base de datos')

def MostrarDatos():

    cursor= db.cursor()
    cursor.execute('SELECT * FROM cursos')
    datos=cursor.fetchall()
    if datos:
            for z in datos:
                print(str(z[0])+"--"+str(z[1]))

# muestra todo los cursos de la base de datos con su profesor asociado
def MostrarCursos():

    cursor= db.cursor()
    cursor.execute("SELECT userid AS 'codigo', user.firstname AS 'nombre profesor' , cursos.id AS 'nrc', fullname AS 'curso' FROM `mdl_role_assignments` AS role INNER JOIN `mdl_user` AS user ON role.userid= user.id INNER JOIN  `mdl_context` AS conte ON role.contextid= conte.id INNER JOIN  `mdl_course` AS cursos ON conte.instanceid= cursos.id WHERE roleid=3")
    datos=cursor.fetchall()
    if datos:
            for z in datos:
                nparticipantes=NumeroParticipantesCursos(str(z[2]))
                ntareas=Tareas(str(z[2]))
                nsubidas=TareasSubidas(str(z[2]))
                nforos = Foros(str(z[2]))
                nfsubidas = ForosSubidas(str(z[2]))

                print(str(z[0])+"--"+str(z[1])+"--"+str(z[2])+"--"+str(z[3]))
                print("detalles de "+str(z[3])+ ':')
                print("Numero de participantes: "+str(nparticipantes))
                print("Numero de tareas: "+ str(ntareas))
                print("Numero de tareas subidas: "+ str(nsubidas))
                print("Efectividad de tareas en el curso: "+ str(efectividad(nparticipantes,ntareas,nsubidas))+'%')
                print("Numero de foros: " + str(nforos))
                print("Numero de foros subidas: " + str(nfsubidas))
                print("Efectividad de foros en el curso: " + str(efectividad(nparticipantes, nforos, nfsubidas)) + '%')

    db.close()

#muestra todos  o el numero de los participantes en cada curso
def NumeroParticipantesCursos(curso):
    cursor = db.cursor()
    sql=("SELECT userid AS 'codigo', user.firstname AS 'nombre profesor' , cursos.id AS 'nrc', fullname AS 'curso' FROM `mdl_role_assignments` AS role INNER JOIN `mdl_user` AS user ON role.userid= user.id INNER JOIN  `mdl_context` AS conte ON role.contextid= conte.id INNER JOIN  `mdl_course` AS cursos ON conte.instanceid= cursos.id WHERE (roleid=3 OR roleid=5)")
    sql=sql+ "AND cursos.id = "+str(curso)
    cursor.execute(sql)
    participante = cursor.fetchall()
    if participante:
         return(len(participante))
    else:
        return (0)

#muestra el numero de tareas que tiene cada curso
def Tareas(curso):
    cursor = db.cursor()
    cursor.execute("SELECT name FROM `mdl_assign`WHERE course="+str(curso))
    tarea = cursor.fetchall()
    if tarea:
         return (len(tarea))
    else:
        return (0)

#muestra  el numero total de tareas subidas en el curso
def TareasSubidas(curso):
    cursor = db.cursor()
    cursor.execute("SELECT course ,tarea.name, sub.status FROM `mdl_assign` as tarea INNER JOIN `mdl_assign_submission`as sub ON tarea.id= sub.assignment WHERE sub.status='submitted' AND course="+str(curso))
    subidas = cursor.fetchall()
    if subidas:
         return (len(subidas))
    else:
        return (0)
#muestra el numero de tareas que tiene cada curso
def Foros(curso):
    cursor = db.cursor()
    cursor.execute("SELECT name FROM `mdl_forum`WHERE introformat=1  AND course="+str(curso))
    foros = cursor.fetchall()
    if foros:
         return (len(foros))
    else:
        return (0)

#muestra  el numero total de tareas subidas en el curso
def ForosSubidas(curso):
    cursor = db.cursor()
    cursor.execute(" SELECT foro.id, discu.id, po.message, po.userid FROM `mdl_forum` AS foro INNER JOIN `mdl_forum_discussions` AS discu ON foro.id=discu.forum INNER JOIN `mdl_forum_posts` AS po ON discu.id=po.discussion WHERE foro.course="+str(curso)+" GROUP BY po.userid")
    fsubidas = cursor.fetchall()
    if fsubidas:
         return (len(fsubidas))
    else:
        return (0)
def efectividad(participante, tareas,subidas):
    if tareas==0:
        return 0
    else:
        efectivida=(float(subidas)/float(participante*tareas))*100
        return efectivida

if __name__=="__main__":
    MostrarCursos()




""" SELECT foro.id, discu.id, po.message, po.userid FROM `mdl_forum` AS foro INNER JOIN `mdl_forum_discussions` AS discu ON foro.id=discu.forum INNER JOIN `mdl_forum_posts` AS po ON discu.id=po.discussion WHERE foro.course=4 GROUP BY po.userid"""