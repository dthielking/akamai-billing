-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Aug 25, 2017 at 02:01 PM
-- Server version: 10.1.24-MariaDB-6
-- PHP Version: 7.0.22-2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `akamaibilling`
--
CREATE DATABASE IF NOT EXISTS `akamaibilling` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `akamaibilling`;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_Contracts`
--

DROP TABLE IF EXISTS `tbl_Contracts`;
CREATE TABLE IF NOT EXISTS `tbl_Contracts` (
  `PK_ContractKey` int(11) NOT NULL,
  `ContractId` varchar(10) NOT NULL,
  PRIMARY KEY (`PK_ContractKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_Products`
--

DROP TABLE IF EXISTS `tbl_Products`;
CREATE TABLE IF NOT EXISTS `tbl_Products` (
  `PK_ProductsKey` int(11) NOT NULL,
  `ProductId` int(11) NOT NULL,
  `ProductName` text,
  PRIMARY KEY (`PK_ProductsKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_ReportingGroups`
--

DROP TABLE IF EXISTS `tbl_ReportingGroups`;
CREATE TABLE IF NOT EXISTS `tbl_ReportingGroups` (
  `PK_ReportingGroupKey` int(11) NOT NULL COMMENT 'PrimaryKey',
  `ReportingGroupId` int(11) NOT NULL,
  `ReportingGroupName` text,
  PRIMARY KEY (`PK_ReportingGroupKey`),
  UNIQUE KEY `ReportingGroupId` (`ReportingGroupId`),
  KEY `PK_ReportingGroupKey` (`PK_ReportingGroupKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_ReportingGroupStatistics`
--

DROP TABLE IF EXISTS `tbl_ReportingGroupStatistics`;
CREATE TABLE IF NOT EXISTS `tbl_ReportingGroupStatistics` (
  `PK_ReportingGroupStatistics` int(11) NOT NULL,
  `Value` int(11) NOT NULL,
  `Date` date NOT NULL,
  `Final` tinyint(1) NOT NULL,
  `FK_ProductsKey` int(11) NOT NULL,
  `FK_ReportingGroupKey` int(11) NOT NULL,
  `FK_StatisticsTypeKey` int(11) NOT NULL,
  `Unit` text NOT NULL,
  PRIMARY KEY (`PK_ReportingGroupStatistics`),
  KEY `PK_ReportingGroupStatistics` (`PK_ReportingGroupStatistics`,`FK_ProductsKey`,`FK_ReportingGroupKey`,`FK_StatisticsTypeKey`),
  KEY `FK_StatisticsTypeKey` (`FK_StatisticsTypeKey`),
  KEY `FK_ProductsKey` (`FK_ProductsKey`),
  KEY `FK_ReportingGroupKey` (`FK_ReportingGroupKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_StatisticsType`
--

DROP TABLE IF EXISTS `tbl_StatisticsType`;
CREATE TABLE IF NOT EXISTS `tbl_StatisticsType` (
  `PK_StatisticsTypeKey` int(11) NOT NULL,
  `Type` text NOT NULL,
  PRIMARY KEY (`PK_StatisticsTypeKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ztbl_ReportingContract`
--

DROP TABLE IF EXISTS `ztbl_ReportingContract`;
CREATE TABLE IF NOT EXISTS `ztbl_ReportingContract` (
  `PK_ReportingContractKey` int(11) NOT NULL,
  `FK_ReportingGroupKey` int(11) NOT NULL,
  `FK_ContractsKey` int(11) NOT NULL,
  PRIMARY KEY (`PK_ReportingContractKey`),
  KEY `FK_ReportingGroupKey` (`FK_ReportingGroupKey`),
  KEY `FK_ContractsKey` (`FK_ContractsKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ztbl_ReportingProduct`
--

DROP TABLE IF EXISTS `ztbl_ReportingProduct`;
CREATE TABLE IF NOT EXISTS `ztbl_ReportingProduct` (
  `PK_ReportingProductKey` int(11) NOT NULL,
  `FK_ProductsKey` int(11) NOT NULL,
  `FK_ReportingGroupKey` int(11) NOT NULL,
  PRIMARY KEY (`PK_ReportingProductKey`),
  KEY `PK_ReportingProductKey` (`PK_ReportingProductKey`,`FK_ProductsKey`,`FK_ReportingGroupKey`),
  KEY `FK_ProductsKey` (`FK_ProductsKey`),
  KEY `FK_ReportingGroupKey` (`FK_ReportingGroupKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_Products`
--
ALTER TABLE `tbl_Products`
  ADD CONSTRAINT `tbl_Products_ibfk_1` FOREIGN KEY (`PK_ProductsKey`) REFERENCES `ztbl_ReportingProduct` (`FK_ProductsKey`);

--
-- Constraints for table `tbl_ReportingGroups`
--
ALTER TABLE `tbl_ReportingGroups`
  ADD CONSTRAINT `tbl_ReportingGroups_ibfk_1` FOREIGN KEY (`PK_ReportingGroupKey`) REFERENCES `ztbl_ReportingContract` (`FK_ReportingGroupKey`);

--
-- Constraints for table `tbl_ReportingGroupStatistics`
--
ALTER TABLE `tbl_ReportingGroupStatistics`
  ADD CONSTRAINT `tbl_ReportingGroupStatistics_ibfk_1` FOREIGN KEY (`FK_ProductsKey`) REFERENCES `tbl_Products` (`PK_ProductsKey`),
  ADD CONSTRAINT `tbl_ReportingGroupStatistics_ibfk_2` FOREIGN KEY (`FK_ReportingGroupKey`) REFERENCES `tbl_ReportingGroups` (`PK_ReportingGroupKey`);

--
-- Constraints for table `tbl_StatisticsType`
--
ALTER TABLE `tbl_StatisticsType`
  ADD CONSTRAINT `tbl_StatisticsType_ibfk_1` FOREIGN KEY (`PK_StatisticsTypeKey`) REFERENCES `tbl_ReportingGroupStatistics` (`FK_StatisticsTypeKey`);

--
-- Constraints for table `ztbl_ReportingContract`
--
ALTER TABLE `ztbl_ReportingContract`
  ADD CONSTRAINT `ztbl_ReportingContract_ibfk_1` FOREIGN KEY (`FK_ContractsKey`) REFERENCES `tbl_Contracts` (`PK_ContractKey`);

--
-- Constraints for table `ztbl_ReportingProduct`
--
ALTER TABLE `ztbl_ReportingProduct`
  ADD CONSTRAINT `ztbl_ReportingProduct_ibfk_1` FOREIGN KEY (`FK_ReportingGroupKey`) REFERENCES `tbl_ReportingGroups` (`PK_ReportingGroupKey`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
