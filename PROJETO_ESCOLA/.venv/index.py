from flask import Flask, render_template, redirect, request, url_for
import mysql.connector

app = Flask(__name__)


#****************************************************Rota de cadastro********************************************************************************
@app.route("/cadastrar")
def createAcount():
    return render_template("createAcount.html", titulo_nav = "Escola vai quem quer", titulo_body = "Cadastrar Usuário")
#*****************************************************Rota de cadastro**********************************************************************
@app.route("/cadastrar", methods=["POST"])
def createAcountInsert():
    error_message = None
    
    name = request.form["name"]
    cpf = request.form["cpf"]
    email = request.form["email"]
    phone = request.form["phone"]
    password = request.form["password"]
    confirmPassword = request.form["confirmPassword"]
    typeUser = request.form["user"]  
    
    name = name.lower()    
    cpf = cpf.replace('.','').replace('.','').replace('-','')
    email = email.lower()
           
    passwordValid = verifyPassword(password, confirmPassword)
    
    if not password:
        error_message = 'Digite a senha e confirmar senha corretamente*.'
        return render_template('createAcount.html', error_message=error_message, titulo_nav = "Escola vai quem quer", titulo_body = "Cadastrar Usuário" )
    
    resultado = insertCadastrar(cpf, name, email, phone, password, typeUser == "Aluno", typeUser == "Professor")    
    
    if not resultado:
        error_message = 'Nome ou cpf de usuário já cadastrados*.'
        return render_template('createAcount.html', error_message=error_message,  titulo_nav = "Escola vai quem quer", titulo_body = "Cadastrar Usuário")
        
            
    return redirect(url_for("login"))


#***********************************************Pagina Cadastrar aluno************************************************************
@app.route("/cadastrarAluno")
def createAcountStudant():
    return render_template("createAcountStudant.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Aluno")

