-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: May 31, 2018 at 07:16 PM
-- Server version: 10.1.16-MariaDB
-- PHP Version: 7.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gamedb`
--

-- --------------------------------------------------------

--
-- Table structure for table `developer`
--

CREATE TABLE `developer` (
  `DeveloperId` int(11) NOT NULL,
  `DeveloperName` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `developer`
--

INSERT INTO `developer` (`DeveloperId`, `DeveloperName`) VALUES
(1, 'PUBG Corporation'),
(2, '11 bit studios'),
(3, 'ConcernedApe'),
(4, 'Obsidian Entertainment'),
(5, 'Sports Interactive'),
(6, 'Milestone S.r.l.'),
(7, 'Facepunch Studios'),
(8, 'Square Enix'),
(9, 'Wube Software LTD.'),
(10, 'Ludeon Studios'),
(11, 'Bethesda Game Studios'),
(12, 'Crytek');

-- --------------------------------------------------------

--
-- Table structure for table `game`
--

CREATE TABLE `game` (
  `GameId` int(11) NOT NULL,
  `GameName` varchar(255) NOT NULL,
  `GamePrice` int(11) NOT NULL,
  `GamePicture` varchar(255) NOT NULL,
  `GameDescription` varchar(255) NOT NULL,
  `DeveloperId` int(11) DEFAULT NULL,
  `GenreId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `game`
--

INSERT INTO `game` (`GameId`, `GameName`, `GamePrice`, `GamePicture`, `GameDescription`, `DeveloperId`, `GenreId`) VALUES
(1, 'PLAYERUNKNOWN''S BATTLEGROUNDS', 150000, 'pubg.jpg', 'PLAYERUNKNOWN''S BATTLEGROUNDS is a battle royale shooter that pits 100 players against each other in a struggle for survival. Gather supplies and outwit your opponents to become the last person standing.', 1, 1),
(2, 'Hunt Showdown', 175000, 'huntshowdown.jpg', 'Hunt: Showdown is a competitive first-person PvP bounty hunting game with heavy PvE elements, from the makers of Crysis. Set in the darkest corners of the world, it packs the thrill of survival games into a match-based format.', 12, 1),
(3, 'Frostpunk', 100000, 'frostpunk.jpg', 'Frostpunk is the first society survival game. As the ruler of the last city on Earth, it is your duty to manage both its citizens and its infrastructure. What decisions will you make to ensure your society''s survival?', 2, 2),
(4, 'Stardew Valley', 115000, 'stardewvalley.jpg', 'You''ve inherited your grandfather''s old farm plot in Stardew Valley. Armed with hand-me-down tools and a few coins, you set out to begin your new life. Can you learn to live off the land and turn these overgrown fields into a thriving home?', 3, 3),
(5, 'Pillars of Eternity II: Deadfire', 200000, 'poe2deadfire.jpg', 'Pursue a rogue god over land and sea in the sequel to the multi-award-winning RPG Pillars of Eternity. Captain your ship on a dangerous voyage of discovery across the vast unexplored archipelago region of the Deadfire.', 4, 4),
(6, 'Football Manager 2018', 400000, 'footballmanager2018.jpg', 'Football Manager 2018 is the latest release in the best-selling, smash-hit series. Putting you in the hot seat of any soccer club in more than 50 countries across the world, Football Manager 2018 is the closest thing to doing the job for real.', 5, 5),
(7, 'Ride 2', 55000, 'ride2.jpg', 'The fastest and most iconic bikes in the world''s biggest digital garage!', 6, 6),
(8, 'Garry''s Mod', 80000, 'garrysmod.jpg', 'Garry''s Mod is a physics sandbox. There aren''t any predefined aims or goals. We give you the tools and leave you to play.', 7, 3),
(9, 'FINAL FANTASY XV WINDOWS EDITION', 675000, 'ffxvwindowsedition.jpg', 'Take the journey, now in ultimate quality. Boasting a wealth of bonus content and supporting ultra high-resolution graphical options and HDR 10, you can now enjoy the beautiful and carefully-crafted experience of FINAL FANTASY XV like never before.', 8, 4),
(10, 'FINAL FANTASY XII THE ZODIAC AGE', 450000, 'ffxiithezodiacage.jpg', 'FINAL FANTASY XII THE ZODIAC AGE - This revered classic returns, now fully remastered for the first time for PC, featuring all new and enhanced gameplay.', 8, 4),
(11, 'Factorio', 125000, 'factorio.jpg', 'Factorio is a game about building and creating automated factories to produce items of increasing complexity, within an infinite 2D world. Use your imagination to design your factory, combine simple elements into ingenious structures.', 9, 2),
(12, 'RimWorld', 150000, 'rimworld.jpg', 'A sci-fi colony sim driven by an intelligent AI storyteller. Inspired by Dwarf Fortress and Firefly. Generates stories by simulating psychology, ecology, gunplay, melee combat, climate, biomes, diplomacy, interpersonal relationships, art, medicine, trade.', 10, 2),
(13, 'The Elder Scrolls V: Skyrim VR', 850000, 'tesvskyrimvr.jpg', 'A true, full-length open-world game for VR has arrived from Bethesda Game Studios. Skyrim VR reimagines the complete epic fantasy masterpiece with an unparalleled sense of scale, depth, and immersion. Skyrim VR also includes all official add-ons.', 11, 4),
(14, 'Fallout Shelter', 25000, 'falloutshelter.jpg', 'Fallout Shelter puts you in control of a state-of-the-art underground Vault from Vault-Tec. Build the perfect Vault, keep your Dwellers happy, and protect them from the dangers of the Wasteland.', 11, 2),
(15, 'Fallout 4 VR', 725000, 'fallout4vr.jpg', 'Fallout 4, the legendary post-apocalyptic adventure from Bethesda Game Studios and winner of more than 200 ‘Best Of’ awards, including the DICE and BAFTA Game of the Year, comes in its entirety to VR.', 11, 4);

