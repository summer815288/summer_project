<?php
/**
 * 寻找缺失的整数
 * User: summer
 * Date: 2020/11/26
 * Time: 11:12 PM
 */

/**
 * 1。在一个无序数组里有99个不重复的正整数，范围是1-100，唯独缺少一个1-100中的整数，如何找出这个缺失的整数？
 *思路：得到1-100的总和，减去数组中的每个值，最后得到的就是缺失的整数
 * 时间复杂度：o(n)
 * 空间复杂度：o(1)
 *
 * @param $data
 *
 * @return float|int
 */

function get_missing_number($data)
{
    $sum = (1 + 100) * 100 / 2;
    foreach ($data as $k => $v) {
        $sum -= $v;
    }

    return $sum;
}

//构造无序数组
for ($i = 1; $i < 101; $i ++) {
    if ($i != 88) {
        $data[] = $i;
    }
}

//输出无序数组
echo get_missing_number($data);
print_r("\n");

/**
 *一个无序数组里有若干个正整数，范围是1-100，其中99个整数都出现了偶数次，只有一个整数出现了奇数次，如何找到这个出现奇数次的数？
 *思路：使用异或运算；偶数次异或得到的是0，出现奇数次异或得到的是1
 * 遍历整个数组，依次做异或运算。由于异或在位运算时相同为0，不同为1，因此所有出现偶数次的整数都会相互抵消变成0，只有唯一出现奇数次的整数会被留下。
 * 假设数组长度是N，那么该解法的时间复杂度是O（N），空间复杂度是O（1）
 *
 * @param $data
 *
 * @return mixed
 */
function get_odd_number($data)
{
    $s = 0;
    foreach ($data as $key => $value) {
        $s ^= $value;
    }

    return $s;

}

$array  = [4, 1, 2, 2, 5, 1, 4];//4出现2次，2出现2次，1出现2次，5出现1次
$result = get_odd_number($array);
print_r($result);
print_r("\n");

/**
 * 3.假设一个无序数组里有若干个正整数，范围是1-100，其中有98个整数出现了偶数次，只有2个整数出现了奇数次，如何找到这2个出现奇数次的整数
 * 思路：分治法
 * 首先把数组元素依次进行异或运算，得到的结果是2个出现了奇数次的整数的异或运算结果，在这个结果中至少有1个二进制位是1
 *
 */

function find_lost_number($data)
{
    //1.第一次进行整体异或运算
    $xorResult = 0;
    foreach ($data as $key => $value) {
        $xorResult ^= $value;
    }
    //如果进行异或运算的结果为0，说明输入的数组不符合题目要求
    if ($xorResult == 0) {
        return null;
    }

    //2.确定2个整数的不同位，以此来分组
    $separator = 1;
    while (0 == ($xorResult & $separator)) {
        $separator <<= 1;
    }
    //3.第二次分组进行异或运算
    $result = [];//用于存储2个出现奇数次整数
    /**
     * 知识小课堂：
     * &&就是判断两个表达式的真假性，只有两个表达式同时为真才为真，有一个为假则为假，具有短路性质。
     * &是将两个二进制的数逐位相与，结果是相与之后的结果。 在计算机网络中相与运算就是同为1时结果为1，其他都为0。取反就是0和1交换就行了。
     */
    foreach ($data as $key => $value) {
        if (0 == ($value & $separator)) {
            $result[0] ^= $value;
            $result1[] = $value;
        } else {
            $result[1] ^= $value;
            $result2[] = $value;
        }
    }
}

$array  = [4, 1, 2, 2, 5, 1, 4, 3];//4出现2次，2出现2次，1出现2次，5出现1次，3出现1次
$result = find_lost_number($array);
print_r($result);
