# Gerenciador de Atividades desenvolvido na linguagem python.
Este projeto é um sistema simples de gerenciamento de atividades com foco em usabilidade e segurança. O objetivo principal é permitir que os usuários cadastrem e gerenciem suas atividades de maneira eficiente, com funcionalidades como criação de contas, autenticação, adição de atividades, e visualização em cronograma.

Funcionalidades
Cadastro de Usuários:

Criação de contas com nome e senha.
Armazenamento seguro de dados.
Login para acessar a conta.
Cadastro e Gerenciamento de Atividades:

Adicionar, editar e excluir atividades.
Cada atividade possui título, descrição, data de início, prazo, horário e prioridade.
Validação de Prazos e Horários:

Validação para garantir que a data de início seja anterior ao prazo de conclusão.
Visualização em Cronograma:

Interface para visualizar atividades em um cronograma (diário, semanal ou mensal).
Classificação e Filtro por Prioridade:

Permite ao usuário visualizar atividades com base no nível de prioridade.
Requisitos Funcionais
Cadastro de Usuário: Sistema para cadastro e login de usuários.
Gerenciamento de Atividades: Função para adicionar, editar e excluir atividades.
Validação de Prazos e Horários: Garantia de que os prazos não sejam conflitantes.
Visualização de Atividades: Exibição de atividades organizadas por data e horário.
Prioridade: Filtro para mostrar atividades com maior prioridade.
Requisitos Não Funcionais
Usabilidade: Interface simples e intuitiva.
Segurança: Senhas armazenadas de forma segura (uso de hash).
Persistência de Dados: Armazenamento de dados usando SQLite ou arquivos de texto.
Backup de Dados: Função para backup de dados para garantir a recuperação.
