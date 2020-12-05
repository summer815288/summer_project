<?php
/**
 * 消息持久化【生产者】
 * 会按计划发送任务到工作队列
 * 每个任务只分发给一个工作者
 *
 * @date   2020/7/15
 * @author edz
 */

require_once dirname(dirname(__FILE__)) . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
if (!$connection->isConnected()) {
    echo 'connect error';
    die;
}

$channel = $connection->channel();
$channel->queue_declare('task_queues', false, true, false, false);
$data = implode(' ', array_slice($argv, 1));
if (empty($data)) {
    $data = "Hello World!";
}
$msg = new AMQPMessage($data, ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT] # 使消息持久化
);

$channel->basic_publish($msg, '', 'task_queue', true, '');//设置mandatory=true,

echo " [x] Sent ", $data, "\n";
$channel->close();
$connection->close();


