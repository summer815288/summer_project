<?php
/**
 * 实现了一个简单的日志系统[可以把日志消息广播给多个接收者]
 *
 * @date   2020/7/16
 * @author edz
 */


require_once dirname(dirname(__FILE__)).'/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
//声明信道
$channel = $connection->channel();
//声明fanout型交换机
$channel->exchange_declare('logs', 'fanout', false, false, false);

$data = implode(' ', array_slice($argv, 1));
if (empty($data)) $data = "info: Hello World!";
$msg = new AMQPMessage($data);
//发布消息到交换机
$channel->basic_publish($msg, 'logs');

echo " [x] Sent ", $data, "\n";

$channel->close();
$connection->close();

