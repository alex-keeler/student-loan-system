-- MySQL Script generated by MySQL Workbench
-- Thu Jun  9 20:35:17 2022
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema loandb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema loandb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `loandb` DEFAULT CHARACTER SET utf8 ;
USE `loandb` ;

-- -----------------------------------------------------
-- Table `loandb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `organization_id` VARCHAR(45) NULL,
  `first_name` VARCHAR(100) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `email_address` VARCHAR(100) NOT NULL,
  `username` VARCHAR(100) NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `user_type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_address_UNIQUE` (`email_address` ASC),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `loandb`.`university`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`university` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `loandb`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`student` (
  `user_id` INT NOT NULL,
  `credit_score` INT NULL,
  `social_security_last_four` INT NOT NULL,
  `university_id` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  INDEX `fk_university_id_idx` (`university_id` ASC),
  CONSTRAINT `fk_s_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `loandb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_s_university_id`
    FOREIGN KEY (`university_id`)
    REFERENCES `loandb`.`university` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `loandb`.`bank`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`bank` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `loandb`.`bank_official`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`bank_official` (
  `user_id` INT NOT NULL,
  `bank_id` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  INDEX `fk_bank_id_idx` (`bank_id` ASC),
  CONSTRAINT `fk_bo_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `loandb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_bo_bank_id`
    FOREIGN KEY (`bank_id`)
    REFERENCES `loandb`.`bank` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `loandb`.`school_billing_official`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`school_billing_official` (
  `user_id` INT NOT NULL,
  `university_id` INT NOT NULL,
  PRIMARY KEY (`user_id`),
  INDEX `fk_university_id_idx` (`university_id` ASC),
  CONSTRAINT `fk_sbo_user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `loandb`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sbo_university_id`
    FOREIGN KEY (`university_id`)
    REFERENCES `loandb`.`university` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `loandb`.`bank_loan_offer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`bank_loan_offer` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `interest_rate` DECIMAL(7,4) NOT NULL,
  `bank_id` INT NOT NULL,
  `interest_type` VARCHAR(45) NOT NULL,
  `start_date` DATETIME NULL,
  `expiration_date` DATETIME NULL,
  `title` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_blo_bank_id_idx` (`bank_id` ASC),
  CONSTRAINT `fk_blo_bank_id`
    FOREIGN KEY (`bank_id`)
    REFERENCES `loandb`.`bank` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `loandb`.`loan`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `loandb`.`loan` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(45) NOT NULL,
  `bank_loan_offer_id` INT NOT NULL,
  `student_user_id` INT NOT NULL,
  `loan_amount` DECIMAL(9,2) NOT NULL,
  `application_date` DATETIME NULL,
  `approval_date` DATETIME NULL,
  `name` VARCHAR(255) NULL,
  `amount_paid` DECIMAL(9,2) NULL,
  `loan_term_months` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_l_bank_loan_offer_id_idx` (`bank_loan_offer_id` ASC),
  INDEX `fk_l_student_user_id_idx` (`student_user_id` ASC),
  CONSTRAINT `fk_l_bank_loan_offer_id`
    FOREIGN KEY (`bank_loan_offer_id`)
    REFERENCES `loandb`.`bank_loan_offer` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_l_student_user_id`
    FOREIGN KEY (`student_user_id`)
    REFERENCES `loandb`.`student` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;