# Sistema de gestão de projetos

## Objetivo: Automatizar o processo de gerenciamento de projetos. 

Pretende-se ter uma agenda que guardará informações relacionadas a cada projecto a ser desenvolvido, e uma área de lembretes informando os projetos em atraso. 

# Logo precisaremos das seguintes informações:

# Tipo de projecto
<ol>
<li></li>
Descrição do projecto
Entidade do projecto (informará a relação do projecto com uma determinada entidade, podendo ser um cliente ou uma disciplina relacionado com um professor)
Custo
Estado do projecto (‘concluído’, ‘em produção’,’prado’)
Data para concluir ( informa a data de limite para concluir um projecto)
Data de registo 
Data de conclusão 
Dias de trabalho ( informa os dias que tens de trabalhar em cada projecto )

</ol>
## Tabelas necessárias:
Usuário
Tipo de projecto
Entidade
Projectos 
Dias de trabalho

## Usuário* {
Id int,
Nome string,
Email string,
Senha string,
Imagem string 
}

## Tipo de Projeto* {
Id int,
Nome string,
IdUsuario int
}

## Entidade* {
Id int,
Nome string,
Contacto string,
Email,
IdUsuario 
}

## Projectos* {
Id int,
IdTipoProjeto int,
Descricao string,
Custos int,
Estado (‘concluído’, ‘em produção’,’prado’)
DataEntrega date, 
DataRegisto date,
DataConclusao date,
IdUsuario int,
IdEntidafe int
}

## Dias de trabalho* {
Id int,
IdProjecto int, 
Dia string,
Hora time,
}


## Gráfico de produtividade*
Projetos em riscos
Projectos em produção 
Projectos parados 
Total de projectos