@app.route("/cadastrarAluno", methods=["POST"])
def createAcountStudantInsert():
    
    error_message = None
    
    name = request.form["name"]
    cpf = request.form["cpf"]
    password = request.form["password"]
    confirmPassword = request.form["confirmPassword"]
    user = request.form["user"]
    
    
    name = name.lower()    
    cpf = cpf.replace('.','').replace('.','').replace('-','')
    
    passwordValid = verifyPassword(password, confirmPassword)
    if not passwordValid:
        error_message = 'Digite a senha e confirmar senha corretamente*.'
        return render_template('createAcountStudant.html', error_message=error_message, titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Aluno" )
    
    resultado = insertCadastrarUsuario(cpf, name, password, user)
    
    if not resultado:
        error_message = 'Aluno ou CPF já cadastrado.'
        return render_template('createAcountStudant.html', error_message=error_message, titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Aluno" )
    
    return redirect(url_for("home"))
# ************************************************ Buscar cadastros de alunos ***************************************************
@app.route("/editarCadastroAluno")
def searchAcountStudent():
    listaAlunosCadastrados = selectStudent()
    return render_template("editAcount.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar / Excluir Alunos", listaAlunosCadastrados=listaAlunosCadastrados)

@app.route("/excluirCadastroAluno/<aluno>")
def excluirCadastroAluno(aluno):
    error_message = None
    if aluno == "":
        error_message = "Não há dados Cadastrados."
        return render_template("editAcount.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar / Excluir Alunos", error_message=error_message)
    deleteStudent(aluno)
    return  redirect(url_for("searchAcountStudent"))
#****************************************************Editar cadastro do aluno ***************************************************
@app.route("/editAluno/<aluno>")
def editDataAluno(aluno):    
    dataAluno = selectStudentOne(aluno)      
    return render_template("editCadastroStudant.html",titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar Dados Cadastrais do Aluno", dataAluno = dataAluno)
# ************************************************* Erro caso senhas e confirm nao sejam iguais ********************************
@app.route("/editAluno")
def errorAluno():   
    error_message1 = None
    idAluno = request.args.get("idAluno")
    error_message1 = request.args.get("message")
    dataAluno = selectStudentOne(idAluno)      
    return render_template("editCadastroStudant.html",titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar Dados Cadastrais do Aluno", dataAluno = dataAluno, error_message1=error_message1)
#*************************************************** Editar cadastro parte 2 ***************************************************
@app.route("/editAluno", methods=["POST"])
def editAluno():
    idAluno = request.form["id"]
    nome = request.form["name"]
    cpf = request.form["cpf"]
    senha = request.form["password"]
    confirmSenha = request.form["confirmPassword"]
      
    #apos capturado verificar password e senha se estão corretos,
    if senha != confirmSenha:
        message = "Digite corretamente senha e confirmar senha para continuar"
        return redirect(url_for("errorAluno", message=message, idAluno=idAluno))
    
    nome = nome.lower()
    
    updateDataStudant(idAluno, nome, cpf, senha)
    
    
    
    #fazer o update dos dados
    return redirect(url_for("searchAcountStudent"))
# ************************************************* Cadastrar Funcionario get *******************************************************
@app.route("/cadastrarFuncionario")
def createAcountFuncionario():
    return render_template("createAcountFuncionario.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Funcionario Academico")
#************************************************* Cadastrar Funcionario no banco de dados ****************************************

@app.route("/cadastrarFuncionario", methods=["POST"])
def createAcountFuncionarioInsert():
    
    error_message = None
    
    name = request.form["name"]
    nameLogin = request.form["nameLogin"]
    email = request.form["email"]
    cpf = request.form["cpf"]
    password = request.form["password"]
    confirmPassword = request.form["confirmPassword"]
    user = request.form["user"]
        
    name = name.lower()
    nameLogin = nameLogin.lower()    
    cpf = cpf.replace('.','').replace('.','').replace('-','')
    
    passwordValid = verifyPassword(password, confirmPassword)
    if not passwordValid:
        error_message = 'Digite a senha e confirmar senha corretamente*.'
        return render_template('createAcountFuncionario.html', error_message=error_message, titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Funcionário Academico")
    
    resultado = insertCadastrarUsuario(cpf, name, password, user, nameLogin, email)
    print(resultado)
    
    if not resultado:
        error_message = 'Funcionario, CPF ou Nome para login já cadastrado.'
        return render_template('createAcountFuncionario.html', error_message=error_message, titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Funcionário Academico" )
    
    return redirect(url_for("home"))
# ************************************************* Editar / Excluir  Funcionario *********************************************
@app.route("/editarCadastroFuncionario")
def searchAcountFuncionario():
    listaFuncionariosCadastrados = selectFuncionario()
    return render_template("editAcountFuncionario.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar / Excluir Funcionários", listaFuncionariosCadastrados=listaFuncionariosCadastrados)
# ************************************************** Excluir funcionario do banco de dados *************************************
@app.route("/excluirCadastroFuncionario/<funcionario>")
def excluirCadastroFuncionario(funcionario):
    error_message = None
    if funcionario == "":
        error_message = "Não há dados Cadastrados."
        return render_template("editAcountFuncionario.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar / Excluir Funcionários", error_message=error_message)
    deleteFuncionario(funcionario)    
    return redirect(url_for("searchAcountFuncionario"))
# ************************************************* Editar dados Funcionario *********************************************
@app.route("/editFuncionario/<funcionario>")
def editFuncionario(funcionario):
    dataFuncionario = selectOneFuncionario(funcionario)
    return render_template("editCadastroFuncionario.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar dados de Funcionários", dataFuncionario=dataFuncionario)
# ************************************************** error funcionario ******************************************************
@app.route("/errorFuncionario")
def errorFuncionario():
    error_message1 = None
    idFuncionario = request.args.get("idFuncionario")
    error_message1 = request.args.get("message")
    dataFuncionario =  selectOneFuncionario(idFuncionario)   
    return render_template("editCadastroFuncionario.html",titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar Dados Cadastrais do Funcionário", dataFuncionario = dataFuncionario, error_message1=error_message1)
    

#************************************************** fazer atualização cadastral do funcionario ***********************************
@app.route("/editFuncionario", methods=["POST"])
def editDataFuncionario():
    idFuncionario = request.form["id"]
    cpf = request.form["cpf"]
    nome = request.form["name"]
    user = request.form["nameLogin"]
    email = request.form["email"]
    senha = request.form["password"]
    confirmSenha = request.form["confirmPassword"]
    #apos capturado verificar password e senha se estão corretos,
    if senha != confirmSenha:
        message = "Digite corretamente senha e confirmar senha para continuar"
        return redirect(url_for("errorFuncionario", message=message, idFuncionario=idFuncionario))
    nome = nome.lower()
    user = user.lower()
    email = email.lower()
    
    updateDataFuncionario(idFuncionario, cpf, nome, user, email, senha)
    
    return redirect(url_for("searchAcountFuncionario"))

# *********************************** Rota de cadastramento de displina **********************************************************
@app.route("/cadastrarDisciplina")
def cadastrarDisciplina():
    return render_template('createDiscipline.html', titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Disciplinas")

@app.route("/cadastrarDisciplina", methods=["POST"])
def cadastrarDisciplinaInsert():
    
    error_message = None
    
    nameDisciplina = request.form["disciplina"]
    
    nameDisciplina = nameDisciplina.lower()    
    
    resultado = insertCadastrarDisplina(nameDisciplina)
    
    if not resultado:
        error_message = 'Disciplina já cadastrado.'
        return render_template('createDiscipline.html',error_message = error_message, titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastramento de Disciplinas")
    return redirect(url_for("home"))
# ************************************************* Editar / Excluir  Disciplina *********************************************
@app.route("/editarCadastroDisciplina")
def searchDsiciplina():
    
    listaDisciplinas = selectDisciplinas()
    
    return render_template("editDisciplinas.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar / Excluir Disciplinas", listaDisciplinas=listaDisciplinas)

#*************************************************** Excluir disciplina *********************************************************
@app.route("/excluirCadastroDisciplina/<disciplina>")
def excluirDisciplina(disciplina):
    deleteDisciplina(disciplina)
    return redirect(url_for("searchDsiciplina"))
# ********************************************** editar dados de disciplina *****************************************************
@app.route("/editarDisciplina/<disciplina>")
def editDisciplina(disciplina):
    
    dataDisciplina = selectOneDisciplina(disciplina)
        
    return render_template("editCadastroDisciplina.html",titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar Disciplinas Cadastradas", dataDisciplina=dataDisciplina)

# ******************************************* editar disciplina no banco de dados ************************************************
@app.route("/editarDisciplina", methods = ["POST"])
def editDataDisciplina():
    idDisciplina = request.form["id"]
    nomeDisciplina = request.form["disciplina"]
    
    nomeDisciplina = nomeDisciplina.lower()
    
    updateDisciplina(idDisciplina, nomeDisciplina)
    
    return redirect(url_for("searchDsiciplina"))
#************************************************ Cadastrar notas de alunos ******************************************************
@app.route("/CadastrarNotas")
def searchStudantAndDisciplinas():    
    listStudants = selectStudent()
    listaDisciplinas = selectDisciplinas() 
    listaCadastrosNotas = selectCadastrosNotas()
    
    successo = request.args.get('sucesso')
    error_message2 = None
    error_message2 = None
    if listStudants == []:
        error_message2 = "Não há alunos cadastrados. Cadastre alunos para continuar."
        
        return render_template("registerNotes.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastrar notas", listStudants=listStudants, listaDisciplinas=listaDisciplinas, error_message2=error_message2)
    if listaDisciplinas == []:
        error_message3 = "Não há disciplinas cadastradas. Cadastre displinas para continuar."
        return render_template("registerNotes.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastrar notas", listStudants=listStudants, listaDisciplinas=listaDisciplinas, error_message2=error_message3)
    listaCadastrosNotas = sorted(listaCadastrosNotas, key=lambda x: (x[3], x[2]))
    
    return render_template("registerNotes.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Cadastrar notas", listStudants=listStudants, listaDisciplinas=listaDisciplinas, error_message2=successo, listaCadastrosNotas=listaCadastrosNotas)
# ********************************************** inserir dados de notas no banco de dados *************************************
@app.route("/CadastrarNotas", methods=["POST"])
def insertStudantAndDisciplinas():    
    error_message2 = None
    error_message3 = None
    
    selectStudant = request.form["studant"]
    selectDisciplina = request.form["disciplina"]
    print(selectStudant, selectDisciplina)
    nota = request.form["nota"]
    verifyQuantNotas = veryNotasCadast(selectStudant, selectDisciplina)
    if not verifyQuantNotas:
        return redirect(url_for("searchStudantAndDisciplinas", sucesso="Todas as notas da disciplina já foram cadastradas. Va em editar notas para alterar."))
    insertDataNota(selectStudant, selectDisciplina, nota) 
    error_message2 = "Nota Cadastrada com sucesso."
    return redirect(url_for("searchStudantAndDisciplinas", sucesso="Nota Cadastrada com sucesso"))
# ********************************************** editar / excluir dados de notas no banco de dados **************************
@app.route("/editarCadastroNotas")
def editNotes():
    message = None
    listaCadastrosNotas = selectCadastrosNotas()
    message = request.args.get("message")
    listaCadastrosNotas = sorted(listaCadastrosNotas, key=lambda x: (x[3], x[2]))
    
    return render_template("editNotesCreate.html",titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar / Excluir notas cadastradas",listaCadastrosNotas=listaCadastrosNotas, message=message )
#********************************************** editar dados de notas cadastradas ******************************************
@app.route("/editNotas/<nota>")
def editNotas(nota):
    dataNota = selectNotasOne(nota)
    return render_template("editCadastroNota.html",titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica - Editar notas cadastradas", dataNota=dataNota)
# ********************************************* atualizar notas no banco de dados *****************************************
@app.route("/editNotas", methods=["POST"])
def editDataNotas():
    idNota = request.form["id"]
    nota = request.form["nota"]
    updateNota(idNota, nota)    
    
    return redirect(url_for("editNotes"))
    
# *********************************************** excluir notas cadastradas ************************************************
@app.route("/deleteCadastroNotas/<nota>")
def excluirNotas(nota):
    deliteNota(nota)
    return redirect(url_for("editNotes", message="Nota Excluida com sucesso"))    

#***********************************************Pagina home Secretaria************************************************************
@app.route("/home")
def home():
    return render_template("homePageSecretaria.html", titulo_nav = "Escola vai quem quer", titulo_body = "Secretária Academica")

#***********************************************Rota principal *******************************************************************
@app.route("/")
def initPage():
    return render_template("initPage.html", titulo_nav = "Escola vai quem quer", titulo_body = "Seja Bem Vindo!")
# ********************************************* Rota de logar usuario funcionario *********************************************
@app.route("/loginProfessor")
def login():
    return render_template("index.html", titulo_nav = "Escola vai quem quer", titulo_body = "Seja Bem Vindo á Pagina do Funcionário Academico")
# ********************************************** validacao e ligin de funcionario **********************************************
@app.route("/loginProfessor", methods=["POST"])
def loginUser():
    user = request.form["user"]
    senha = request.form["password"]
    userCheck = request.form["userCheck"]
    
    resultado = verifyUser(user, senha, userCheck)
    print(resultado)
    
    if not resultado:
        error_message = "Usuário ou senha invalido. Tente novamente"
        return render_template("index.html", error_message = error_message, titulo_nav = "Escola vai quem quer", titulo_body = error_message)
    if userCheck == "Professor":
        return redirect(url_for("home"))
    
    return render_template("index.html", error_message = error_message, titulo_nav = "Escola vai quem quer", titulo_body = error_message)
# ********************************************* Rota de logar usuario aluno *********************************************
@app.route("/loginAluno")
def loginAluno():
    return render_template("indexAluno.html", titulo_nav = "Escola vai quem quer", titulo_body = "Seja Bem Vindo a Página do Aluno!")

# ********************************************** validacao e ligin de Aluno **********************************************

@app.route("/loginAluno", methods=["POST"])
def loginAlunoHome():
    cpf = request.form["cpf"]
    senha = request.form["password"]
    error_message = None
    cpf = cpf.replace('.','').replace('.','').replace('-','')
    searchDataStudant = selectStudentOneCpf(cpf)
    print(searchDataStudant)
    if not searchDataStudant:
        error_message = "CPF ou senha invalidos, digite corretamente para acessar a home do aluno!"
        return render_template("indexAluno.html",titulo_nav = "Escola vai quem quer", titulo_body = "Seja Bem Vindo a Página do Aluno!", error_message=error_message)
    
    if senha != searchDataStudant[3]:
        error_message = "CPF ou senha invalidos, digite corretamente para acessar a home do aluno!"
        return render_template("indexAluno.html",titulo_nav = "Escola vai quem quer", titulo_body = "Seja Bem Vindo a Página do Aluno!", error_message=error_message)
    
    searchNotasStudant = selectNotasOneStuant(searchDataStudant[0])
    print( searchNotasStudant)
    
    materias = {}
    for item in searchNotasStudant:
        key = (item[5])
        if key not in materias:
            materias[key] = {'nome': item[5], 'notas':[]}
        materias[key]['notas'].append(item[3])
    
    for disciplina in materias.values():
        if disciplina['notas']:
            disciplina['media'] = sum(disciplina['notas']) / len(disciplina['notas'])
        else:
            disciplina['media'] = None
   
    for disciplina in materias.values():
        # Preencher com zeros se tiver menos de 4 notas
        disciplina['notas'] += [0.0] * (4 - len(disciplina['notas']))

        # Calcular a média
        disciplina['media'] = sum(disciplina['notas']) / len(disciplina['notas']) if len(disciplina['notas']) > 0 else None
    print(materias)
    return render_template("homePageAluno.html",titulo_nav = "Escola vai quem quer", titulo_body = "Seja Bem Vindo a home page do aluno" , searchDataStudant=searchDataStudant, materias=materias)

#***********************************************************************************************************************************
#***********************************************************************************************************************************
#***********************************************************************************************************************************
'''comando banco de dados'''
# Conecao com banco
def conn():
    return mysql.connector.connect(
        host = 'mysql01.cgkdrobnydiy.us-east-1.rds.amazonaws.com',
        user = 'aluno_fatec',
        password = 'aluno_fatec',   
        database = 'meu_banco' 
    )
# *********************************************************************************************************************************
# busca de notas do aluno individual
def selectNotasOneStuant(idAluno):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT A.IDUSER, A.CPF, A.NOME , N.NOTA, D.IDDISCIPLINA, D.NOME_DISCIPLINA FROM denis_TB_notas N INNER JOIN denis_TB_disciplina D ON D.IDDISCIPLINA = N.ID_DISCIPLINA	INNER JOIN denis_TB_aluno A ON A.IDUSER = N.ID_ALUNO WHERE A.IDUSER = {};".format(idAluno)
    print(query)
    myCursor.execute(query)
    resultado = myCursor.fetchall()     
    return resultado
#*****************************************************************************************************************************
#atualizacao de dados de aluno,  materia e nota
def updateNota(idNota, nota):
    db = conn()
    mycursor = db.cursor()
    query = "UPDATE denis_TB_notas SET NOTA = '{}' WHERE IDNOTA = {};".format(nota, idNota)
    mycursor.execute(query)
    db.commit()     
    return True
    
#*****************************************************************************************************************************
#selecao de dados de alunp,  materia e nota
def selectNotasOne(nota):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT A.IDUSER, A.NOME, D.IDDISCIPLINA, D.NOME_DISCIPLINA,N.IDNOTA, N.NOTA FROM denis_TB_notas N INNER JOIN denis_TB_disciplina D ON D.IDDISCIPLINA = N.ID_DISCIPLINA	INNER JOIN denis_TB_aluno A ON A.IDUSER = N.ID_ALUNO WHERE N.IDNOTA = {};".format(nota)
    myCursor.execute(query)
    resultado = myCursor.fetchone() 
    return resultado
#*****************************************************************************************************************************
#atualizar disciplina
def updateDisciplina(idDisciplina, nomeDisciplina):
    db = conn()
    mycursor = db.cursor()
    query = "UPDATE denis_TB_disciplina SET NOME_DISCIPLINA = '{}' WHERE IDDISCIPLINA = {};".format(nomeDisciplina, idDisciplina)
    mycursor.execute(query)
    db.commit()     
    return True
#*****************************************************************************************************************************
#filtrar dados de uma disciplina
def selectOneDisciplina(idDisciplina):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT IDDISCIPLINA, NOME_DISCIPLINA FROM denis_TB_disciplina WHERE IDDISCIPLINA = '{}';".format(idDisciplina)
    myCursor.execute(query)
    resultado = myCursor.fetchone()   
    return resultado
# ****************************************************************************************************************************
#fazer update dos dados do funcionario
def updateDataFuncionario(idFuncionario, cpf, nome, user, email, senha):
    db = conn()
    mycursor = db.cursor()
    query = "UPDATE denis_TB_funcionario SET NOME = '{}', CPF = '{}', SENHA = '{}', EMAIL = '{}', NOMELOGIN = '{}' WHERE IDUSER = {};".format(nome, cpf, senha, email, user, idFuncionario)
    mycursor.execute(query)
    db.commit()    
    return True
#*****************************************************************************************************************************
#filtrar dados de um unico funcionario
def selectOneFuncionario(funcionario):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT * FROM denis_TB_funcionario WHERE IDUSER = {};".format(funcionario)
    myCursor.execute(query)
    resultado = myCursor.fetchone()    
    return resultado
# ****************************************************************************************************************************
#fazer update dos dados do aluno 
def updateDataStudant(idAluno, nome, cpf, senha):
    db = conn()
    mycursor = db.cursor()
    query = "UPDATE denis_TB_aluno SET NOME = '{}', CPF = '{}', SENHA = '{}' WHERE IDUSER = {};".format(nome, cpf, senha, idAluno)
    mycursor.execute(query)
    db.commit()    
    return True
# ****************************************************************************************************************************
#deletar  nota do aluno 
def deliteNota(idNota):
    db = conn()
    myCursor = db.cursor()
    query = "DELETE FROM denis_TB_notas WHERE IDNOTA = {}".format(idNota)
    myCursor.execute(query)
    db.commit() 
    return True
# ****************************************************************************************************************************
#buscar cadastro de nota do aluno 
def veryNotasCadast(selectStudant, selectDisciplina):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT A.IDUSER,D.IDDISCIPLINA, N.NOTA, D.NOME_DISCIPLINA, A.CPF, A.NOME FROM denis_TB_notas N INNER JOIN denis_TB_disciplina D ON D.IDDISCIPLINA = N.ID_DISCIPLINA	INNER JOIN denis_TB_aluno A ON A.IDUSER = N.ID_ALUNO WHERE A.IDUSER = {};".format(selectStudant)
    myCursor.execute(query)
    resultado = myCursor.fetchall()
    cont = 0
    for listResult in resultado:
        if selectDisciplina == str(listResult[1]):
            cont = cont + 1
        if cont > 3:
            return False
    print('cheguei aqui')
    return True 
#********************************************************************************************************************************
#buscar cadastro de nota do aluno 
def selectCadastrosNotas():
    db = conn()
    myCursor = db.cursor()
    query = "SELECT A.IDUSER, N.NOTA, D.NOME_DISCIPLINA, A.CPF, A.NOME, N.IDNOTA FROM denis_TB_notas N INNER JOIN denis_TB_disciplina D ON D.IDDISCIPLINA = N.ID_DISCIPLINA	INNER JOIN denis_TB_aluno A ON A.IDUSER = N.ID_ALUNO;"
    myCursor.execute(query)
    resultado = myCursor.fetchall()    
    return resultado   
# ****************************************************************************************************************************
#inserindo cadastro de nota do aluno 
def insertDataNota(selectStudant, selectDisciplina, nota):    
    db = conn()
    myCursor = db.cursor()  
    # insercao de dados caso esteja tudo ok   
    query = "INSERT INTO denis_TB_notas (ID_ALUNO, ID_DISCIPLINA, NOTA) VALUES (%s, %s, %s);"
    values = (selectStudant, selectDisciplina, nota)
    myCursor.execute(query, values)
    db.commit() 
    return True
# ****************************************************************************************************************************
#deletar disciplinas cadastradas no banco de dados
def deleteDisciplina(idDisciplina):
    db = conn()
    myCursor = db.cursor()
    query = "DELETE FROM denis_TB_disciplina WHERE IDDISCIPLINA = {}".format(idDisciplina)
    myCursor.execute(query)
    db.commit() 
    return True
# ****************************************************************************************************************************
#buscar dados de disciplinas cadastradas no banco de dados
def selectDisciplinas():
    db = conn()
    myCursor = db.cursor()
    query = "SELECT * FROM denis_TB_disciplina;"
    myCursor.execute(query)
    resultado = myCursor.fetchall()    
    return resultado
# ****************************************************************************************************************************
#deletar funcionario cadastrado
def deleteFuncionario(idFuncionario):
    db = conn()
    myCursor = db.cursor()
    query = "DELETE FROM denis_TB_funcionario WHERE IDUSER = {}".format(idFuncionario)
    myCursor.execute(query)
    db.commit()     
    return True
# ****************************************************************************************************************************
#buscar dados de funcionarios cadastrados no banco de dados
def selectFuncionario():
    db = conn()
    myCursor = db.cursor()
    query = "SELECT IDUSER, CPF, NOME, NOMELOGIN, EMAIL, SENHA FROM denis_TB_funcionario;"
    myCursor.execute(query)
    resultado = myCursor.fetchall()    
    return resultado
# ****************************************************************************************************************************
#deletar aluno cadastrado
def deleteStudent(idAluno):
    db = conn()
    myCursor = db.cursor()
    query = "DELETE FROM denis_TB_aluno WHERE IDUSER = {}".format(idAluno)
    myCursor.execute(query)
    db.commit()    
    return True
# ****************************************************************************************************************************
#buscar dados de alunos cadastrados no banco de dados
def selectStudent():
    db = conn()
    myCursor = db.cursor()
    query = "SELECT IDUSER, CPF, NOME FROM denis_TB_aluno;"
    myCursor.execute(query)
    resultado = myCursor.fetchall()
        
    return resultado
# ****************************************************************************************************************************
#buscar dados de alunos cadastrados no banco de dados
def selectStudentOne(idAluno):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT IDUSER, CPF, NOME, SENHA FROM denis_TB_aluno WHERE IDUSER = {};".format(idAluno)
    myCursor.execute(query)
    resultado = myCursor.fetchone()
        
    return resultado

#buscar dados de alunos cadastrados por cpf
def selectStudentOneCpf(cpfAluno):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT IDUSER, CPF, NOME, SENHA FROM denis_TB_aluno WHERE CPF = {};".format(cpfAluno)
    myCursor.execute(query)
    resultado = myCursor.fetchone()
        
    return resultado

# ****************************************************************************************************************************
#Verificação e inserção em cadastrar displina
def insertCadastrarDisplina(disciplina):
    db = conn()
    myCursor = db.cursor()
    query = "SELECT * FROM denis_TB_disciplina WHERE NOME_DISCIPLINA = '{}'".format(disciplina)
    myCursor.execute(query)
    resultado = myCursor.fetchall()
    if resultado != []:       
        return False
    # insercao de dados caso esteja tudo ok   
    query = "INSERT INTO denis_TB_disciplina (NOME_DISCIPLINA) VALUES ('{}')".format(disciplina)
    print(query)
    myCursor.execute(query)
    db.commit()         
    return True
#******************************************************************************************************************************
# verificacao e insercao de dados em cadastro   
def insertCadastrar(cpf, nome, email, telefone, senha, aluno, professor):
    db = conn()
    myCursor = db.cursor()
    # verificacao de existencia de nome de usuario e cpf
    query = "SELECT * FROM denis_TB_user_school WHERE NOME = '{}' OR CPF = '{}'".format(nome, cpf)
    myCursor.execute(query)
    resultado = myCursor.fetchall()
    if resultado != []:       
        return False    
    # insercao de dados caso esteja tudo ok   
    query = "INSERT INTO denis_TB_user_school (CPF, NOME, EMAIL, TELEFONE, SENHA, ALUNO, PROFESSOR ) VALUES (%s,%s, %s,%s,%s, %s,%s)"
    values = (cpf, nome, email, telefone, senha, aluno, professor)
    myCursor.execute(query, values)
    db.commit()  
    return True
#*******************************************Funcao de cadastramento de aluno no banco de dados ***********************************
# verificacao e insercao de dados em cadastro   
def insertCadastrarUsuario(cpf, nome,senha, user,nameLogin="", email=""):
    print(user)
    db = conn()
    myCursor = db.cursor()
    # verificacao de existencia de nome de usuario e cpf
    query = ""
    if user == "Aluno":
        query = "SELECT * FROM denis_TB_aluno WHERE NOME = '{}' OR CPF = '{}'".format(nome, cpf)
    else:
        query = "SELECT * FROM denis_TB_funcionario WHERE NOME = '{}' OR CPF = '{}' OR NOMELOGIN = '{}'".format(nome, cpf,nameLogin)
    print(query)
    myCursor.execute(query)
    resultado = myCursor.fetchall()
    if resultado != []:       
        return False    
    # insercao de dados caso esteja tudo ok   
    if user == 'Aluno':
        query = "INSERT INTO denis_TB_aluno (CPF, NOME,SENHA, ALUNO) VALUES (%s,%s, %s,%s)"
        values = (cpf, nome, senha, True)
    else:
        query = "INSERT INTO denis_TB_funcionario (CPF, NOME, NOMELOGIN, EMAIL, SENHA, FUNCIONARIO) VALUES (%s,%s, %s,%s, %s,%s)"
        values = (cpf, nome, nameLogin, email, senha, True)     
   
    myCursor.execute(query, values)
    db.commit()  
    return True
#********************************************************************************************************************************
#******************** verificação para logar no sistema *************************************************************************
def verifyUser(user, senha, userCheck):
    db = conn()
    myCursor = db.cursor()
    # verificacao de existencia de nome de usuario e cpf
    if userCheck == "Professor":
        user = user.lower()
        query = "SELECT * FROM denis_TB_funcionario WHERE NOMELOGIN = '{}' AND SENHA = '{}' AND FUNCIONARIO = {}".format(user, senha, 1)
    #else:
    #    user = user.replace('.','').replace('.','').replace('-','')
    #    query = "SELECT * FROM denis_TB_user_school WHERE CPF = '{}' AND SENHA = '{}' AND ALUNO = {}".format(user, senha, 1)
                
    myCursor.execute(query)
    resultado = myCursor.fetchone() 
    
    if resultado is None:
        return False  
    
    return resultado

#******************************* funcoes de tratamento de dados ******************************************************************
def verifyPassword(password, confirmPassword):
    if password != confirmPassword:
        return False
    return True

app.run()