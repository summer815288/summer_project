<?php
/**
 * 消费者发送确认
 * User: summer
 * Date: 2020/7/21
 * Time: 13:30
 */
require_once dirname(dirname(__FILE__)) . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;

class A
{

    function consumer()
    {
        $conn    = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        $channel = $conn->channel();

        $channel->queue_declare('hello2', false, true, false, false);

        echo ' [*] Waiting for messages. To exit press CTRL+C', "\n";

        $callback = function ($msg) {
            echo " [x] Received ", $msg->body, "\n";
            $msg->delivery_info['channel']->basic_ack($msg->delivery_info['delivery_tag']);
        };

        //开启消息确认模式
        $channel->basic_consume('hello2', '', false, false, false, false, $callback);

        while (count($channel->callbacks)) {
            $channel->wait();
        }

        $channel->close();
        $conn->close();
    }

    /**
     * 消息争抢模式-basic_qos
     *
     * @throws \ErrorException
     */
    public function consumer_bos()
    {
        $conn    = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        $channel = $conn->channel();

        $channel->queue_declare('hello', false, true, false, false);

        echo ' [*] Waiting for messages. To exit press CTRL+C', "\n";

        $callback = function ($msg) {
            echo " [x] Received ", $msg->body, "\n";
            sleep(3);
            $msg->delivery_info['channel']->basic_ack($msg->delivery_info['delivery_tag']);
        };

        //开启消息确认模式
        $channel->basic_consume('hello', '', false, false, false, false, $callback);
        /**开启消息争抢**/
        $channel->basic_qos(null, 1, null);
        while (count($channel->callbacks)) {
            $channel->wait();
        }

        $channel->close();
        $conn->close();
    }

    /**
     * fanout消息队列监听
     *
     * @throws \ErrorException
     */
    public function consumer_fanout()
    {
        $conn    = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        $channel = $conn->channel();
        $channel->exchange_declare('logs', 'fanout', false, true, false);
        //获取临时队列
        list($queue_name, ,) = $channel->queue_declare("", false, false, true, false);
        //绑定队列到交换机
        $channel->queue_bind($queue_name, 'logs');

        echo ' [*] Waiting for messages. To exit press CTRL+C', "\n";

        $callback = function ($msg) {
            echo " [x] Received ", $msg->body, "\n";
            sleep(3);
            $msg->delivery_info['channel']->basic_ack($msg->delivery_info['delivery_tag']);
        };

        //开启消息确认模式
        $channel->basic_consume($queue_name, '', false, false, false, false, $callback);

        while (count($channel->callbacks)) {
            $channel->wait();
        }

        $channel->close();
        $conn->close();
    }

    /**
     * direct消息队列监听
     *
     * @throws \ErrorException
     */
    public function consumer_direct()
    {
        $conn    = new AMQPStreamConnection('192.168.2.184', 5672, 'guest', 'guest');
        $channel = $conn->channel();
        $channel->exchange_declare('direct_logs', 'direct', false, true, false);

        //获取临时队列
        list($queue_name, ,) = $channel->queue_declare("", false, false, true, false);
        //绑定队列到交换机
        $channel->queue_bind($queue_name, 'direct_logs', 'direct_black');

        echo ' [*] Waiting for messages. To exit press CTRL+C', "\n";

        $callback = function ($msg) {
            echo " [x] Received ", $msg->body, "\n";
            sleep(3);
            $msg->delivery_info['channel']->basic_ack($msg->delivery_info['delivery_tag']);
        };

        //开启消息确认模式
        $channel->basic_consume($queue_name, '', false, false, false, false, $callback);

        while (count($channel->callbacks)) {
            $channel->wait();
        }

        $channel->close();
        $conn->close();
    }
}

$a = new A();
echo $a->consumer();
die;