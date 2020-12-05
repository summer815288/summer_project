<?php
/**
 * Create  receive_logs.php
 *
 * @date   2020/7/16
 * @author edz
 */


require_once dirname(dirname(__FILE__)).'/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
//声明信道
$channel = $connection->channel();
//声明fanout型交换机
$channel->exchange_declare('logs', 'fanout', false, false, false);
//声明队列
list($queue_name, ,) = $channel->queue_declare("", false, false, true, false);
//队列和交换机绑定
$channel->queue_bind($queue_name, 'logs');

echo ' [*] Waiting for logs. To exit press CTRL+C', "\n";

$callback = function ($msg) {
    echo ' [x] ', $msg->body, "\n";
};
//消费
$channel->basic_consume($queue_name, '', false, true, false, false, $callback);

while (count($channel->callbacks)) {
    $channel->wait();
}

$channel->close();
$connection->close();

