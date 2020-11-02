    var row_index = null;
    var form = document.forms[1].elements;
    var oldUrl = null;
    
    // Pegar o indice da linha selecionada na tabela
    $('td').mouseenter(function(){
        row_index = $(this).parent().index()+1;
    })
    
    // Adicionar um atributo no link de confirmação para eliminar o registo
    function fnIdselecionado(valor){
        document.getElementById("btnConfirm").setAttribute('href',valor)
    }
    
    function PassarDados(newUrl){
        document.getElementById("btnCancelar").setAttribute('class','btn btn-danger visible')
        let tabela = document.getElementById('tbEntidades').rows;
        oldUrl = document.forms[1].action;
        document.forms[1].action = form.action = newUrl;
    
        form.nome.value = tabela[row_index].cells[1].innerHTML;
        form.email.value = tabela[row_index].cells[2].innerHTML;
        form.contacto.value = tabela[row_index].cells[3].innerHTML;
        form.submit.value = "Actualizar";
     }
    
     $("#btnCancelar").click(function(){
         document.forms[1].action = oldUrl
        form.submit.value = "Adicionar"; 
        document.getElementById("btnCancelar").setAttribute('class','btn btn-danger hidden')
     })
