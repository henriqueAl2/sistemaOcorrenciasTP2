USE sistemaOcorrencias;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE pesquisa;
TRUNCATE TABLE `Notificação`;
TRUNCATE TABLE alerta;
TRUNCATE TABLE Acompanhamento;
TRUNCATE TABLE Ocorrencia;
TRUNCATE TABLE tipoOcorrencia;
TRUNCATE TABLE Local;
TRUNCATE TABLE Usuario;

ALTER TABLE Usuario MODIFY COLUMN senha VARCHAR(255) NOT NULL;
ALTER TABLE Usuario MODIFY COLUMN tipo ENUM('admin', 'comum') NOT NULL;

SET @col_exists = (
    SELECT COUNT(*) 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_SCHEMA = DATABASE() 
      AND TABLE_NAME = 'Ocorrencia' 
      AND COLUMN_NAME = 'acessada_admin'
);
SET @sql_stmt = IF(@col_exists = 0, 'ALTER TABLE Ocorrencia ADD COLUMN acessada_admin TINYINT(1) NOT NULL DEFAULT 0;', 'SELECT 1;');
PREPARE stmt FROM @sql_stmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO Usuario (CPF, nome, email, senha, tipo) VALUES
('00000000000', 'Admin Geral', 'admin@sistema.com', '123456', 'admin'),
('11122233344', 'Carlos Silva', 'carlos@email.com', '123456', 'comum'),
('55566677788', 'Mariana Souza', 'mariana@email.com', '123456', 'comum');

INSERT INTO Local (codigo, endereco, latitude, longitude, imagem) VALUES
(101, 'Av. Paulista, 1000 - Bela Vista', '-23.564912', '-46.651984', NULL),
(102, 'Rua Augusta, 500 - Consolação', '-23.553120', '-46.658410', NULL),
(103, 'Av. Rebouças, 2100 - Pinheiros', '-23.562100', '-46.674200', NULL);

INSERT INTO tipoOcorrencia (idtipoOcorrencia, nome, descricao, Local_codigo) VALUES
(1, 'Buraco na via', 'Buraco em calçada ou asfalto', 101),
(2, 'Iluminação pública', 'Poste apagado ou piscando', 102),
(3, 'Descarte irregular', 'Acúmulo de lixo ou entulho', 103);

INSERT INTO Ocorrencia (idOcorrencia, tipo, descricao, data, hora, status, Usuario_CPF, Local_codigo, acessada_admin) VALUES
(1, 'Buraco na via', 'Buraco fundo na calçada', '2026-11-13', '2026-11-13 09:30:00', 'Aberta', '11122233344', 101, 0),
(2, 'Iluminação pública', 'Poste totalmente apagado', '2026-11-13', '2026-11-13 10:15:00', 'Em análise', '55566677788', 102, 1),
(3, 'Descarte irregular', 'Entulho bloqueando passagem', '2026-11-13', '2026-11-13 11:00:00', 'Aberta', '11122233344', 103, 0);

INSERT INTO Acompanhamento (idAcompanhamento, dataInicio, Usuario_CPF) VALUES
(1, '2026-11-13', '11122233344'),
(2, '2026-11-13', '55566677788');

INSERT INTO alerta (idalerta, mensagem, dataHora, lida, tipoOcorrencia_idtipoOcorrencia, Ocorrencia_idOcorrencia) VALUES
(1, 'Alerta: Novo buraco na Av. Paulista', '2026-11-13 09:31:00', 'nao', 1, 1),
(2, 'Alerta: Falha de luz na Rua Augusta', '2026-11-13 10:16:00', 'nao', 2, 2);

INSERT INTO `Notificação` (`idNotificação`, mensagem, dataHora, lida, Usuario_CPF) VALUES
(1, 'Ocorrência #1 registrada com sucesso.', '2026-11-13 09:30:05', 'nao', '11122233344'),
(2, 'Status da ocorrência #2: Em análise.', '2026-11-13 10:20:00', 'sim', '55566677788');

INSERT INTO pesquisa (idpesquisa, termoPesquisado, regiaoConsultada, dataHora, alerta_idalerta, `Notificação_idNotificação`) VALUES
(1, 'Buraco calçada', 'Bela Vista', '2026-11-13 09:45:00', 1, 1),
(2, 'Poste apagado', 'Consolação', '2026-11-13 10:30:00', 2, 2);

CREATE OR REPLACE VIEW vw_admin_usuarios AS
SELECT 
    CPF,
    nome,
    email,
    tipo
FROM Usuario;

