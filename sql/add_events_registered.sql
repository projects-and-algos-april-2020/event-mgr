-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
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
-- Table `event_manager`.`events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`events` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`events` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `event_name` VARCHAR(155) NULL DEFAULT NULL,
  `host` VARCHAR(155) NULL DEFAULT NULL,
  `notes` VARCHAR(255) NULL DEFAULT NULL,
  `start_time` DATETIME NULL DEFAULT NULL,
  `start_date` DATETIME NULL DEFAULT NULL,
  `end_time` DATETIME NULL DEFAULT NULL,
  `end_date` DATETIME NULL DEFAULT NULL,
  `address_01` VARCHAR(155) NULL DEFAULT NULL,
  `address_02` VARCHAR(155) NULL DEFAULT NULL,
  `city` VARCHAR(155) NULL DEFAULT NULL,
  `state` VARCHAR(45) NULL DEFAULT NULL,
  `zip_code` VARCHAR(45) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `event_manager`.`student_accounts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`student_accounts` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`student_accounts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `school_name` VARCHAR(155) NULL DEFAULT NULL,
  `first_name` VARCHAR(155) NULL DEFAULT NULL,
  `last_name` VARCHAR(155) NULL DEFAULT NULL,
  `password` VARCHAR(155) NULL DEFAULT NULL,
  `email` VARCHAR(155) NULL DEFAULT NULL,
  `phone_number` VARCHAR(45) NULL DEFAULT NULL,
  `int_fb` VARCHAR(255) NULL DEFAULT 'Facebook API KEY',
  `int_tw` VARCHAR(255) NULL DEFAULT 'Twitter API Key',
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `event_manager`.`student_badges`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`student_badges` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`student_badges` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_account_id` INT NOT NULL,
  `badge_id` INT NULL DEFAULT NULL,
  `QR_code` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_student_badges_student_accounts1_idx` (`student_account_id` ASC) VISIBLE,
  CONSTRAINT `fk_student_badges_student_accounts1`
    FOREIGN KEY (`student_account_id`)
    REFERENCES `event_manager`.`student_accounts` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `event_manager`.`events_student_badges`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`events_student_badges` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`events_student_badges` (
  `event_id` INT NOT NULL,
  `student_badge_id` INT NOT NULL,
  INDEX `fk_events_student_badges_events1_idx` (`event_id` ASC) VISIBLE,
  INDEX `fk_events_student_badges_student_badges1_idx` (`student_badge_id` ASC) VISIBLE,
  CONSTRAINT `fk_events_student_badges_events1`
    FOREIGN KEY (`event_id`)
    REFERENCES `event_manager`.`events` (`id`),
  CONSTRAINT `fk_events_student_badges_student_badges1`
    FOREIGN KEY (`student_badge_id`)
    REFERENCES `event_manager`.`student_badges` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `event_manager`.`student_webcard`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`student_webcard` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`student_webcard` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_account_id` INT NOT NULL,
  `student_photo` BLOB NULL DEFAULT NULL,
  `academic_interest01` VARCHAR(155) NULL DEFAULT NULL,
  `academic_interest02` VARCHAR(155) NULL DEFAULT NULL,
  `academic_interest03` VARCHAR(155) NULL DEFAULT NULL,
  `webcard_URL` VARCHAR(255) NULL DEFAULT NULL,
  `created_At` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_student_webcard_student_accounts1_idx` (`student_account_id` ASC) VISIBLE,
  CONSTRAINT `fk_student_webcard_student_accounts1`
    FOREIGN KEY (`student_account_id`)
    REFERENCES `event_manager`.`student_accounts` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `event_manager`.`studentacct_event`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`studentacct_event` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`studentacct_event` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_account_id` INT NOT NULL,
  `event_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_studentacct_event_student_accounts1_idx` (`student_account_id` ASC) VISIBLE,
  INDEX `fk_studentacct_event_events1_idx` (`event_id` ASC) VISIBLE,
  CONSTRAINT `fk_studentacct_event_events1`
    FOREIGN KEY (`event_id`)
    REFERENCES `event_manager`.`events` (`id`),
  CONSTRAINT `fk_studentacct_event_student_accounts1`
    FOREIGN KEY (`student_account_id`)
    REFERENCES `event_manager`.`student_accounts` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `event_manager`.`event_participants`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `event_manager`.`event_participants` ;

CREATE TABLE IF NOT EXISTS `event_manager`.`event_participants` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `studentacct_event_id` INT NOT NULL,
  `event` VARCHAR(155) NULL,
  `date_time` DATETIME NULL,
  `host` VARCHAR(155) NULL,
  `email` VARCHAR(155) NULL DEFAULT NULL,
  `notes` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_event_participants_studentacct_event1_idx` (`studentacct_event_id` ASC) VISIBLE,
  CONSTRAINT `fk_event_participants_studentacct_event1`
    FOREIGN KEY (`studentacct_event_id`)
    REFERENCES `event_manager`.`studentacct_event` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
