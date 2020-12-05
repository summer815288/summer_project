<?php
/**
 * Desc: .
 * User: summer
 * Date: 2020/7/21
 * Time: 16:12
 */
require_once dirname(dirname(__FILE__)) . '/vendor/autoload.php';

$hosts  = ["127.0.0.1"];
$client = Elasticsearch\ClientBuilder::create()->setHosts($hosts)->build();
// 添加数据
$params = [
    'index'=>'website',
    'type'=>'blog',
    'id'=>10,
    'body'=>[
        'title'=>'elasticsearch & php',
        'content'=>'balabala...',
        'created_at'=>'2017-08-01 12:02:20'
    ]
];
$resp = $client->index($params);
var_dump($resp);

