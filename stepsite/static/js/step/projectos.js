var row_index = null;
var form = document.forms[0].elements;

// {{url_for('addcategoria')}}

function SelectCategoria(id,nome){
    form.idCategoria.value= id;
    form.categoria.value= nome;
}

function AcaoCategoria(url,acao,valor){
    document.getElementById("btnSendCategoria").innerText=acao;
    let formC = document.forms["formCategoria"];
    formC.action = url;
    formC.elements.categoria.value=valor;
}

// Adicionar um atributo no link de confirmação para eliminar o registo
function fnIdselecionado(valor){
    document.getElementById("btnConfirm").setAttribute('href',valor)
}

// Pegar o indice da linha selecionada na tabela
$('td').mouseenter(function(){
    row_index = $(this).parent().index();
})


function fnAdicional(valor){
    let dataC = null
    if (valor[4]=="") 
        dataC = "..."
    else
        dataC = valor[4]

    let descricao = "<p> <strong>DESCRIÇÃO: </strong>"+valor[0]+"</p>"
    let categoria = "<p> <strong>CATEGORIA: </strong>"+valor[1]+"</p>"
    let entidade = "<p> <strong>ENTIDADE: </strong>"+valor[2]+"</p>"
    let estado = "<p> <strong>ESTADO: </strong>"+valor[3]+"</p>"
    let concluido = "<p> <strong>DATA DE CONCLUSÃO: </strong>"+dataC+"</p>"
    let entrega = "<p> <strong>DATA DE ENTREGA: </strong>"+valor[5]+"</p>"
    
    document.getElementById("divModal").innerHTML= descricao + categoria + entidade + estado + entrega + concluido
}
