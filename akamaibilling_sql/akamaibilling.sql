-- --------------------------------------------------------
-- Host:                         akamaibilling.shared-service.aws-cbc.cloud
-- Server Version:               5.6.37-log - MySQL Community Server (GPL)
-- Server Betriebssystem:        Linux
-- HeidiSQL Version:             9.5.0.5196
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Exportiere Datenbank Struktur für akamaibilling
CREATE DATABASE IF NOT EXISTS `akamaibilling` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `akamaibilling`;

-- Exportiere Struktur von View akamaibilling.akamaistatistiken_2017
-- Erstelle temporäre Tabelle um View Abhängigkeiten zuvorzukommen
CREATE TABLE `akamaistatistiken_2017` (
	`Datum` DATE NOT NULL,
	`Vertragsnummer` VARCHAR(15) NOT NULL COLLATE 'utf8_general_ci',
	`ReportingGroupId` VARCHAR(15) NOT NULL COLLATE 'utf8_general_ci',
	`ReportingGroupName` TEXT NULL COLLATE 'utf8_general_ci',
	`Produkt` TEXT NULL COLLATE 'utf8_general_ci',
	`Wert` DOUBLE(17,2) UNSIGNED NOT NULL,
	`Einheit` TEXT NOT NULL COLLATE 'utf8_general_ci',
	`StatistikTyp` VARCHAR(20) NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Exportiere Struktur von View akamaibilling.akamaistatistiken_2018
-- Erstelle temporäre Tabelle um View Abhängigkeiten zuvorzukommen
CREATE TABLE `akamaistatistiken_2018` (
	`Datum` DATE NOT NULL,
	`Vertragsnummer` VARCHAR(15) NOT NULL COLLATE 'utf8_general_ci',
	`ReportingGroupId` VARCHAR(15) NOT NULL COLLATE 'utf8_general_ci',
	`ReportingGroupName` TEXT NULL COLLATE 'utf8_general_ci',
	`Produkt` TEXT NULL COLLATE 'utf8_general_ci',
	`Wert` DOUBLE(17,2) UNSIGNED NOT NULL,
	`Einheit` TEXT NOT NULL COLLATE 'utf8_general_ci',
	`StatistikTyp` VARCHAR(20) NOT NULL COLLATE 'utf8_general_ci'
) ENGINE=MyISAM;

-- Exportiere Struktur von Tabelle akamaibilling.tbl_contracts
CREATE TABLE IF NOT EXISTS `tbl_contracts` (
  `ContractId` varchar(15) NOT NULL,
  PRIMARY KEY (`ContractId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Daten Export vom Benutzer nicht ausgewählt
-- Exportiere Struktur von Tabelle akamaibilling.tbl_products
CREATE TABLE IF NOT EXISTS `tbl_products` (
  `ProductId` varchar(15) NOT NULL,
  `ProductName` text,
  PRIMARY KEY (`ProductId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Daten Export vom Benutzer nicht ausgewählt
-- Exportiere Struktur von Tabelle akamaibilling.tbl_reportinggroups
CREATE TABLE IF NOT EXISTS `tbl_reportinggroups` (
  `ReportingGroupId` varchar(15) NOT NULL,
  `ReportingGroupName` text,
  PRIMARY KEY (`ReportingGroupId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Daten Export vom Benutzer nicht ausgewählt
-- Exportiere Struktur von Tabelle akamaibilling.tbl_reportinggroupstatistics
CREATE TABLE IF NOT EXISTS `tbl_reportinggroupstatistics` (
  `Value` double(17,2) unsigned NOT NULL,
  `Date` date NOT NULL,
  `Final` tinyint(1) NOT NULL,
  `ProductsId` varchar(15) NOT NULL,
  `ReportingGroupId` varchar(15) NOT NULL,
  `Unit` text NOT NULL,
  `StatisticType` varchar(20) NOT NULL,
  PRIMARY KEY (`Date`,`ProductsId`,`ReportingGroupId`,`StatisticType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Daten Export vom Benutzer nicht ausgewählt
-- Exportiere Struktur von Tabelle akamaibilling.ztbl_reportingcontract
CREATE TABLE IF NOT EXISTS `ztbl_reportingcontract` (
  `ReportingGroupKey` varchar(15) NOT NULL,
  `ContractsKey` varchar(15) NOT NULL,
  PRIMARY KEY (`ReportingGroupKey`,`ContractsKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Daten Export vom Benutzer nicht ausgewählt
-- Exportiere Struktur von Tabelle akamaibilling.ztbl_reportingproduct
CREATE TABLE IF NOT EXISTS `ztbl_reportingproduct` (
  `ProductsKey` varchar(15) NOT NULL,
  `ReportingGroupKey` varchar(15) NOT NULL,
  PRIMARY KEY (`ProductsKey`,`ReportingGroupKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Daten Export vom Benutzer nicht ausgewählt
-- Exportiere Struktur von View akamaibilling.akamaistatistiken_2017
-- Entferne temporäre Tabelle und erstelle die eigentliche View
DROP TABLE IF EXISTS `akamaistatistiken_2017`;
CREATE ALGORITHM=UNDEFINED DEFINER=`akamaibilling`@`%` SQL SECURITY DEFINER VIEW `akamaistatistiken_2017` AS select `tbl_reportinggroupstatistics`.`Date` AS `Datum`,`ztbl_reportingcontract`.`ContractsKey` AS `Vertragsnummer`,`tbl_reportinggroupstatistics`.`ReportingGroupId` AS `ReportingGroupId`,`tbl_reportinggroups`.`ReportingGroupName` AS `ReportingGroupName`,`tbl_products`.`ProductName` AS `Produkt`,`tbl_reportinggroupstatistics`.`Value` AS `Wert`,`tbl_reportinggroupstatistics`.`Unit` AS `Einheit`,`tbl_reportinggroupstatistics`.`StatisticType` AS `StatistikTyp` from (((`tbl_reportinggroupstatistics` join `tbl_products`) join `ztbl_reportingcontract`) join `tbl_reportinggroups`) where ((`tbl_reportinggroupstatistics`.`ProductsId` = `tbl_products`.`ProductId`) and (`tbl_reportinggroupstatistics`.`ReportingGroupId` = `ztbl_reportingcontract`.`ReportingGroupKey`) and (`tbl_reportinggroupstatistics`.`ReportingGroupId` = `tbl_reportinggroups`.`ReportingGroupId`) and (`tbl_reportinggroupstatistics`.`Date` >= '2017-01-01') and (`tbl_reportinggroupstatistics`.`Date` <= '2017-12-31'));

-- Exportiere Struktur von View akamaibilling.akamaistatistiken_2018
-- Entferne temporäre Tabelle und erstelle die eigentliche View
DROP TABLE IF EXISTS `akamaistatistiken_2018`;
CREATE ALGORITHM=UNDEFINED DEFINER=`akamaibilling`@`%` SQL SECURITY DEFINER VIEW `akamaistatistiken_2018` AS select `tbl_reportinggroupstatistics`.`Date` AS `Datum`,`ztbl_reportingcontract`.`ContractsKey` AS `Vertragsnummer`,`tbl_reportinggroupstatistics`.`ReportingGroupId` AS `ReportingGroupId`,`tbl_reportinggroups`.`ReportingGroupName` AS `ReportingGroupName`,`tbl_products`.`ProductName` AS `Produkt`,`tbl_reportinggroupstatistics`.`Value` AS `Wert`,`tbl_reportinggroupstatistics`.`Unit` AS `Einheit`,`tbl_reportinggroupstatistics`.`StatisticType` AS `StatistikTyp` from (((`tbl_reportinggroupstatistics` join `tbl_products`) join `ztbl_reportingcontract`) join `tbl_reportinggroups`) where ((`tbl_reportinggroupstatistics`.`ProductsId` = `tbl_products`.`ProductId`) and (`tbl_reportinggroupstatistics`.`ReportingGroupId` = `ztbl_reportingcontract`.`ReportingGroupKey`) and (`tbl_reportinggroupstatistics`.`ReportingGroupId` = `tbl_reportinggroups`.`ReportingGroupId`) and (`tbl_reportinggroupstatistics`.`Date` >= '2018-01-01') and (`tbl_reportinggroupstatistics`.`Date` <= '2018-12-31'));

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
