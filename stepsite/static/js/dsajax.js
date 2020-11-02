function dsAjaxSendForm(id_Formulario, instrucao){
    document.getElementById(id_Formulario).onsubmit = (e)=>{
        e.preventDefault();

        // Pegar o Formulário pelo Id inserido
        let form = document.getElementById(id_Formulario)
       
        // Declaração da variavel que efectuará o pedido
        let pedido = new XMLHttpRequest();

        // Função a ser executada quando o pedido estiver pronto
        pedido.onreadystatechange=()=>{
            // Instrucoes a serem executadas
            if(pedido.readyState==4 && pedido.statusText=="OK"){
                let data = JSON.parse(pedido.responseText)
                instrucao(data);
            }
            // Caso a pedido nao for encontrado
            else if(pedido.status==404){
                alert("Requisição não encontrada");
            }
        }
        
        const data = new FormData(form);
        // Preparar o pedido
        pedido.open(form.method,form.action,true);
        // Enviar o pedido
        pedido.send(data);
    }
}