-- --------------------------------------------------------

--
-- Table structure for table `gamedetail`
--

CREATE TABLE `gamedetail` (
  `GameDetailId` int(11) NOT NULL,
  `UserId` int(11) NOT NULL,
  `GameId` int(11) NOT NULL,
  `Review` varchar(255) NOT NULL,
  `PostedDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `gamedetail`
--

INSERT INTO `gamedetail` (`GameDetailId`, `UserId`, `GameId`, `Review`, `PostedDate`) VALUES
(1, 2, 1, 'PUBG is so awesome!', '2018-05-04 16:03:42'),
(2, 3, 1, 'I love this game!', '2018-05-09 06:20:59'),
(3, 2, 2, 'I highly reccommend you guys to buy Hunt Showdown', '2018-05-09 15:52:08'),
(4, 1, 1, 'Lets play PUBG together, its so fun', '2018-05-09 16:12:46'),
(5, 1, 1, 'This game is so innovative', '2018-05-15 15:31:34');

-- --------------------------------------------------------

--
-- Table structure for table `genre`
--

CREATE TABLE `genre` (
  `GenreId` int(11) NOT NULL,
  `GenreName` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `genre`
--

INSERT INTO `genre` (`GenreId`, `GenreName`) VALUES
(1, 'Action'),
(2, 'Simulation'),
(3, 'Indie'),
(4, 'RPG'),
(5, 'Sports'),
(6, 'Racing');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `UserId` int(11) NOT NULL,
  `UserName` varchar(255) NOT NULL,
  `UserEmail` varchar(255) NOT NULL,
  `UserPassword` varchar(255) NOT NULL,
  `UserRole` varchar(255) NOT NULL,
  `UserPicture` varchar(255) DEFAULT 'default.png'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`UserId`, `UserName`, `UserEmail`, `UserPassword`, `UserRole`, `UserPicture`) VALUES
(1, 'admin', 'admin', 'admin', 'admin', 'businessman.png'),
(2, 'admin2', 'admin2', 'admin2', 'admin', 'showman.png'),
(3, 'tomy', 'tomy@gmail.com', 'asdfasdfasdf', 'member', 'detective.png'),
(4, 'test', 'test@test.com', 'aaa111!!!', 'member', 'default.png'),
(5, 'usersatu', 'usersatu@email.com', 'aaa111!!!', 'member', 'worker.png'),
(6, 'userdua', 'userdua@email.com', 'aaa111!!!', 'member', 'manager.png'),
(7, 'usertiga', 'usertiga@email.com', 'aaa111!!!', 'member', 'maid.png'),
(8, 'userempat', 'userempat@email.com', 'aaa111!!!', 'member', 'teacher.png'),
(9, 'userlima', 'userlima@email.com', 'aaa111!!!', 'member', 'waiter.png');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `developer`
--
ALTER TABLE `developer`
  ADD PRIMARY KEY (`DeveloperId`);

--
-- Indexes for table `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`GameId`),
  ADD KEY `DeveloperId` (`DeveloperId`),
  ADD KEY `GenreId` (`GenreId`);

--
-- Indexes for table `gamedetail`
--
ALTER TABLE `gamedetail`
  ADD PRIMARY KEY (`GameDetailId`),
  ADD KEY `UserId` (`UserId`),
  ADD KEY `GameId` (`GameId`);

--
-- Indexes for table `genre`
--
ALTER TABLE `genre`
  ADD PRIMARY KEY (`GenreId`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`UserId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `developer`
--
ALTER TABLE `developer`
  MODIFY `DeveloperId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT for table `game`
--
ALTER TABLE `game`
  MODIFY `GameId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
--
-- AUTO_INCREMENT for table `gamedetail`
--
ALTER TABLE `gamedetail`
  MODIFY `GameDetailId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `genre`
--
ALTER TABLE `genre`
  MODIFY `GenreId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `UserId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `game`
--
ALTER TABLE `game`
  ADD CONSTRAINT `game_ibfk_1` FOREIGN KEY (`DeveloperId`) REFERENCES `developer` (`DeveloperId`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `game_ibfk_2` FOREIGN KEY (`GenreId`) REFERENCES `genre` (`GenreId`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `gamedetail`
--
ALTER TABLE `gamedetail`
  ADD CONSTRAINT `gamedetail_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `user` (`UserId`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `gamedetail_ibfk_2` FOREIGN KEY (`GameId`) REFERENCES `game` (`GameId`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
