

/* States */
INSERT INTO core_state VALUES (1, 'open', 'open', false, 'ff6f6f');
INSERT INTO core_state VALUES (2, 'in progress', 'in progress', false, 'fff42a');
INSERT INTO core_state VALUES (3, 'closed', 'closed',  false, '85ce55');
SELECT pg_catalog.setval('core_state_id_seq', 3, false);

/*User types*/
INSERT INTO core_usertype VALUES (1, 'OP');
INSERT INTO core_usertype VALUES (2, 'User');
SELECT pg_catalog.setval('core_usertype_id_seq', 2, true);

/*Priorities*/
INSERT INTO core_priority VALUES (1, 'Normal');
INSERT INTO core_priority VALUES (2, 'Medium');
INSERT INTO core_priority VALUES (3, 'Critical');
SELECT pg_catalog.setval('core_priority_id_seq', 3, true);

/*Company*/
INSERT INTO core_company VALUES (1, 'gnubit', 'logo/Wait-Meme-Cool-HD_JOhEzdO.jpg');
SELECT pg_catalog.setval('core_company_id_seq', 1, true);

/*Groups*/
INSERT INTO auth_group VALUES (1, 'SYSADMGRP');
SELECT pg_catalog.setval('auth_group_id_seq', 1, true);

/*Sample users*/
INSERT INTO core_user VALUES (2,'pbkdf2_sha256$24000$jb2a5PXT2HVw$T5tDm6XsVW6Yw4QlCLpp/mqn35KV7c7HV50VOhce0+8=', NULL, false, 'sabueso', 'Ramiro', 'Magallanes', 'sabueso@sabueso.org', true, true, '2017-02-01 00:00:00+01', '', 1, 'https://www.debian.org/security/dsa-long');
SELECT pg_catalog.setval('core_user_id_seq', 2, true);

/*Queues*/
INSERT INTO core_queue VALUES (1, 'cola1', '[Q1]', '', 1);
INSERT INTO core_queue VALUES (2, 'cola2', '[Q2-tech]', '', 1);
SELECT pg_catalog.setval('core_queue_id_seq', 2, true);

/*Rights - Depends on group and queues */
INSERT INTO core_rights VALUES (1, true, true, true, true, true, true, 1, 1);
INSERT INTO core_rights VALUES (2, true, true, true, true, true, true, 1, 2);
SELECT pg_catalog.setval('core_rights_id_seq', 2, true);
