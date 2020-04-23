-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema event_manager
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `event_manager` ;

-- -----------------------------------------------------
-- Schema event_manager
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `event_manager` DEFAULT CHARACTER SET utf8 ;
USE `event_manager` ;

-- -----------------------------------------------------
-- Table `event_manager`.`student_accounts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`student_accounts` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`student_accounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `school_name` VARCHAR(155) NULL,
  `first_name` VARCHAR(155) NULL,
  `last_name` VARCHAR(155) NULL,
  `password` VARCHAR(155) NULL,
  `email` VARCHAR(155) NULL,
  `phone_number` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_manager`.`user_accounts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`user_accounts` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`user_accounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(155) NULL,
  `last_name` VARCHAR(155) NULL,
  `password` VARCHAR(255) NULL,
  `email` VARCHAR(155) NULL,
  `phone_number` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_manager`.`events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`events` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `event_name` VARCHAR(155) NULL,
  `description` VARCHAR(255) NULL,
  `host` VARCHAR(155) NULL,
  `start_time` DATETIME NULL,
  `start_date` DATETIME NULL,
  `end_time` DATETIME NULL,
  `end_date` DATETIME NULL,
  `address_01` VARCHAR(155) NULL,
  `address_02` VARCHAR(155) NULL,
  `city` VARCHAR(155) NULL,
  `state` VARCHAR(45) NULL,
  `zip_code` VARCHAR(45) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_manager`.`student_webcard`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`student_webcard` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`student_webcard` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_photo` BLOB NULL,
  `academic_interest01` VARCHAR(155) NULL,
  `academic_interest02` VARCHAR(155) NULL,
  `academic_interest03` VARCHAR(155) NULL,
  `webcard_URL` VARCHAR(255) NULL,
  `created_At` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `student_accounts_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_student_webcard_student_accounts1_idx` (`student_accounts_id` ASC) VISIBLE,
  CONSTRAINT `fk_student_webcard_student_accounts1`
    FOREIGN KEY (`student_accounts_id`)
    REFERENCES `event_manager`.`student_accounts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_manager`.`student_badges`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`student_badges` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`student_badges` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `badge_id` INT NULL,
  `QR_code` VARCHAR(255) NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `student_accounts_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_student_badges_student_accounts1_idx` (`student_accounts_id` ASC) VISIBLE,
  CONSTRAINT `fk_student_badges_student_accounts1`
    FOREIGN KEY (`student_accounts_id`)
    REFERENCES `event_manager`.`student_accounts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_manager`.`student_acct_events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`student_acct_events` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`student_acct_events` (
  `student_account_event_id` INT NOT NULL AUTO_INCREMENT,
  `student_accounts_id` INT NOT NULL,
  `events_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`student_account_event_id`),
  INDEX `fk_student_acct_events_student_accounts_idx` (`student_accounts_id` ASC) VISIBLE,
  INDEX `fk_student_acct_events_events1_idx` (`events_id` ASC) VISIBLE,
  CONSTRAINT `fk_student_acct_events_student_accounts`
    FOREIGN KEY (`student_accounts_id`)
    REFERENCES `event_manager`.`student_accounts` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_student_acct_events_events1`
    FOREIGN KEY (`events_id`)
    REFERENCES `event_manager`.`events` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `event_manager`.`events_student_badges`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`events_student_badges` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`events_student_badges` (
  `event_student_badge_id` INT NOT NULL AUTO_INCREMENT,
  `events_id` INT NOT NULL,
  `student_badges_id` INT NOT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`event_student_badge_id`),
  INDEX `fk_events_student_badges_events1_idx` (`events_id` ASC) VISIBLE,
  INDEX `fk_events_student_badges_student_badges1_idx` (`student_badges_id` ASC) VISIBLE,
  CONSTRAINT `fk_events_student_badges_events1`
    FOREIGN KEY (`events_id`)
    REFERENCES `event_manager`.`events` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_events_student_badges_student_badges1`
    FOREIGN KEY (`student_badges_id`)
    REFERENCES `event_manager`.`student_badges` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
