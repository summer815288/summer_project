<?php
//function gen() {
//    yield 1;
//}
//$g = gen();
//echo $g->valid();    //1
//echo $g->current();  //1
//
//echo $g->next();
//
//echo $g->valid();    //
//echo $g->current();  //


/**
 * 多个yield语句
 *
 * @return \Generator
 */
function gen()
{
    yield 1;
    yield 2;
    yield 3;
}

$g = gen();
$a = $g->valid();//1
$b = $g->current();//1
$c = "\n";

echo $a . ':' . $b;








