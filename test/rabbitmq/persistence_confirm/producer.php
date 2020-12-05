<?php
/**
 * 生产者消息确认
 * User: summer
 * Date: 2020/7/21
 * Time: 13:30
 */
require_once dirname(dirname(__FILE__)) . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use \PhpAmqpLib\Message\AMQPMessage;

class B
{
    /**
     * 默认交换器持久化发送消息-开启消息确认
     * @throws \Exception
     */
     function simpleSend()
    {
        //连接rq
        $conn = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        //建立通道
        $channel = $conn->channel();
        //确认投放队列，并将队列持久化
        $channel->queue_declare('hello2', false, true, false, false);
        //异步回调消息确认
        $channel->set_ack_handler(function (AMQPMessage $message) {
            echo "Message acked with content " . $message->body . PHP_EOL;
        });
        $channel->set_nack_handler(function (AMQPMessage $message) {
            echo "Message nacked with content " . $message->body . PHP_EOL;
        });
        /**开启消息确认*/
        $channel->confirm_select();
        //建立消息，并消息持久化
        $msg = new AMQPMessage('kingblanc!', ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]);
        $channel->basic_publish($msg, '', 'hello2');

        echo " [x] Sent 'Hello World!'\n";
        //阻塞等待消息确认
        $channel->wait_for_pending_acks();

        $channel->close();
        $conn->close();
    }

    /**
     * fanout交换器持久化发送消息-开启消息确认
     * @throws \Exception
     */
    public function fanoutSend()
    {
        $conn    = new  AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        $channel = $conn->channel();
        //创建交换机
        $channel->exchange_declare('logs', 'fanout', false, true, false);
        //创建消息，并持久化
        $message = new AMQPMessage('hello every one', ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]);

        //消息发送状态回调
        $channel->set_ack_handler(function (AMQPMessage $message) {
            echo '发送成功::' . $message->body;
        });

        $channel->set_nack_handler(function (AMQPMessage $message) {
            echo '发送失败::' . $message->body;
        });
        //开启消息发送状态监听
        $channel->confirm_select();
        //发送消息
        $channel->basic_publish($message, 'logs');
        //阻塞等待消息确认
        $channel->wait_for_pending_acks();

        $channel->close();
        $conn->close();
    }

    /**
     * direct交换器持久化发送消息-开启消息确认
     * @throws \Exception
     */
    public function directSend()
    {
        $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        $channel    = $connection->channel();
        $channel->exchange_declare('direct_logs', 'direct', false, true, false);
        $message = new AMQPMessage('hello,balck', ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]);

        //消息发送状态回调
        $channel->set_ack_handler(function (AMQPMessage $message) {
            echo '发送成功::' . $message->body;
        });

        $channel->set_nack_handler(function (AMQPMessage $message) {
            echo '发送失败::' . $message->body;
        });
        //开启消息发送状态监听
        $channel->confirm_select();
        //发送消息
        $channel->basic_publish($message, 'direct_logs', 'direct_black');
        //阻塞等待消息确认
        $channel->wait_for_pending_acks();

        $channel->close();
        $connection->close();
    }
}

 echo (new B())->simpleSend();die;