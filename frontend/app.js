const backendURL = "http://127.0.0.1:8000";  

async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length === 0) {
        alert("Selecione um arquivo antes de enviar.");
        return;
    }

    const file = fileInput.files[0];  
    const formData = new FormData();
    formData.append("file", file);
    formData.append("filename", file.name);

    try {
        const response = await fetch(`${backendURL}/upload`, {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        updateTable();
        updateKeyboardLayout();

        document.getElementById("status").innerText = "Arquivo enviado: " + result.filename;
    } catch (error) {
        console.error("Erro ao enviar arquivo:", error);
        alert("Erro ao enviar o arquivo.");
    }
}


// Area de upload
function allowDrop(event) {
    event.preventDefault();
}

// Evento de soltar arquivos na area de uppload
function handleDrop(event) {
    event.preventDefault();
    const fileInput = document.getElementById('fileInput');
    fileInput.files = event.dataTransfer.files;
}

// Função para atualizar a tabela com novos dados
async function updateTable() {
    const response = await fetch('http://localhost:8000/inputs/');
    const data = await response.json();
    const resultTableBody = document.querySelector('#resultTable tbody');
  
    resultTableBody.innerHTML = '';
  
    data.forEach((entry, index) => {
      const row = document.createElement('tr');
      row.innerHTML = `<td>${index + 1}</td>
                       <td>${entry.filename || "Sem nome"}</td>
                       <td>${entry.character_count.a || 0}</td>
                       <td>${entry.character_count.b || 0}</td>
                       <td>${entry.character_count.c || 0}</td>
                       <td>${entry.character_count.ç || 0}</td>
                       <td>${entry.character_count.d || 0}</td>
                       <td>${entry.character_count.e || 0}</td>
                       <td>${entry.character_count.f || 0}</td>
                       <td>${entry.character_count.g || 0}</td>
                       <td>${entry.character_count.h || 0}</td>
                       <td>${entry.character_count.i || 0}</td>
                       <td>${entry.character_count.j || 0}</td>
                       <td>${entry.character_count.k || 0}</td>
                       <td>${entry.character_count.l || 0}</td>
                       <td>${entry.character_count.m || 0}</td>
                       <td>${entry.character_count.n || 0}</td>
                       <td>${entry.character_count.o || 0}</td>
                       <td>${entry.character_count.p || 0}</td>
                       <td>${entry.character_count.q || 0}</td>
                       <td>${entry.character_count.r || 0}</td>
                       <td>${entry.character_count.s || 0}</td>
                       <td>${entry.character_count.t || 0}</td>
                       <td>${entry.character_count.u || 0}</td>
                       <td>${entry.character_count.v || 0}</td>
                       <td>${entry.character_count.w || 0}</td>
                       <td>${entry.character_count.x || 0}</td>
                       <td>${entry.character_count.y || 0}</td>
                       <td>${entry.character_count.z || 0}</td>`;
  
      resultTableBody.appendChild(row);
    });
}

async function updateKeyboardLayout() {
    try {
        const response = await fetch(`${backendURL}/layout/`);
        const layoutData = await response.json();
        

        console.log(layoutData)
        const keyboardContainer = document.querySelector('.keyboard-container');
        const rows = keyboardContainer.querySelectorAll('.row');
        
        if (!layoutData.matrix || layoutData.matrix.length !== rows.length) {
            console.error("Erro: matriz inválida no layout.json");
            return;
        }
        
        rows.forEach((row, rowIndex) => {
            const buttons = row.querySelectorAll('button');
            if (layoutData.matrix[rowIndex].length !== buttons.length) {
                console.error(`Erro: número de teclas na linha ${rowIndex} não corresponde ao layout.json`);
                return;
            }
            
            buttons.forEach((button, buttonIndex) => {
                button.innerText = layoutData.matrix[rowIndex][buttonIndex];
            });
        });
    } catch (error) {
        console.error("Erro ao atualizar o layout do teclado:", error);
    }
}


updateTable()