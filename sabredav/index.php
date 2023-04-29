<?php

use
Sabre\DAV;

require_once 'vendor/autoload.php';

date_default_timezone_set('UTC');
$pdo = new \PDO('pgsql:host=127.0.0.1;port=5432;dbname=sabredav;user=sabredav;password={{ sabredav_database_password }}');
$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$authBackend = new \Sabre\DAV\Auth\Backend\PDO($pdo);
$authBackend->setRealm('{{ sabredav_realm }}');

$principalBackend = new \Sabre\DAVACL\PrincipalBackend\PDO($pdo);
$carddavBackend = new \Sabre\CardDAV\Backend\PDO($pdo);
$caldavBackend = new \Sabre\CalDAV\Backend\PDO($pdo);

$nodes = [
    new \Sabre\CalDAV\Principal\Collection($principalBackend),
    new \Sabre\CalDAV\CalendarRoot($principalBackend, $caldavBackend),
    new \Sabre\CardDAV\AddressBookRoot($principalBackend, $carddavBackend),
];

$server = new \Sabre\DAV\Server($nodes);
$server->setBaseUri("/");

$server->addPlugin(new \Sabre\DAV\Auth\Plugin($authBackend));
$server->addPlugin(new \Sabre\DAV\Browser\Plugin());
$server->addPlugin(new \Sabre\DAV\Sync\Plugin());
$server->addPlugin(new \Sabre\DAV\Sharing\Plugin());
$server->addPlugin(new \Sabre\DAVACL\Plugin());

$server->addPlugin(new \Sabre\CalDAV\Plugin());
$server->addPlugin(new \Sabre\CalDAV\Schedule\Plugin());
$server->addPlugin(new \Sabre\CalDAV\SharingPlugin());
$server->addPlugin(new \Sabre\CalDAV\ICSExportPlugin());

$server->addPlugin(new \Sabre\CardDAV\Plugin());
$server->addPlugin(new \Sabre\CardDAV\VCFExportPlugin());

$server->start();
