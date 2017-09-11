-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 06, 2017 at 05:28 PM
-- Server version: 10.1.26-MariaDB
-- PHP Version: 7.1.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `akamaibilling`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_contracts`
--

DROP TABLE IF EXISTS `tbl_contracts`;
CREATE TABLE IF NOT EXISTS `tbl_contracts` (
  `ContractId` varchar(15) NOT NULL,
  PRIMARY KEY (`ContractId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_products`
--

DROP TABLE IF EXISTS `tbl_products`;
CREATE TABLE IF NOT EXISTS `tbl_products` (
  `ProductId` varchar(15) NOT NULL,
  `ProductName` text,
  PRIMARY KEY (`ProductId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_reportinggroups`
--

DROP TABLE IF EXISTS `tbl_reportinggroups`;
CREATE TABLE IF NOT EXISTS `tbl_reportinggroups` (
  `ReportingGroupId` varchar(15) NOT NULL,
  `ReportingGroupName` text,
  PRIMARY KEY (`ReportingGroupId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_reportinggroupstatistics`
--

DROP TABLE IF EXISTS `tbl_reportinggroupstatistics`;
CREATE TABLE IF NOT EXISTS `tbl_reportinggroupstatistics` (
  `Value` bigint(20) UNSIGNED NOT NULL,
  `Date` date NOT NULL,
  `Final` tinyint(1) NOT NULL,
  `ProductsId` varchar(15) NOT NULL,
  `ReportingGroupId` varchar(15) NOT NULL,
  `Unit` text NOT NULL,
  `StatisticType` varchar(20) NOT NULL,
  PRIMARY KEY (`Date`,`ProductsId`,`ReportingGroupId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ztbl_reportingcontract`
--

DROP TABLE IF EXISTS `ztbl_reportingcontract`;
CREATE TABLE IF NOT EXISTS `ztbl_reportingcontract` (
  `ReportingGroupKey` varchar(15) NOT NULL,
  `ContractsKey` varchar(15) NOT NULL,
  PRIMARY KEY (`ReportingGroupKey`,`ContractsKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ztbl_reportingproduct`
--

DROP TABLE IF EXISTS `ztbl_reportingproduct`;
CREATE TABLE IF NOT EXISTS `ztbl_reportingproduct` (
  `ProductsKey` varchar(15) NOT NULL,
  `ReportingGroupKey` varchar(15) NOT NULL,
  PRIMARY KEY (`ProductsKey`,`ReportingGroupKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
