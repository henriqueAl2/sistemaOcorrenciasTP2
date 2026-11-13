-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema sistemaOcorrencias
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sistemaOcorrencias
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sistemaOcorrencias` DEFAULT CHARACTER SET utf8 ;
USE `sistemaOcorrencias` ;

-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`Usuario` (
  `CPF` VARCHAR(11) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(6) NOT NULL,
  `tipo` ENUM("admin", "user") NULL,
  PRIMARY KEY (`CPF`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`Local`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`Local` (
  `codigo` INT NOT NULL,
  `endereco` VARCHAR(150) NULL,
  `latitude` VARCHAR(45) NULL,
  `longitude` VARCHAR(45) NULL,
  `imagem` LONGBLOB NULL,
  PRIMARY KEY (`codigo`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`Ocorrencia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`Ocorrencia` (
  `idOcorrencia` INT NOT NULL,
  `tipo` VARCHAR(45) NULL,
  `descricao` VARCHAR(255) NULL,
  `data` DATE NULL,
  `hora` DATETIME NULL,
  `status` VARCHAR(45) NULL,
  `Usuario_CPF` VARCHAR(11) NOT NULL,
  `Local_codigo` INT NOT NULL,
  PRIMARY KEY (`idOcorrencia`),
  INDEX `fk_Ocorrencia_Usuario_idx` (`Usuario_CPF` ASC) VISIBLE,
  INDEX `fk_Ocorrencia_Local1_idx` (`Local_codigo` ASC) VISIBLE,
  CONSTRAINT `fk_Ocorrencia_Usuario`
    FOREIGN KEY (`Usuario_CPF`)
    REFERENCES `sistemaOcorrencias`.`Usuario` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Ocorrencia_Local1`
    FOREIGN KEY (`Local_codigo`)
    REFERENCES `sistemaOcorrencias`.`Local` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`tipoOcorrencia`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`tipoOcorrencia` (
  `idtipoOcorrencia` INT NOT NULL,
  `nome` VARCHAR(45) NULL,
  `descricao` VARCHAR(255) NULL,
  `Local_codigo` INT NOT NULL,
  PRIMARY KEY (`idtipoOcorrencia`),
  INDEX `fk_tipoOcorrencia_Local1_idx` (`Local_codigo` ASC) VISIBLE,
  CONSTRAINT `fk_tipoOcorrencia_Local1`
    FOREIGN KEY (`Local_codigo`)
    REFERENCES `sistemaOcorrencias`.`Local` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`alerta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`alerta` (
  `idalerta` INT NOT NULL,
  `mensagem` VARCHAR(45) NULL,
  `dataHora` DATETIME NULL,
  `lida` ENUM("sim", "nao") NULL,
  `tipoOcorrencia_idtipoOcorrencia` INT NOT NULL,
  `Ocorrencia_idOcorrencia` INT NOT NULL,
  PRIMARY KEY (`idalerta`),
  INDEX `fk_alerta_tipoOcorrencia1_idx` (`tipoOcorrencia_idtipoOcorrencia` ASC) VISIBLE,
  INDEX `fk_alerta_Ocorrencia1_idx` (`Ocorrencia_idOcorrencia` ASC) VISIBLE,
  CONSTRAINT `fk_alerta_tipoOcorrencia1`
    FOREIGN KEY (`tipoOcorrencia_idtipoOcorrencia`)
    REFERENCES `sistemaOcorrencias`.`tipoOcorrencia` (`idtipoOcorrencia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_alerta_Ocorrencia1`
    FOREIGN KEY (`Ocorrencia_idOcorrencia`)
    REFERENCES `sistemaOcorrencias`.`Ocorrencia` (`idOcorrencia`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`Notificação`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`Notificação` (
  `idNotificação` INT NOT NULL,
  `mensagem` VARCHAR(45) NULL,
  `dataHora` DATETIME NULL,
  `lida` ENUM("sim", "nao") NULL,
  `Usuario_CPF` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`idNotificação`),
  INDEX `fk_Notificação_Usuario1_idx` (`Usuario_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_Notificação_Usuario1`
    FOREIGN KEY (`Usuario_CPF`)
    REFERENCES `sistemaOcorrencias`.`Usuario` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`pesquisa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`pesquisa` (
  `idpesquisa` INT NOT NULL,
  `termoPesquisado` VARCHAR(45) NULL,
  `regiaoConsultada` VARCHAR(45) NULL,
  `dataHora` DATETIME NULL,
  `alerta_idalerta` INT NOT NULL,
  `Notificação_idNotificação` INT NOT NULL,
  PRIMARY KEY (`idpesquisa`),
  INDEX `fk_pesquisa_alerta1_idx` (`alerta_idalerta` ASC) VISIBLE,
  INDEX `fk_pesquisa_Notificação1_idx` (`Notificação_idNotificação` ASC) VISIBLE,
  CONSTRAINT `fk_pesquisa_alerta1`
    FOREIGN KEY (`alerta_idalerta`)
    REFERENCES `sistemaOcorrencias`.`alerta` (`idalerta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pesquisa_Notificação1`
    FOREIGN KEY (`Notificação_idNotificação`)
    REFERENCES `sistemaOcorrencias`.`Notificação` (`idNotificação`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`Acompanhamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`Acompanhamento` (
  `idAcompanhamento` INT NOT NULL,
  `dataInicio` DATE NULL,
  `Usuario_CPF` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`idAcompanhamento`, `Usuario_CPF`),
  INDEX `fk_Acompanhamento_Usuario1_idx` (`Usuario_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_Acompanhamento_Usuario1`
    FOREIGN KEY (`Usuario_CPF`)
    REFERENCES `sistemaOcorrencias`.`Usuario` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `sistemaOcorrencias`.`AlertaRegiao`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sistemaOcorrencias`.`AlertaRegiao` (
  `idAlertaRegiao` INT NOT NULL,
  `latitudeCentro` VARCHAR(45) NULL,
  `longitudeCentro` VARCHAR(45) NULL,
  `raioKM` INT NULL,
  `Usuario_CPF` VARCHAR(11) NOT NULL,
  PRIMARY KEY (`idAlertaRegiao`),
  INDEX `fk_AlertaRegiao_Usuario1_idx` (`Usuario_CPF` ASC) VISIBLE,
  CONSTRAINT `fk_AlertaRegiao_Usuario1`
    FOREIGN KEY (`Usuario_CPF`)
    REFERENCES `sistemaOcorrencias`.`Usuario` (`CPF`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
