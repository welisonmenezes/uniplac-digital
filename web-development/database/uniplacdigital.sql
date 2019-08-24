-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 23-Ago-2019 às 20:02
-- Versão do servidor: 10.1.38-MariaDB
-- versão do PHP: 7.3.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `uniplacdigital`
--
CREATE DATABASE IF NOT EXISTS `uniplacdigital` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `uniplacdigital`;

-- --------------------------------------------------------

--
-- Estrutura da tabela `category`
--

CREATE TABLE `category` (
  `ID` int(11) NOT NULL,
  `Category` varchar(45) DEFAULT NULL,
  `Description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `category`
--

INSERT INTO `category` (`ID`, `Category`, `Description`) VALUES
(1, 'Sistemas de Informação', 'Lorem ipsum'),
(2, 'Direito', 'Lorem ipsum');

-- --------------------------------------------------------

--
-- Estrutura da tabela `configuration`
--

CREATE TABLE `configuration` (
  `ID` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `UpdatedBy` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `configuration`
--

INSERT INTO `configuration` (`ID`, `Name`, `Phone`, `Email`, `CreatedAt`, `UpdatedAt`, `UpdatedBy`) VALUES
(1, 'Uniplac Lages', '4922333322', 'uniplac@lages.com', '2019-08-23 00:00:00', '2019-08-23 00:00:00', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `configurationimage`
--

CREATE TABLE `configurationimage` (
  `ConfigurationID` int(11) NOT NULL,
  `ImageID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `configurationimage`
--

INSERT INTO `configurationimage` (`ConfigurationID`, `ImageID`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `image`
--

CREATE TABLE `image` (
  `ID` int(11) NOT NULL,
  `ImageData` longblob NOT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `UpdatedBy` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `image`
--

INSERT INTO `image` (`ID`, `ImageData`, `CreatedAt`, `UpdatedAt`, `UpdatedBy`) VALUES
(1, 0x89504e470d0a1a0a0000000d4948445200000020000000200804000000d973b27f0000000467414d410000b18f0bfc6105000000206348524d00007a26000080840000fa00000080e8000075300000ea6000003a98000017709cba513c00000002624b47440000aa8d2332000000097048597300000ec400000ec401952b0e1b0000000774494d4507e30801021f303ccf0574000001444944415448c7a594bf4bc34014803f4d83160505155c741047ff055d6c91ee05c13fc2c9c9ff43173737a14b0517053b893f36d14504290e3a16a42608a5e7d026b9bbe4d2e4eebd2df7beef1e39de03535459a0404c1bf14bd68a084cf80d822d37dc5a10e1968204b712c8b88540c54b0baa5c2bb8a051049b8af136f5d4698f015f7479e6910e6199dbd3f9cb05bbf67894f76cbbe002c19013666441bb143eca075612419dc042f1c292abe2964aa2d8a16fa13896ff844d1721ebe08d051f3cd1c457dea7c5391d5ee9e2b39cf1fc1566b9923fd4b42ee459d8e090b7540f3fcca94e55a10f93c701ef9aa2a9b7252bb2a6719e3345709a2e4914a671dee72f16dc6515440af33e68c4977c67178c14790b658f010241602aa8114cd84847e31e302b36c98f56be6072acd243780e823e61b1bd690e9f4f970e60a84d8f452cfe03c1e14ce32e8da9dc0000002574455874646174653a63726561746500323031392d30382d30315430303a33313a34382b30323a3030185714320000002574455874646174653a6d6f6469667900323031392d30382d30315430303a33313a34382b30323a3030690aac8e0000001974455874536f667477617265007777772e696e6b73636170652e6f72679bee3c1a0000000049454e44ae426082, '2019-08-23 00:00:00', '2019-08-23 00:00:00', 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `post`
--

CREATE TABLE `post` (
  `ID` int(11) NOT NULL,
  `Title` varchar(100) NOT NULL,
  `Excerpt` varchar(255) NOT NULL,
  `Content` longtext NOT NULL,
  `ImageID` int(11) DEFAULT NULL,
  `EntryDate` datetime NOT NULL,
  `DepartureDate` datetime NOT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `StatusID` int(11) NOT NULL,
  `UserID` int(11) NOT NULL,
  `TypeID` int(11) NOT NULL,
  `CategoryID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `post`
--

INSERT INTO `post` (`ID`, `Title`, `Excerpt`, `Content`, `ImageID`, `EntryDate`, `DepartureDate`, `CreatedAt`, `UpdatedAt`, `StatusID`, `UserID`, `TypeID`, `CategoryID`) VALUES
(2, 'Title test', 'Excerpt test', 'Content test', 1, '2019-08-23 00:00:00', '2019-08-23 00:00:00', '2019-08-23 00:00:00', '2019-08-23 00:00:00', 2, 1, 1, NULL),
(3, 'Test two', 'Excertp test two', 'Content test two', 1, '2019-08-23 00:00:00', '2019-08-23 00:00:00', '2019-08-23 00:00:00', '2019-08-23 00:00:00', 2, 1, 1, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `role`
--

CREATE TABLE `role` (
  `ID` int(11) NOT NULL,
  `Role` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `role`
--

INSERT INTO `role` (`ID`, `Role`) VALUES
(1, 'Admin'),
(2, 'Editor');

-- --------------------------------------------------------

--
-- Estrutura da tabela `status`
--

CREATE TABLE `status` (
  `ID` int(11) NOT NULL,
  `Status` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `status`
--

INSERT INTO `status` (`ID`, `Status`) VALUES
(1, 'Waiting'),
(2, 'Aproved');

-- --------------------------------------------------------

--
-- Estrutura da tabela `type`
--

CREATE TABLE `type` (
  `ID` int(11) NOT NULL,
  `Type` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `type`
--

INSERT INTO `type` (`ID`, `Type`) VALUES
(1, 'News'),
(2, 'Infos');

-- --------------------------------------------------------

--
-- Estrutura da tabela `user`
--

CREATE TABLE `user` (
  `ID` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `CreatedAt` datetime NOT NULL,
  `UpdatedAt` datetime NOT NULL,
  `RoleID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `user`
--

INSERT INTO `user` (`ID`, `Name`, `Email`, `Password`, `Phone`, `CreatedAt`, `UpdatedAt`, `RoleID`) VALUES
(1, 'Welison', 'welison@email.com', '123456', '49991919292', '2019-08-23 00:00:00', '2019-08-23 00:00:00', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `configuration`
--
ALTER TABLE `configuration`
  ADD PRIMARY KEY (`ID`,`UpdatedBy`),
  ADD KEY `fk_Configuration_Users1_idx` (`UpdatedBy`);

--
-- Indexes for table `configurationimage`
--
ALTER TABLE `configurationimage`
  ADD PRIMARY KEY (`ConfigurationID`,`ImageID`),
  ADD KEY `fk_Configuration_has_Images_Images1_idx` (`ImageID`),
  ADD KEY `fk_Configuration_has_Images_Configuration_idx` (`ConfigurationID`);

--
-- Indexes for table `image`
--
ALTER TABLE `image`
  ADD PRIMARY KEY (`ID`,`UpdatedBy`),
  ADD KEY `fk_Images_Users1_idx` (`UpdatedBy`);

--
-- Indexes for table `post`
--
ALTER TABLE `post`
  ADD PRIMARY KEY (`ID`,`StatusID`,`UserID`,`TypeID`),
  ADD KEY `fk_Announcements_Statuses1_idx` (`StatusID`),
  ADD KEY `fk_Announcement_User1_idx` (`UserID`),
  ADD KEY `fk_Announcement_Image1_idx` (`ImageID`),
  ADD KEY `fk_Post_PostType1_idx` (`TypeID`),
  ADD KEY `fk_Post_Category1_idx` (`CategoryID`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `status`
--
ALTER TABLE `status`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `type`
--
ALTER TABLE `type`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID`,`RoleID`),
  ADD KEY `fk_Users_Role1_idx` (`RoleID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `configuration`
--
ALTER TABLE `configuration`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `image`
--
ALTER TABLE `image`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `post`
--
ALTER TABLE `post`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `status`
--
ALTER TABLE `status`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `type`
--
ALTER TABLE `type`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `configuration`
--
ALTER TABLE `configuration`
  ADD CONSTRAINT `fk_Configuration_Users1` FOREIGN KEY (`UpdatedBy`) REFERENCES `user` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `configurationimage`
--
ALTER TABLE `configurationimage`
  ADD CONSTRAINT `fk_Configuration_has_Images_Configuration` FOREIGN KEY (`ConfigurationID`) REFERENCES `configuration` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Configuration_has_Images_Images1` FOREIGN KEY (`ImageID`) REFERENCES `image` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `image`
--
ALTER TABLE `image`
  ADD CONSTRAINT `fk_Images_Users1` FOREIGN KEY (`UpdatedBy`) REFERENCES `user` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `post`
--
ALTER TABLE `post`
  ADD CONSTRAINT `fk_Announcement_Image1` FOREIGN KEY (`ImageID`) REFERENCES `image` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Announcement_User1` FOREIGN KEY (`UserID`) REFERENCES `user` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Announcements_Statuses1` FOREIGN KEY (`StatusID`) REFERENCES `status` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Post_Category1` FOREIGN KEY (`CategoryID`) REFERENCES `category` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Post_PostType1` FOREIGN KEY (`TypeID`) REFERENCES `type` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Limitadores para a tabela `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_Users_Role1` FOREIGN KEY (`RoleID`) REFERENCES `role` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
