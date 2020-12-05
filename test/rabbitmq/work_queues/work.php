<?php
/**
 * 【消费者】-开启消费者确认模式、事务
 *
 * @date   2020/7/15
 * @author edz
 */
require_once dirname(dirname(__FILE__)) . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;

$connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
$channel    = $connection->channel();
$channel->queue_declare('task_queues', false, true, false, false);
echo '[*] waiting for message . To exit press CTRL+C', "\n";

//channel开启事务
$channel->tx_select();

try {
    $callback = function ($msg) {
        echo " [x] Received ", $msg->body, "\n";
        sleep(substr_count($msg->body, '.'));
        echo " [x] Done", "\n";
        //消息确认
        $msg->delivery_info['channel']->basic_ack($msg->delivery_info['delivery_tag']);
    };
    #翻译时注：只有consumer已经处理并确认了上一条message时queue才分派新的message给它
    $channel->basic_qos(null, 1, null);
    //开启消息确认机制 no_ack=false
    $channel->basic_consume('task_queue', '', false, false, false, false, $callback);
    //channel开启事务
    $channel->tx_commit();
} catch (Exception $e) {
    $channel->tx_rollback();
    //todo 进行后续处理，把未回应的信息储存起来，不要再次进入队列
}
while (count($channel->callbacks)) {
    $channel->wait();
}
$channel->close();
$connection->close();



/**
 * 事务：
 * RabbitMQ中与事务机制有关的方法有三个，
 * 分别是Channel里面的txSelect()，txCommit()以及txRollback()，
 * txSelect用于将当前Channel设置成是transaction模式，txCommit用于提交事务，txRollback用于回滚事务，
 * 在通过txSelect开启事务之后，我们便可以发布消息给broker代理服务器了，
 * 如果txCommit提交成功了，则消息一定是到达broker了，
 * 如果在txCommit执行之前broker异常奔溃或者由于其他原因抛出异常，这个时候我们便可以捕获异常通过txRollback回滚事务了。
 */

/**
 * Publisher Confirm机制（又称为Confirms或Publisher Acknowledgements）：
 * 是作为解决事务机制性能开销大（导致吞吐量下降）而提出的另外一种保证消息不会丢失的方式。
 *
 * 生产者将信道设置成confirm模式，
 * 一旦信道进入confirm模式，所有在该信道上面发布的消息都会被指派一个唯一的ID(从1开始)，
 * 一旦消息被投递到所有匹配的队列之后，broker就会发送一个确认给生产者（包含消息的唯一ID）,这就使得生产者知道消息已经正确到达目的队列了，
 * 如果消息和队列是可持久化的，那么确认消息会将消息写入磁盘之后发出，broker回传给生产者的确认消息中deliver-tag域包含了确认消息的序列号，
 *
 * confirm模式最大的好处在于他是异步的，一旦发布一条消息，生产者应用程序就可以在等信道返回确认的同时继续发送下一条消息，
 * 当消息最终得到确认之后，生产者应用便可以通过回调方法来处理该确认消息，
 * 如果RabbitMQ因为自身内部错误导致消息丢失，就会发送一条nack消息，生产者应用程序同样可以在回调方法中处理该nack消息。
 *
 * 在channel 被设置成 confirm 模式之后，所有被 publish 的后续消息都将被 confirm（即 ack） 或者被nack一次。但是没有对消息被 confirm 的快慢做任何保证，并且同一条消息不会既被 confirm又被nack 。
 *
 * 缺点：
 * Confirm机制在性能上要比事务优越很多。但是Confirm机制，无法进行回滚，
 * 就是一旦服务器崩溃，生产者无法得到Confirm信息，生产者其实本身也不知道该消息吃否已经被持久化，
 * 只有继续重发来保证消息不丢失，但是如果原先已经持久化的消息，并不会被回滚，这样队列中就会存在两条相同的消息，系统需要支持去重。
 *
 * Channel对象提供的ConfirmListener()回调方法只包含deliveryTag（当前Chanel发出的消息序号），
 * 我们需要自己为每一个Channel维护一个unconfirm的消息序号集合，
 * 每publish一条数据，集合中元素加1，每回调一次handleAck方法，unconfirm集合删掉相应的一条（multiple=false）或多条（multiple=true）记录。
 * 从程序运行效率上看，这个unconfirm集合最好采用有序集合SortedSet存储结构。
 */
/*
 * 当消费者开启ack确认机制却忘记在处理完消息后回传rabbitmq ack时，会产生严重后果。

1. 未ack的消费者可以继续接收消息，但是不回传ack。导致rabbitmq内存被unacknowledged messages占用过多。

2. 从代码层面要解决掉，需要放弃掉这个进程，另开进程添加ack代码，进行消息回传。从而清除掉占用内存的已经被处理却未被删除的消息。
 */
