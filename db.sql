CREATE TABLE `routerboards` (
  `id` int(11) NOT NULL,
  `identity` varchar(30) COLLATE utf8_bin NOT NULL,
  `ipaddress` varchar(15) COLLATE utf8_bin NOT NULL,
  `locality` varchar(30) COLLATE utf8_bin NOT NULL,
  `username` varchar(30) COLLATE utf8_bin NOT NULL,
  `password` varchar(30) COLLATE utf8_bin NOT NULL,
  `routerosversion` varchar(30) COLLATE utf8_bin NOT NULL,
  `boardname` varchar(30) COLLATE utf8_bin NOT NULL,
  `architecturename` varchar(30) COLLATE utf8_bin NOT NULL,
  `currentfirmware` varchar(30) COLLATE utf8_bin NOT NULL,
  `model` varchar(30) COLLATE utf8_bin NOT NULL,
  `serialnumber` varchar(30) COLLATE utf8_bin NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

ALTER TABLE `routerboards`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `routerboards`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;
