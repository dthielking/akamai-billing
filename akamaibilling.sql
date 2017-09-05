-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 04, 2017 at 08:34 AM
-- Server version: 5.7.19-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

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

CREATE TABLE `tbl_Contracts` (
  `PK_ContractKey` int(11) NOT NULL,
  `ContractId` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tbl_Contracts`
--

INSERT INTO `tbl_Contracts` (`PK_ContractKey`, `ContractId`) VALUES
(2, '3-O5GPDD'),
(1, 'C-KS5Y24');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_Products`
--

CREATE TABLE `tbl_Products` (
  `PK_ProductsKey` int(11) NOT NULL,
  `ProductId` text NOT NULL,
  `ProductName` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tbl_Products`
--

INSERT INTO `tbl_Products` (`PK_ProductsKey`, `ProductId`, `ProductName`) VALUES
(1, 'B-3-2CWD0A', 'Dynamic Content Assembly'),
(2, 'B-3-2RYP6H', 'Advanced Cache Optimization'),
(3, 'B-3-FX2TZ', 'Secure Delivery'),
(4, 'M-LC-102131', 'Aspera Upload Acceleration'),
(5, 'M-LC-853', 'SSL Network Access - Wildcard'),
(6, 'B-3-2CWCZ7', 'Access Control'),
(7, 'M-LC-1196', 'Real User Monitoring'),
(8, 'B-3-A5ME5', 'Site and Visitor Intelligence'),
(9, 'B-3-A5MED', 'NetStorage'),
(10, 'B-3-2CWCQW', 'Content Targeting'),
(11, 'M-LC-1211', 'Dynamic Site Delivery'),
(12, 'B-3-4D7JA2', 'Log Delivery Service'),
(13, 'B-3-4D5VW3', 'Progressive Media Downloads'),
(14, 'B-3-92R4U0', 'SWF Verification'),
(15, 'M-LC-102131', 'Aspera Upload Acceleration'),
(16, 'B-3-92QNMT', 'Log Delivery Service'),
(17, 'M-LC-134267', 'Technical Advisory Service'),
(18, 'B-3-1OLH42', 'Stream and Viewer Intelligence'),
(19, 'B-3-1OJ9JP', 'Log Delivery Service'),
(20, 'B-4-1OYYUD', 'Stream and Viewer intelligence'),
(21, '1-1RUSYB', 'Standard Support'),
(22, 'B-4-1JGZSC', 'HD Streaming for Live and On Demand'),
(23, 'B-3-4D7J3F', 'Content Targeting'),
(24, 'B-3-1OJNZU', 'Content Targeting'),
(25, 'M-LC-136533', 'Named Enhanced Support Plus Technical Advisory Service'),
(26, 'B-3-4D7JCO', 'URL and Visitor Intelligence'),
(27, 'M-LC-135915', 'Professional Services - Enterprise'),
(28, 'M-LC-127469', 'Media Analytics'),
(29, 'M-LC-133443', 'Akamai University Customer Training - Classroom'),
(30, 'B-3-4D7J4U', 'Access Control'),
(31, 'B-3-1OLHC6', 'Secure Streaming'),
(32, 'M-LC-1152', 'SecureHD Player Verification'),
(33, 'M-LC-1151', 'SecureHD Media Encryption'),
(34, 'M-LC-1154', 'SecureHD Content Targeting'),
(35, 'B-3-A5MED', 'NetStorage'),
(36, 'M-LC-1153', 'SecureHD Token Authorization'),
(37, 'M-LC-155691', 'Streaming Combined with Flash Streaming');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_ReportingGroupStatistics`
--

CREATE TABLE `tbl_ReportingGroupStatistics` (
  `PK_ReportingGroupStatistics` int(11) NOT NULL,
  `Value` int(11) NOT NULL,
  `Date` date NOT NULL,
  `Final` tinyint(1) NOT NULL,
  `FK_ProductsKey` int(11) NOT NULL,
  `FK_ReportingGroupKey` int(11) NOT NULL,
  `Unit` text NOT NULL,
  `StatisticType` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_ReportingGroups`
--

CREATE TABLE `tbl_ReportingGroups` (
  `PK_ReportingGroupKey` int(11) NOT NULL COMMENT 'PrimaryKey',
  `ReportingGroupId` int(11) NOT NULL,
  `ReportingGroupName` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tbl_ReportingGroups`
--

INSERT INTO `tbl_ReportingGroups` (`PK_ReportingGroupKey`, `ReportingGroupId`, `ReportingGroupName`) VALUES
(1, 72073, NULL),
(2, 72074, NULL),
(3, 72075, NULL),
(4, 72076, NULL),
(5, 72077, NULL),
(6, 121647, NULL),
(7, 121689, NULL),
(8, 121690, NULL),
(9, 121691, NULL),
(10, 121692, NULL),
(11, 121693, NULL),
(12, 121694, NULL),
(13, 121695, NULL),
(14, 121697, NULL),
(15, 121698, NULL),
(16, 121699, NULL),
(17, 121700, NULL),
(18, 121701, NULL),
(19, 121702, NULL),
(20, 121703, NULL),
(21, 121704, NULL),
(22, 121705, NULL),
(23, 121706, NULL),
(24, 121707, NULL),
(25, 121708, NULL),
(26, 121709, NULL),
(27, 121710, NULL),
(28, 121711, NULL),
(29, 121712, NULL),
(30, 121713, NULL),
(31, 121714, NULL),
(32, 121715, NULL),
(33, 121716, NULL),
(34, 121717, NULL),
(35, 121718, NULL),
(36, 121719, NULL),
(37, 121720, NULL),
(38, 121721, NULL),
(39, 121722, NULL),
(40, 121723, NULL),
(41, 121724, NULL),
(42, 121725, NULL),
(43, 121726, NULL),
(44, 121727, NULL),
(45, 121728, NULL),
(46, 121729, NULL),
(47, 121730, NULL),
(48, 121731, NULL),
(49, 121732, NULL),
(50, 121733, NULL),
(51, 121734, NULL),
(52, 121735, NULL),
(53, 121736, NULL),
(54, 121737, NULL),
(55, 121738, NULL),
(56, 121739, NULL),
(57, 121740, NULL),
(58, 121741, NULL),
(59, 121742, NULL),
(60, 121743, NULL),
(61, 121744, NULL),
(62, 121745, NULL),
(63, 121746, NULL),
(64, 121747, NULL),
(65, 121748, NULL),
(66, 121749, NULL),
(67, 121750, NULL),
(68, 121751, NULL),
(69, 121752, NULL),
(70, 121753, NULL),
(71, 121754, NULL),
(72, 121755, NULL),
(73, 121756, NULL),
(74, 121757, NULL),
(75, 121758, NULL),
(76, 121759, NULL),
(77, 121760, NULL),
(78, 121761, NULL),
(79, 121762, NULL),
(80, 121763, NULL),
(81, 121764, NULL),
(82, 121765, NULL),
(83, 121766, NULL),
(84, 121767, NULL),
(85, 121768, NULL),
(86, 121769, NULL),
(87, 121770, NULL),
(88, 121771, NULL),
(89, 121772, NULL),
(90, 121773, NULL),
(91, 121774, NULL),
(92, 121775, NULL),
(93, 121776, NULL),
(94, 121777, NULL),
(95, 121778, NULL),
(96, 121779, NULL),
(97, 121780, NULL),
(98, 121781, NULL),
(99, 121782, NULL),
(100, 121783, NULL),
(101, 121784, NULL),
(102, 121785, NULL),
(103, 121786, NULL),
(104, 121787, NULL),
(105, 121788, NULL),
(106, 121789, NULL),
(107, 121790, NULL),
(108, 121791, NULL),
(109, 121792, NULL),
(110, 121793, NULL),
(111, 121794, NULL),
(112, 121795, NULL),
(113, 121796, NULL),
(114, 121797, NULL),
(115, 121798, NULL),
(116, 121799, NULL),
(117, 121800, NULL),
(118, 121801, NULL),
(119, 121802, NULL),
(120, 121803, NULL),
(121, 121804, NULL),
(122, 121805, NULL),
(123, 121806, NULL),
(124, 121807, NULL),
(125, 121808, NULL),
(126, 121809, NULL),
(127, 121810, NULL),
(128, 121811, NULL),
(129, 121812, NULL),
(130, 121813, NULL),
(131, 121814, NULL),
(132, 121815, NULL),
(133, 121816, NULL),
(134, 121817, NULL),
(135, 121818, NULL),
(136, 121819, NULL),
(137, 121820, NULL),
(138, 121821, NULL),
(139, 121822, NULL),
(140, 121823, NULL),
(141, 121824, NULL),
(142, 121825, NULL),
(143, 121826, NULL),
(144, 121827, NULL),
(145, 121828, NULL),
(146, 121829, NULL),
(147, 121830, NULL),
(148, 121831, NULL),
(149, 121832, NULL),
(150, 121833, NULL),
(151, 121834, NULL),
(152, 121835, NULL),
(153, 121836, NULL),
(154, 121837, NULL),
(155, 121838, NULL),
(156, 121839, NULL),
(157, 121840, NULL),
(158, 121841, NULL),
(159, 121842, NULL),
(160, 121843, NULL),
(161, 121844, NULL),
(162, 141689, NULL),
(163, 141720, NULL),
(164, 141722, NULL),
(165, 146263, NULL),
(166, 146264, NULL),
(167, 146270, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ztbl_ReportingContract`
--

CREATE TABLE `ztbl_ReportingContract` (
  `PK_ReportingContractKey` int(11) NOT NULL,
  `FK_ReportingGroupKey` int(11) NOT NULL,
  `FK_ContractsKey` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ztbl_ReportingContract`
--

INSERT INTO `ztbl_ReportingContract` (`PK_ReportingContractKey`, `FK_ReportingGroupKey`, `FK_ContractsKey`) VALUES
(30, 1, 2),
(31, 2, 1),
(32, 2, 2),
(33, 3, 2),
(34, 4, 1),
(35, 4, 2),
(36, 5, 2),
(37, 6, 2),
(38, 7, 2),
(39, 8, 2),
(40, 9, 2),
(41, 10, 2),
(42, 11, 2),
(43, 12, 2),
(44, 13, 2),
(45, 14, 2),
(46, 15, 2),
(47, 16, 2),
(48, 17, 2),
(49, 18, 2),
(50, 19, 2),
(51, 20, 2),
(52, 21, 2),
(53, 22, 2),
(54, 23, 2),
(55, 24, 2),
(56, 25, 2),
(57, 26, 2),
(58, 27, 2),
(59, 28, 2),
(60, 29, 2),
(61, 30, 2),
(62, 31, 2),
(63, 32, 2),
(64, 33, 2),
(65, 34, 2),
(66, 35, 2),
(67, 36, 2),
(68, 37, 2),
(69, 38, 2),
(70, 39, 2),
(71, 40, 2),
(72, 41, 2),
(73, 42, 2),
(74, 43, 2),
(75, 44, 2),
(76, 45, 2),
(77, 46, 2),
(78, 47, 2),
(79, 48, 2),
(80, 49, 2),
(81, 50, 2),
(82, 51, 2),
(83, 52, 2),
(84, 53, 2),
(85, 54, 2),
(86, 55, 2),
(87, 56, 2),
(88, 57, 2),
(89, 58, 2),
(90, 59, 2),
(91, 60, 2),
(92, 61, 2),
(93, 62, 2),
(94, 63, 2),
(95, 64, 2),
(96, 65, 2),
(97, 66, 2),
(98, 67, 2),
(99, 68, 2),
(100, 69, 2),
(101, 70, 2),
(102, 71, 2),
(103, 72, 2),
(104, 74, 2),
(105, 75, 2),
(106, 76, 2),
(107, 77, 2),
(108, 78, 2),
(109, 79, 2),
(110, 80, 2),
(111, 81, 2),
(112, 82, 2),
(113, 83, 2),
(114, 84, 2),
(115, 85, 2),
(116, 86, 2),
(117, 87, 2),
(118, 89, 2),
(119, 90, 2),
(120, 91, 2),
(121, 92, 2),
(122, 93, 2),
(123, 94, 2),
(124, 95, 2),
(125, 96, 2),
(126, 97, 2),
(127, 98, 2),
(128, 99, 2),
(129, 100, 2),
(130, 101, 2),
(131, 102, 2),
(132, 103, 2),
(133, 104, 2),
(134, 106, 2),
(135, 107, 2),
(136, 108, 2),
(137, 109, 2),
(138, 110, 2),
(139, 111, 1),
(140, 112, 2),
(141, 113, 2),
(142, 114, 2),
(143, 115, 1),
(144, 116, 1),
(145, 117, 2),
(146, 118, 2),
(147, 119, 1),
(148, 120, 2),
(149, 121, 2),
(150, 122, 2),
(151, 123, 2),
(152, 124, 2),
(153, 125, 2),
(154, 126, 2),
(155, 127, 2),
(156, 128, 2),
(157, 129, 2),
(158, 130, 2),
(159, 131, 2),
(160, 132, 2),
(161, 133, 1),
(162, 134, 2),
(163, 135, 2),
(164, 136, 2),
(165, 137, 2),
(166, 138, 2),
(167, 139, 2),
(168, 140, 2),
(169, 141, 2),
(170, 142, 2),
(171, 143, 2),
(172, 144, 2),
(173, 145, 2),
(174, 146, 1),
(175, 1, 2),
(176, 2, 1),
(177, 2, 2),
(178, 3, 2),
(179, 4, 1),
(180, 4, 2),
(181, 5, 2),
(182, 6, 2),
(183, 7, 2),
(184, 8, 2),
(185, 9, 2),
(186, 10, 2),
(187, 11, 2),
(188, 12, 2),
(189, 13, 2),
(190, 14, 2),
(191, 15, 2),
(192, 16, 2),
(193, 17, 2),
(194, 18, 2),
(195, 19, 2),
(196, 20, 2),
(197, 21, 2),
(198, 22, 2),
(199, 23, 2),
(200, 24, 2),
(201, 25, 2),
(202, 26, 2),
(203, 27, 2),
(204, 28, 2),
(205, 29, 2),
(206, 30, 2),
(207, 31, 2),
(208, 32, 2),
(209, 33, 2),
(210, 34, 2),
(211, 35, 2),
(212, 36, 2),
(213, 37, 2),
(214, 38, 2),
(215, 39, 2),
(216, 40, 2),
(217, 41, 2),
(218, 42, 2),
(219, 43, 2),
(220, 44, 2),
(221, 45, 2),
(222, 46, 2),
(223, 47, 2),
(224, 48, 2),
(225, 49, 2),
(226, 50, 2),
(227, 51, 2),
(228, 52, 2),
(229, 53, 2),
(230, 54, 2),
(231, 55, 2),
(232, 56, 2),
(233, 57, 2),
(234, 58, 2),
(235, 59, 2),
(236, 60, 2),
(237, 61, 2),
(238, 62, 2),
(239, 63, 2),
(240, 64, 2),
(241, 65, 2),
(242, 66, 2),
(243, 67, 2),
(244, 68, 2),
(245, 69, 2),
(246, 70, 2),
(247, 71, 2),
(248, 72, 2),
(249, 73, 2),
(250, 74, 2),
(251, 75, 2),
(252, 76, 2),
(253, 77, 2),
(254, 78, 2),
(255, 79, 2),
(256, 80, 2),
(257, 81, 2),
(258, 82, 2),
(259, 83, 2),
(260, 84, 2),
(261, 85, 2),
(262, 86, 2),
(263, 87, 2),
(264, 88, 2),
(265, 89, 2),
(266, 90, 2),
(267, 91, 2),
(268, 92, 2),
(269, 93, 2),
(270, 94, 2),
(271, 95, 2),
(272, 96, 2),
(273, 97, 2),
(274, 98, 2),
(275, 99, 2),
(276, 100, 2),
(277, 101, 2),
(278, 102, 2),
(279, 103, 2),
(280, 104, 2),
(281, 105, 2),
(282, 106, 2),
(283, 107, 2),
(284, 108, 2),
(285, 110, 2),
(286, 111, 1),
(287, 112, 2),
(288, 113, 2),
(289, 114, 2),
(290, 115, 1),
(291, 116, 1),
(292, 117, 2),
(293, 118, 2),
(294, 119, 1),
(295, 120, 2),
(296, 121, 2),
(297, 122, 2),
(298, 123, 2),
(299, 124, 2),
(300, 125, 2),
(301, 126, 2),
(302, 127, 2),
(303, 128, 2),
(304, 129, 2),
(305, 130, 2),
(306, 131, 2),
(307, 132, 2),
(308, 133, 1),
(309, 134, 2),
(310, 135, 2),
(311, 136, 2),
(312, 137, 2),
(313, 138, 2),
(314, 139, 2),
(315, 140, 2),
(316, 141, 2),
(317, 142, 2),
(318, 143, 2),
(319, 144, 2),
(320, 145, 2),
(321, 146, 1),
(322, 147, 1),
(323, 148, 1),
(324, 149, 2),
(325, 150, 1),
(326, 151, 1),
(327, 152, 2),
(328, 153, 2),
(329, 154, 2),
(330, 155, 2),
(331, 156, 2),
(332, 157, 1),
(333, 158, 2),
(334, 159, 2),
(335, 160, 2),
(336, 161, 2),
(337, 162, 2),
(338, 163, 2),
(339, 164, 2),
(340, 166, 2),
(341, 167, 2);

-- --------------------------------------------------------

--
-- Table structure for table `ztbl_ReportingProduct`
--

CREATE TABLE `ztbl_ReportingProduct` (
  `PK_ReportingProductKey` int(11) NOT NULL,
  `FK_ProductsKey` int(11) NOT NULL,
  `FK_ReportingGroupKey` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_Contracts`
--
ALTER TABLE `tbl_Contracts`
  ADD PRIMARY KEY (`PK_ContractKey`),
  ADD UNIQUE KEY `ContractId` (`ContractId`),
  ADD UNIQUE KEY `PK_ContractKey` (`PK_ContractKey`);

--
-- Indexes for table `tbl_Products`
--
ALTER TABLE `tbl_Products`
  ADD PRIMARY KEY (`PK_ProductsKey`);

--
-- Indexes for table `tbl_ReportingGroupStatistics`
--
ALTER TABLE `tbl_ReportingGroupStatistics`
  ADD PRIMARY KEY (`PK_ReportingGroupStatistics`),
  ADD KEY `PK_ReportingGroupStatistics` (`PK_ReportingGroupStatistics`,`FK_ProductsKey`,`FK_ReportingGroupKey`),
  ADD KEY `FK_ProductsKey` (`FK_ProductsKey`),
  ADD KEY `FK_ReportingGroupKey` (`FK_ReportingGroupKey`);

--
-- Indexes for table `tbl_ReportingGroups`
--
ALTER TABLE `tbl_ReportingGroups`
  ADD PRIMARY KEY (`PK_ReportingGroupKey`),
  ADD UNIQUE KEY `ReportingGroupId` (`ReportingGroupId`),
  ADD KEY `PK_ReportingGroupKey` (`PK_ReportingGroupKey`);

--
-- Indexes for table `ztbl_ReportingContract`
--
ALTER TABLE `ztbl_ReportingContract`
  ADD PRIMARY KEY (`PK_ReportingContractKey`),
  ADD KEY `FK_ReportingGroupKey` (`FK_ReportingGroupKey`),
  ADD KEY `FK_ContractsKey` (`FK_ContractsKey`);

--
-- Indexes for table `ztbl_ReportingProduct`
--
ALTER TABLE `ztbl_ReportingProduct`
  ADD PRIMARY KEY (`PK_ReportingProductKey`),
  ADD KEY `PK_ReportingProductKey` (`PK_ReportingProductKey`,`FK_ProductsKey`,`FK_ReportingGroupKey`),
  ADD KEY `FK_ProductsKey` (`FK_ProductsKey`),
  ADD KEY `FK_ReportingGroupKey` (`FK_ReportingGroupKey`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_Contracts`
--
ALTER TABLE `tbl_Contracts`
  MODIFY `PK_ContractKey` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `tbl_Products`
--
ALTER TABLE `tbl_Products`
  MODIFY `PK_ProductsKey` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;
--
-- AUTO_INCREMENT for table `tbl_ReportingGroupStatistics`
--
ALTER TABLE `tbl_ReportingGroupStatistics`
  MODIFY `PK_ReportingGroupStatistics` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `tbl_ReportingGroups`
--
ALTER TABLE `tbl_ReportingGroups`
  MODIFY `PK_ReportingGroupKey` int(11) NOT NULL AUTO_INCREMENT COMMENT 'PrimaryKey', AUTO_INCREMENT=168;
--
-- AUTO_INCREMENT for table `ztbl_ReportingContract`
--
ALTER TABLE `ztbl_ReportingContract`
  MODIFY `PK_ReportingContractKey` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=342;
--
-- AUTO_INCREMENT for table `ztbl_ReportingProduct`
--
ALTER TABLE `ztbl_ReportingProduct`
  MODIFY `PK_ReportingProductKey` int(11) NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
