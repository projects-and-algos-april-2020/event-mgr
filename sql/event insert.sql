USE event_manager;  -- 2020-04-22 03:15:56

INSERT INTO `event_manager`.`events`
(`event_name`,
`host`,
`start_time`,
`start_date`,
`end_time`,
`end_date`,
`address_01`,
`address_02`,
`city`,
`state`,
`zip_code`,
`created_at`,
`updated_at`)
VALUES
('Electric Avenue',
'Eddy Grant Technical College',
NOW(),
NOW(),
NOW(),
NOW(),
'123 Funky Loop',
'1983',
'New York',
'NY',
14468,
NOW(),
NOW())



