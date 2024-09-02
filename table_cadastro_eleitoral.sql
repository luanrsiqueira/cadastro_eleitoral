CREATE TABLE CadastroEleitoral (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lider VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(255),
    bairro VARCHAR(100),
    celular VARCHAR(20),
    titulo_eleitoral VARCHAR(20),
    secao VARCHAR(20),
    zona_eleitoral VARCHAR(20),
    escolaridade VARCHAR(100),
    profissao VARCHAR(100),
    instagram VARCHAR(100),
    estado_civil VARCHAR(50),
    sexo VARCHAR (50)
    situacao_emprego VARCHAR(255),
    observacao TEXT,
    data_nascimento DATE NOT NULL,
    data_cadastro DATE NOT NULL
);
