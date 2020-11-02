$('#caixa').hide();
document.getElementById('closeAlert').onclick = ()=>{
    $('#caixa').hide();
}

// Área de Projectos
// Adicionar/Editar categorias
document.getElementById('btnSendCategoria').onclick = dsAjaxSendForm('formCategoria',comandoCategoria);

function comandoCategoria(rs){   
    vetor = Array(rs);
    if(vetor[0].success){
        document.location = document.URL;
    }
    else{
        $('#caixa').show();
        document.getElementById('caixa').setAttribute("class","alert alert-danger");
        document.getElementById('CaixaMsg').innerHTML = vetor[0].msg;
    }
    vetor = null;
}