CREATE OR REPLACE VIEW vw_admin_ocorrencias_locais AS
SELECT 
    o.idOcorrencia,
    o.tipo,
    o.descricao,
    o.data,
    o.hora,
    o.status,
    o.acessada_admin,
    u.CPF AS cpf_autor,
    u.nome AS nome_autor,
    l.codigo AS codigo_local,
    l.endereco,
    l.latitude,
    l.longitude,
    l.imagem
FROM Ocorrencia o
INNER JOIN Local l ON o.Local_codigo = l.codigo
INNER JOIN Usuario u ON o.Usuario_CPF = u.CPF;

CREATE OR REPLACE VIEW vw_admin_locais AS
SELECT 
    codigo,
    endereco,
    latitude,
    longitude,
    imagem
FROM Local;

CREATE OR REPLACE VIEW vw_usuario_minhas_ocorrencias AS
SELECT 
    o.idOcorrencia,
    o.tipo,
    o.descricao,
    o.data,
    o.hora,
    o.status,
    o.Usuario_CPF,
    l.endereco,
    l.latitude,
    l.longitude
FROM Ocorrencia o
INNER JOIN Local l ON o.Local_codigo = l.codigo;

CREATE OR REPLACE VIEW vw_alertas_sistema AS
SELECT 
    a.idalerta,
    a.mensagem,
    a.dataHora,
    t.nome AS tipo_ocorrencia,
    o.idOcorrencia,
    o.descricao AS descricao_ocorrencia,
    CASE 
        WHEN o.acessada_admin = 1 THEN 'sim'
        ELSE 'nao'
    END AS lida
FROM alerta a
INNER JOIN Ocorrencia o ON a.Ocorrencia_idOcorrencia = o.idOcorrencia
INNER JOIN tipoOcorrencia t ON a.tipoOcorrencia_idtipoOcorrencia = t.idtipoOcorrencia;

CREATE OR REPLACE VIEW vw_historico_pesquisas AS
SELECT 
    p.idpesquisa,
    p.termoPesquisado,
    p.regiaoConsultada,
    p.dataHora,
    a.mensagem AS alerta_relacionado,
    n.mensagem AS notificacao_relacionada
FROM pesquisa p
LEFT JOIN alerta a ON p.alerta_idalerta = a.idalerta
LEFT JOIN `Notificação` n ON p.`Notificação_idNotificação` = n.`idNotificação`;

CREATE OR REPLACE VIEW vw_notificacoes_usuario AS
SELECT 
    `idNotificação` AS id_notificacao,
    Usuario_CPF,
    mensagem,
    dataHora,
    lida
FROM `Notificação`;

CREATE OR REPLACE VIEW vw_acompanhamento_ocorrencias AS
SELECT 
    ac.idAcompanhamento,
    ac.dataInicio,
    u.CPF AS cpf_seguidor,
    u.nome AS nome_seguidor,
    o.idOcorrencia,
    o.tipo,
    o.descricao,
    o.status,
    l.endereco
FROM Acompanhamento ac
INNER JOIN Usuario u ON ac.Usuario_CPF = u.CPF
INNER JOIN Ocorrencia o ON o.Usuario_CPF = u.CPF
INNER JOIN Local l ON o.Local_codigo = l.codigo;

DROP PROCEDURE IF EXISTS sp_admin_acessar_ocorrencia;
DROP PROCEDURE IF EXISTS sp_acessar_notificacao;

DELIMITER $$

CREATE PROCEDURE sp_admin_acessar_ocorrencia(IN p_id_ocorrencia INT)
BEGIN
    UPDATE Ocorrencia 
    SET acessada_admin = 1 
    WHERE idOcorrencia = p_id_ocorrencia;
END $$

CREATE PROCEDURE sp_acessar_notificacao(IN p_id_notificacao INT)
BEGIN
    UPDATE `Notificação` 
    SET lida = 'sim' 
    WHERE `idNotificação` = p_id_notificacao;
END $$

DELIMITER ;

SELECT * FROM vw_admin_usuarios;
SELECT * FROM vw_admin_ocorrencias_locais;
SELECT * FROM vw_admin_locais;
SELECT * FROM vw_usuario_minhas_ocorrencias WHERE Usuario_CPF = '11122233344';
SELECT * FROM vw_alertas_sistema;
CALL sp_admin_acessar_ocorrencia(1);
SELECT * FROM vw_alertas_sistema;
SELECT * FROM vw_historico_pesquisas;
SELECT * FROM vw_notificacoes_usuario;
CALL sp_acessar_notificacao(1);
SELECT * FROM vw_notificacoes_usuario;
SELECT * FROM vw_acompanhamento_ocorrencias;