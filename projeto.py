import sqlite3  # IMPOTANDO O BANCO DE DADOS
from tabulate import tabulate # IMPORTANDO A BIBLIOETECA tabulate PARA CRIAÇÃO DA TABELA DO CRONOGRAMA 
from time import sleep # IMPORTANDO A BIBLIOETECA time PARA USAR O TEMPORIZADOR sleep
from datetime import datetime # IMPORTANTO A BIBLIOETCA datetime PARA TRATAR DATAS E HORARIOS.

# CORES PARA APLICAR NO TERMINAL
red='\033[31m'
RESET = '\033[0m'
GREEN = '\033[32m'
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

def remover_acentos(txt):   # FUNÇÃO PARA REMOVER OS ACENTOS DE PALAVRAS ( O QUE VAI AJUDAR NOS FILTROS DE BUSCA E EDIÇÃO.)

    com= "áàâãäéèêëíìîïóòôõöúùûü"
    sem="aaaaaeeeeiiiiooooouuuu"
    tabela=str.maketrans(com + com.upper(), sem+sem.upper())  # CRIA UMA TABELA DE TRADUÇÃO ONDE CADA CARACTERE É MAPEADO PARA SUA VERSÃO SEM ACENTO.

    return txt.translate(tabela) # FAZ A CONVERSAO COM BASE NA TABELA, SUBSTITUINDO OS CARACTERES CONFORME DEFINIDO.



def menu(lista):  # FUNÇÃO PARA CRIAÇÃO DE MENU DE OPÇÕES.
    c=1
    for opção in (lista):
        print(f'{c} - {opção}')
        c+=1
    print()
    opção = input('Sua opção: ').strip()
    return opção


# PARTE DE CADASTRAMENTO DE USUARIO E LOGIN.

