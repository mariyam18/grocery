-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Feb 11, 2020 at 02:53 PM
-- Server version: 5.7.29-0ubuntu0.18.04.1
-- PHP Version: 7.2.24-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `grocery`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart_order`
--

CREATE TABLE `cart_order` (
  `order_id` bigint(100) NOT NULL,
  `total_price` int(20) DEFAULT NULL,
  `total_quantity` int(20) DEFAULT NULL,
  `lane1` varchar(100) NOT NULL,
  `lane2` varchar(100) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `uid` int(10) DEFAULT NULL,
  `status_value` int(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cart_order`
--

INSERT INTO `cart_order` (`order_id`, `total_price`, `total_quantity`, `lane1`, `lane2`, `city`, `state`, `uid`, `status_value`) VALUES
(94155669975136, 340, 6, 'hsdhv', 'jhgj', 'yfgv', 'yggh', 1, 0),
(94168333045888, 280, 5, 'yjgj', 'gfgh', 'hgdfgh', 'gdgf', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `order_item`
--

CREATE TABLE `order_item` (
  `cart_item_id` int(10) NOT NULL,
  `Product_id` int(100) DEFAULT NULL,
  `P_name` varchar(50) NOT NULL,
  `P_price` int(20) NOT NULL,
  `P_quantity` int(20) NOT NULL,
  `P_total_price` int(20) NOT NULL,
  `order_id` bigint(100) DEFAULT NULL,
  `shop_id` int(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_item`
--

INSERT INTO `order_item` (`cart_item_id`, `Product_id`, `P_name`, `P_price`, `P_quantity`, `P_total_price`, `order_id`, `shop_id`) VALUES
(53, 1, 'Potato', 50, 2, 100, 94168333045888, 1),
(54, 3, 'Apple', 60, 3, 180, 94168333045888, 2),
(55, 3, 'Apple', 60, 4, 240, 94155669975136, 2),
(56, 8, 'Onion', 50, 2, 100, 94155669975136, 2);

-- --------------------------------------------------------

--
-- Table structure for table `Product`
--

CREATE TABLE `Product` (
  `Product_id` int(100) NOT NULL,
  `P_name` varchar(50) DEFAULT NULL,
  `P_actual_price` int(20) DEFAULT NULL,
  `P_category` varchar(50) DEFAULT NULL,
  `P_discount_price` int(20) DEFAULT NULL,
  `P_quantity` int(20) DEFAULT NULL,
  `P_quantity_type` varchar(50) DEFAULT NULL,
  `shop_id` int(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Product`
--

INSERT INTO `Product` (`Product_id`, `P_name`, `P_actual_price`, `P_category`, `P_discount_price`, `P_quantity`, `P_quantity_type`, `shop_id`) VALUES
(1, 'Potato', 50, 'Vegetables', 45, 16, 'Weight (kg)', 1),
(3, 'Apple', 60, 'Fruits', 50, 8, 'Weight(kg)', 2),
(4, 'Banana', 40, 'Fruits', 38, 4, 'Unit', 2),
(7, 'Apple', 60, 'Fruits', 50, 7, 'Weight(kg)', 3),
(8, 'Onion', 50, 'Vegetables', 40, 4, 'Weight(kg)', 2);

-- --------------------------------------------------------

--
-- Table structure for table `Shopkeeper`
--

CREATE TABLE `Shopkeeper` (
  `shop_id` int(100) NOT NULL,
  `shop_name` varchar(50) DEFAULT NULL,
  `shopkeeper_contact` bigint(13) DEFAULT NULL,
  `shopkeeper_name` varchar(60) DEFAULT NULL,
  `shopkeeper_dob` date DEFAULT NULL,
  `shopkeeper_email` varchar(40) DEFAULT NULL,
  `shop_add` varchar(75) DEFAULT NULL,
  `shop_city` varchar(30) DEFAULT NULL,
  `shop_district` varchar(30) DEFAULT NULL,
  `shop_state` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Shopkeeper`
--

INSERT INTO `Shopkeeper` (`shop_id`, `shop_name`, `shopkeeper_contact`, `shopkeeper_name`, `shopkeeper_dob`, `shopkeeper_email`, `shop_add`, `shop_city`, `shop_district`, `shop_state`) VALUES
(1, 'Abcd shop', 9876543212, 'Mahesh', '1998-12-04', 'mahesh@gmail.com', 'abc,shop no 2', 'mumbra', 'thane', 'maharashtra'),
(2, 'Xyz shop', 3216549870, 'sameer', '1998-10-04', 'sameer@gmail.com', 'xyz,shop no 5', 'mumbra', 'thane', 'maharashtra'),
(3, 'mnop shop', 7418529632, 'bob', '1997-01-13', 'bob@gmail.com', 'samar nagar', 'kalyan', 'thane', 'maharashtra');

-- --------------------------------------------------------

--
-- Table structure for table `Users`
--

CREATE TABLE `Users` (
  `uid` int(10) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Users`
--

INSERT INTO `Users` (`uid`, `email`, `password`) VALUES
(1, 'anoor@gmail.com', '123456'),
(2, 'abc@gmail.com', '123'),
(3, 'xyz@gmail.com', '963'),
(4, 'ansari@gmail.com', '123456'),
(5, 'nooras@gmail.com', '987654'),
(6, 'xyz@gmail.com', '123456'),
(7, 'my@gmail.com', '951'),
(8, 'amina@gmial.com', '123456'),
(9, 'noorasfatima@gmail.com', '123456'),
(10, 'mariyamshaikh@gmail.com', '123456');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart_order`
--
ALTER TABLE `cart_order`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `uid` (`uid`);

--
-- Indexes for table `order_item`
--
ALTER TABLE `order_item`
  ADD PRIMARY KEY (`cart_item_id`),
  ADD KEY `Product_id` (`Product_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `shop_id` (`shop_id`);

--
-- Indexes for table `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`Product_id`),
  ADD KEY `shop_id` (`shop_id`);

--
-- Indexes for table `Shopkeeper`
--
ALTER TABLE `Shopkeeper`
  ADD PRIMARY KEY (`shop_id`);

--
-- Indexes for table `Users`
--
ALTER TABLE `Users`
  ADD PRIMARY KEY (`uid`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `order_item`
--
ALTER TABLE `order_item`
  MODIFY `cart_item_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;
--
-- AUTO_INCREMENT for table `Product`
--
ALTER TABLE `Product`
  MODIFY `Product_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT for table `Shopkeeper`
--
ALTER TABLE `Shopkeeper`
  MODIFY `shop_id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `Users`
--
ALTER TABLE `Users`
  MODIFY `uid` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart_order`
--
ALTER TABLE `cart_order`
  ADD CONSTRAINT `cart_order_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `Users` (`uid`);

--
-- Constraints for table `order_item`
--
ALTER TABLE `order_item`
  ADD CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`Product_id`) REFERENCES `Product` (`Product_id`),
  ADD CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `cart_order` (`order_id`),
  ADD CONSTRAINT `order_item_ibfk_3` FOREIGN KEY (`shop_id`) REFERENCES `Shopkeeper` (`shop_id`);

--
-- Constraints for table `Product`
--
ALTER TABLE `Product`
  ADD CONSTRAINT `Product_ibfk_1` FOREIGN KEY (`shop_id`) REFERENCES `Shopkeeper` (`shop_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
