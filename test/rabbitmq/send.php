<?php
/**
 * Create  send.php
 *
 * @date   2020/7/15
 * @author edz
 */
require_once __DIR__.'/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
$connection=new AMQPStreamConnection('localhost',5672,'guest','guest');
if(!$connection->isConnected()){
    echo 'connect error';die;
}

$channel=$connection->channel();
$channel->queue_declare('hello',false,false,false,false);
$msg=new AMQPMessage('Hello World!');
$channel->basic_publish($msg,'','hello');
echo "sent 'hello world!'\n";
$channel->close();
$connection->close();