# CRIANDO UM BANCO DE DADOS PARA CADASTRAR OS DADOS DE CADASTRAMENTO DO USUARIO.
conexao=sqlite3.connect('cadastramento.db')
cursor=conexao.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, email TEXT NOT NULL UNIQUE, senha TEXT NOT NULL)''')
conexao.commit()

def cadastro():  # FUNÇÃO PARA CADASTRAMENTO DE USUARIO.
    while True:
     nome = input("NOME: ").lower()
     email = input("EMAIL: ").lower()
     senha = input("SENHA: ").lower()   
     while len(senha) < 8:                 
      senha=input(red+'SUA SENHA PRECISA CONTER NO MINIMO 8 CARACTERES.\nDIGITE UMA NOVA SENHA: '+RESET)

     cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,)) # EXECUTA UMA CONSULTA NO BANCO DE DADOS PARA SELECIONAR TODAS AS LINHAS DO BANCO DE DADOS DENOMINADO 'usuarios' ONDE O CAMPO 'email' SEJA IGUAL AO EMAIL FORNECIDO.

     if cursor.fetchone(): # A FUNÇÃO fetchone() É USADA PARA OBTER A PRIMEIRA LINHA DO RESULTADO DA CONSULTA ANTERIOR. SE fetchone() RETORNAR ALGUM VALOR, ISSO SIGNIFICA QUE JA EXISTE UM USUARIO COM O MESMO EMAIL NO BANCO DE DADOS.

        print(red+f'O EMAIL ({email}) JÁ PERTENCE A OUTRO USUARIO. TENTE OUTRO...'+RESET) 

        # CASO O EMAIL NAO  ESTEJA JA NA LISTA, ELE VAI CADASTRAR O USUARIO, DESTA FORMA:
     else:
            cursor.execute("INSERT INTO usuarios (nome,email,senha) VALUES(?,?,?)",(nome,email,senha))   
            conexao.commit()
            print(GREEN+'USUARIO CADASTRADO COM SUCESSO!'+RESET)  
            break
    print()

def login(): # FUNÇÃO DE LOGIN DO USUARIO.
    while True:
        email= input('SEU EMAIL: ').lower()
        senha = input('SUA SENHA: ').lower()

        # VERIFICA TODOS OS EMAILS E SENHAS DO BANCO DE DADOS
        cursor.execute("SELECT * FROM usuarios WHERE email=? and senha=?",(email,senha))
        if cursor.fetchone():   # SE O EMAIL E A SENHA CONSTAR NO BANCO DE DADOS, ELE REALIZA O LOGIN.
            print(GREEN+'LOGIN REALIZADO!'+RESET)
            return email
            break
        else:  # SE O RESULTADO DO fetchone() FOR None ISSO SIGNIFICA QUE NÃO CONSTA OS DADOS FORNECIDOS PELO USUARIO NO BANCO DE DADOS.
            print(red+'EMAIL OU SENHA INCORRETOS!'+RESET)  

# CRIANDO UM BANCO DE DADOS PARA CADA USUARIO.    

def banco_unico(email):  # FUNÇÃO PARA CRIAR UM BANCO DE DADOS PARA CADA USUARIO DIFERENTE.
    banco = f'{email}_dados.db' # CRIANDO UM BANCO DE DADOS APARTIR DO EMAIL DO USUARIO ( QUE É UNICO )
    conexao_usuario = sqlite3.connect(banco)   # CRIANDO UMA CONEXÃO DO sqlite3 COM O BANCO DE DADOS.
    cursor_usuario = conexao_usuario.cursor()  # CRIANDO UM CURSOR 
    cursor_usuario.execute('''CREATE TABLE IF NOT EXISTS dados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        informacao TEXT NOT NULL)''')   # CRIANDO UMA TABELA SE AINDA NÃO EXISTIR DENOMINADA DADOS PARA ADICIONAR OS DADOS DE CADA USUARIO.
    conexao_usuario.commit()   # SALVANDO A CRIAÇÃO DA TABELA 
     

#  PROGRAMA PRINCIPAL 

print('╔═══════════════════════════════════════╗')
print('║  BEM VINDO AO CRONOGRAMA DE ESTUDOS   ║')         # CABEÇALHO
print('╚═══════════════════════════════════════╝')
while True:    # OPÇÃO DO USUARIO ESCOLHER SE ELE DESEJA SE CADASTRAR OU FAZER LOGIN 
    direçao=' '  
    while direçao not in '1' or direçao in '2':
         direçao=menu(['LOGIN', 'CADASTRO'])
         if direçao in '1' or direçao in '2':
             break
    if direçao == '1':     # SE ELE PREFERIR FAZER O LOGIN:
        print('╔══════════════════════════════╗')
        print('║            LOGIN             ║')
        print('╚══════════════════════════════╝')
        email_usuario=login() # CHAMANDO A FUNÇÃO LOGIN A PARTIR DA VARIAVEL email_usuario PARA QUE OS DADOS DE LOGIN SERA ATRIUIDOS A ESSA VARIAVEL 
        banco_unico(email_usuario) 
        print()
    if direçao == '2':   # SE ELE AINDA NÃO FOR USUARIO CADASTRADO.

        print('╔══════════════════════════════╗')
        print('║          CADASTRO            ║')
        print('╚══════════════════════════════╝')
        cadastro()  # CHAMANDO A FUNÇAO cadastro()

        # EM SEGUIDA CHAMANDO A TELA DE LOGIN PARA QUE O USUARIO RECEM CADASTRADO POSSA REALIZAR SEU LOGIN
        print('╔══════════════════════════════╗')
        print('║            LOGIN             ║')
        print('╚══════════════════════════════╝')
        email_usuario=login() ## CHAMANDO A FUNÇÃO LOGIN A PARTIR DA VARIAVEL email_usuario PARA QUE OS DADOS DE LOGIN SERA ATRIUIDOS A ESSA VARIAVEL 
        banco_unico(email_usuario) # ADICIOANDO OS DADOS DO LOGIN A FUNÇÃO banco_unico FAZENDO COM ELA CRIE UM BANCO DE DADOS PARA AQUELE USUARIO.
        print()

    print(BOLD+'          BEM VINDO!    '+RESET)     # INTERAÇÃO DO PROGRAMA INICIAL APÓS LOGIN
    
    # PROGRAMA PRINCIOAL 

    while True:
        print('╔══════════════════════════════╗')
        print('║            MENU              ║')
        print('╚══════════════════════════════╝')
        ops =menu(['CRIAR CRONOGRAMA', 'VISUALIZAR CRONOGRAMA', 'EDITAR CRONOGRAMA','SAIR'])  # CRIANDO UM MENU DE OPÇÕES.
        print()
        # OPERANDO COM BASE NA ESCOLHA DO USUARIO:
        if ops == '1': # SE ELE PREFERIR CRIAR UM CONOGRAMA DO 0 OU ADICIONAR AO CONOGRAMA.
            print('╔══════════════════════════════╗')
            print('║     CRIANDO CRONOGRAMA       ║')
            print('╚══════════════════════════════╝')
            try:
                titulo = input('Título: ').capitalize().strip()   # TITULO DA ATIVIDADE
                descriçao = input('Descrição: ').capitalize().strip()   # DSECRIÇÃO DA ATIVIDADE

                while True:  # CRIANDO UM LOOP PARA A INCLUSAO DA DATA DE INICIO
                 hoje=datetime.today().date()  # ATRIBUINDO A DATA DO DIA PARA A VARIAVEL DENOMINADA "HOJE"
                 data = input('Data de início (dd/mm/aaaa) : ').strip()   # DATA DE INICIO DA ATIVIDADE
                 try:
                     data_inicio = datetime.strptime(data, '%d/%m/%Y').date()  # VERIFICANDO SE A DATA FORNECIDA PELO USUARIO ESTÁ NO FORMATO CORRETO E ADICIONANDO ELA A VARIAVEL DENOMINADA "data_inicio".
                     if data_inicio < hoje: # VERIFICANDO SE A DATA DE INICIO É MENOR QUE A DATA ATUAL
                         print(red+f'A DATA DE INICIO NÃO PODE SER MENOR QUE A DATA DE HOJE.'+RESET)  # SE FOR MENOR...
                         print(red+f'DATA DE HOJE: {hoje}'+RESET)   # INFORMANDO A DATA ATUAL PARA CITUAR O USUARIO
                         
                     else:  # SE NÃO FOR MENOR...
                            break
                    
                 except ValueError:  # SE A DATA FORNECIDA PELO USUARIO NÃO ESTIVER NO FORMATO DESEJADO
                     print("Data inválida! Por favor, insira no formato dd/mm/aaaa.") # INTERAÇÃO COM O USUARIO

                while True: # CRIANDO UM LOOP PARA O PRAZO
                  prazo = input('Prazo (dd/mm/aaaa) : ').strip() # PRAZO DE CONCLUSÃO DA ATIVIDADE
                  try:
                    data_prazo=datetime.strptime(prazo,'%d/%m/%Y').date() # VERIFICANDO SE O PRAZO FORNECIDO PELO USUARIO ESTA NO FORMATO DESEJADO (DD/MM/AAAA).
                    if data_prazo < data_inicio: # VERIFICANDO SE O PRAZO É MENOR QUE A DATA DE INICIO
                        print(red+'O PRAZO NÃO PODE SER MENOR DO QUE A DATA DE INICIO.'+RESET) # INFORMANDO QUE O PRAZO NÃO PODE SER MENOR QUE A DATA DE INICIO.
                    else:
                        break
                  except ValueError: # INFORMANDO AO USUARIO QUE A DATA NÃO ESTA NO FORMATO DESEJADO (DD/MM/AAAA)
                    print(red+'DATA INVALIDA! POR FAVOR, DIGITE UM PRAZO VALIDO NO FORMATO (dd/mm/aaaa)'+RESET)     

                while True:   # LOOP PARA O HORARIO DE INICIO
                  horarioini = input('HÓRARIO (ex: 14:00) : ' ).strip()
                  try:
                    horario_formatado=datetime.strptime(horarioini,'%H:%M') # VERIFICANDO SE O HORARIO FORNECIDO PELO USUARIO ESTA NO FORMADO DESEJADO (HH:MM)
                    break
                  except ValueError:
                        print(red+"Horário inválido! Por favor, insira no formato HH:MM."+RESET) # INFORMANDO PARA O USUARIO QUE O FORMATO DO HORARIO NÃO ESTA NO FORMATO DESEJADO (HH:MM)
                while True: # LOOP PARA O HORARIO FINAL
                    horariofim=input('HORÁRIO FINAL (ex: 15:00) : ').strip()
                    try:
                        horario_formatado2=datetime.strptime(horariofim,'%H:%M') # VERIFICANDO SE O HORARIO FORNECIDO PELO USUARIO ESTA NO FORMADO DESEJADO (HH:MM)
                        if horario_formatado2 < horario_formatado : # ANALIZANDO SE O HORARIO FORNECIDO PELO USUARIO É MENOR QUE O HORARIO INICIAL
                            print(red+'O HORÁRIO FINAL NÃO PODE SER MENOR QUE O INICIAL.'+RESET) # INFORMANDO AO USUARIO
                        else:
                            break
                    except ValueError:
                          print(red+"Horário inválido! Por favor, insira no formato HH:MM."+RESET) # INFORMANDO AO USUARIO QUE O HORARIO FORNECIDO NÃO ESTA NO FORMATO DESEJADO (HH:MM)



                prioridade = input('Nível de prioridade (alto/medio/baixo): ').capitalize().strip() # NIVEL DE PRIORIDADE DA ATIVIDADE
                
            # CRIANDO UMA CONEXAO COM O BANCO DE DADOS PARA A INSERIR TODOS OS DADOS FORNECIDOS ANTERIOMENTE.
                banco = sqlite3.connect(f'{email_usuario}.db') # CRIANDO UM BANCO DE DADOS UNICO APARTIR DO EMAIL DO USUARIO
                cursor = banco.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS estudos (titulo text, descriçao text, data text, prazo text, horario text, horario_fim text,  prioridade text)")
                  # CRIANDO UM BANCO DE DADOS CASO AINDA NÃO EXISTA
                cursor.execute("INSERT INTO estudos (titulo, descriçao, data, prazo, horario, horario_fim, prioridade) VALUES (?, ?, ?, ?, ?, ?, ?)", (remover_acentos(titulo), descriçao, data_inicio.strftime('%d/%m/%Y'), data_prazo.strftime('%d/%m/%Y'), horario_formatado.strftime('%H:%M'),horario_formatado2.strftime('%H:%M'),prioridade)) # ADICIONANDO AS VARIAVEIS AO CONOGRAMA
                banco.commit() # ADICIONANDO...
                print()
                print(GREEN+f"Atividade denominada {titulo.upper()} cadastrada com sucesso!"+RESET)   # INTERAÇÃO COM O USUARIO!
                print()
            
            except sqlite3.Error as erro:  # TRATAMENTO DE ERRO.
                print("Erro ao inserir dados no banco de dados:", erro)    
            
            finally:   # FINALIZANDO A EXECUÇÃO. 
                if banco:
                    banco.close()  # FECHANDO O BANCO.

        elif ops == '2': # SE ELE PREFERIR VIZUALIZAR O CRONOGRAMA
            try:        
                print(f'╔══════════════════════════════╗'.center(110))
                print(BOLD+f'║         CRONOGRAMA           ║'.center(110)+RESET)    # CABECALHO
                print(f'╚══════════════════════════════╝'.center(110))
                banco = sqlite3.connect(f'{email_usuario}.db') # CRIANDO CONEXÃO COM O BANCO DO USUARIO
                cursor = banco.cursor()
                cursor.execute("SELECT * FROM estudos") # PARA SELECIONAR TUDO DO BANCO
                tupla = cursor.fetchall() # ADICIONANDO TODOS OS DADOS DO BANCO A UMA VARIAVEL
                cabecalho=[BOLD+'Título', 'Descrição', 'Data Início', 'Prazo', 'Horário Inicial','Horário Final', 'Nível de Prioridade'+RESET] # CRIANDO UM CABEÇALHO PARA A TABELA DO CRONOGRAMA 
                print(tabulate(tupla, headers=cabecalho, tablefmt="fancy_grid")) # USANDO A BIBLIOTECA TABULATE PARA CRIA UMA TABELA COM OS DADOS 

                # INTERÇÃO COM O USUARIO.

                print()
                print('╔══════════════════════════════╗')
                print('║   SELECIONE UM DAS OPÇÕES    ║')
                print('╚══════════════════════════════╝')
                opc2=menu(['FILTRAR ATIVIDADES','VOLTAR PARA O MENU','SAIR'])   # MENU 
                print()


                # FILTROS DE BUSCA.
                # MENU DOS FILTROS
                if opc2 == '1':
                    print('╔══════════════════════════════╗')
                    print('║   SELECIONE UM DAS OPÇÕES    ║')
                    print('╚══════════════════════════════╝')
                    opc3=menu(['FILTRAR POR PRIORIDADE','FILTRAR POR PRAZO', 'FILTRAR POR TÍTULO','SAIR']) # MENU DOS FILTROS
                    print()
                    if opc3=='1': # SE O USUARIO PREFERIR FILTRAR PELO NIVEL DE PRIORIDADE.
                        nivel=input('DIGITE O NIVEL DE PRIORIDAE QUE DESEJA FILTRAR: ').capitalize().strip() 
                        nivel=remover_acentos(nivel)
                        print()
                        banco=sqlite3.connect(f'{email_usuario}.db')
                        cursor=banco.cursor()
                        query = """
                        SELECT * FROM estudos
                        WHERE prioridade =? """    # SELECIONANDO TODAS AS ATIVIDAES COM O NIVEL DE PRIORIDADE DESEJADA E ADICIONANDO A UMA VARIAVEL.
                        cursor.execute(query,(nivel,)) 
                        resultados=cursor.fetchall()
                        print(f'                                    ATIVIDADES COM NIVEL DE  PRIORIDADE: {nivel.upper()}              ')
                        print(tabulate(resultados,headers=cabecalho,tablefmt="fancy_grid"))  # FORMAÇÃO DA TABELA 
                    banco.close()       
                    if opc3=='2': # SE O USUARIO PREFERIR FILTRAR PELO PRAZO
                        prazos=input('DIGITE O PRAZO QUE DESEJA FILTAR: ').capitalize().strip()
                        print()
                        banco=sqlite3.connect(f'{email_usuario}.db')
                        cursor=banco.cursor()
                        query=''' SELECT * FROM estudos WHERE prazo =?'''   # SELECIONANDO TODAS AS ATIVIDAES COM O PRAZO DESEJADAO E ADICIONANDO A UMA VARIAVEL.
                        cursor.execute(query,(prazos,))
                        resultados2=cursor.fetchall()
                        print(f'                         ATIVIDADES COM PRAZO: ({prazos})                                   ')
                        print(tabulate(resultados2,headers=cabecalho,tablefmt='fancy_grid'))
                    banco.close()
                    if opc3 =='3':  # SE O USUARIO PREFERIR FILTRAR PELO TITULO
                        tit=input('DIGITE O TITULO QUE  DESEJA FILTRAR:  ').capitalize().strip() 
                        tit=remover_acentos(tit)
                        print()
                        banco=sqlite3.connect(f'{email_usuario}.db') 
                        cursor=banco.cursor()
                        query='''SELECT * FROM estudos WHERE titulo=?''' # SELECIONANDO TODAS AS ATIVIDAES COM O TITULO DESEJADAO E ADICIONANDO A UMA VARIAVEL.
                        cursor.execute(query,(tit,))
                        resultados3=cursor.fetchall()
                        print(f'                        ATIVIDADES COM TÍTULO: {tit.upper()}                                ')
                        print(tabulate(resultados3,headers=cabecalho,tablefmt='fancy_grid'))  
                    banco.close()    
                if opc2 == '2':  # VOLTANDO PRO MENU
                    continue
                if opc2 == '3':   # ENCERRANDO O PROGRAMA.
                        print('ENCERRANDO PROGRAMA...')
                        sleep(1.5)
                        print('PROGRAMA ENCERRADO, ATÉ LOGO!')   
                        break  
                                            
            except sqlite3.Error as erro:  # TRATAMENTO DE ERRO
                print(f'Erro ao visualizar o cronograma: {erro}')

            finally:   # FINALIZANDO A EXECUÇÃO
                if banco:
                    banco.close()  #  FECHANDO O BANCO


        elif ops == '3':   # SE O USUARIO PREFERIR EXCLUIR OU EDITAR ALGO DA TABELA.
            print('╔══════════════════════════════╗')
            print('║      EDITAR CRONOGRAMA       ║')
            print('╚══════════════════════════════╝')
            escolha=menu(['EXCLUIR','EDITAR'])
            # SE ELE ESCOLHER EXCLUIR: 
            print()
            if escolha == '1':
                excluir = input('QUAL ATIVDADE DESEJA EXCLUIR? ').capitalize().strip()
                excluir=remover_acentos(excluir)
                print()
                excluir1=excluir.capitalize().strip() # TRANSFORMANDO A FORMA DE RECEBIMENTO DA RESPOSTA
                try:
                    banco = sqlite3.connect(f'{email_usuario}.db')  # SE CONECTANDO COM O BANCO
                    cursor = banco.cursor()
                    cursor.execute("DELETE FROM estudos WHERE titulo = ?", (excluir1,)) # EXCLUINDO O QUE O USUARIO DESEJA
                    banco.commit()
                    if cursor.rowcount > 0: # SE O PROGRAMA FOR BEM EXECUTADO:
                        print(f'EXCLUINDO A ATIVIDADE: {excluir.upper()}...')
                        sleep(1.5)
                        print(GREEN+'ATIVIDADE REMOVIDA!'+RESET)
                        print()    
                    else: # SE NÃO TIVER ESSA ATIVIDADE DIGITADA 
                        print(red+'ATIVIDADE NÃO ENCONTRADA!'+RESET)
                
                except sqlite3.Error as erro:   #TRATAMENTO DE ERRO
                    print(f'Erro ao excluir: {erro}')
                
                finally:   #  FINALIZANDO A EXECUÇÃO
                    if banco:
                        banco.close()    # FECHANDO O BANCO
            elif escolha == '2':     # SE ELE ESCOLHER EDITAR
                atividade = input('QUAL ATIVIDADE DESEJA EDITAR? ').capitalize().strip()
                atividade=remover_acentos(atividade)
            
                try:
                    banco = sqlite3.connect(f'{email_usuario}.db')  # SE CONECTANDO COM O BANCO
                    cursor = banco.cursor()
                    # VERIFICAR SE A ATIVIDADE EXISTE NO BANCO
                    cursor.execute("SELECT * FROM estudos WHERE titulo = ?", (atividade,))
                    dados = cursor.fetchone()
                    # SE A ATIVIDADE EXISTIR NO BANCO:
                    if dados:
                        print('╔══════════════════════════════════════════════════════════════════════════════╗')
                        print('║Campos disponíveis para edição: Título, Descrição, Data, Horário e Prioridade.║')
                        print('╚══════════════════════════════════════════════════════════════════════════════╝')
                        campo = input('QUAL CAMPO DESEJA EDITAR? ').lower().strip()
                        campo=remover_acentos(campo)
                        editar = input('DIGITE A EDIÇÃO: ')
                        editar1=editar.capitalize().strip()
                        # PARA ATUALIZAR A EDIÇÃO:
                        cursor.execute(f"UPDATE estudos SET {campo} = ? WHERE titulo = ?", (editar1, atividade))
                        banco.commit()
                        print(f'EDITANDO O CAMPO {campo.upper()} DA ATIVIDADE {atividade.upper()} PARA {editar.upper()}.')
                        sleep(1.5)
                        print(GREEN+'ATIVIDADE EDITADA!'+RESET)
                    else:           # CASO ATIVIDADE DIGITADA NÃO EXISTA
                        print(red+'ATIVIDADE NÃO ENCONTRADA!'+RESET)
                
                except sqlite3.Error as erro:   # TRATAMENTO DE ERRO
                    print(f'Erro ao editar: {erro}')
                
                finally:                   # FINALIZANDO A EXEUÇÃO 
                    if banco:
                        banco.close()          # FECHANDO A CONEXÃO COM O BANCO
                        
        if ops == '4':  # SE O USUARIO PREFERIR ENCERRAR O PROGRAMA.
            print('ENCERRANDO PROGRAMA...')
            sleep(1.5)
            print('PROGRAMA ENCERRADO, ATÉ LOGO!')     
            break
    break
