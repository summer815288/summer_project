<?php

/**
 * 使用bitmap解决标签很多的问题
 * 思路：
 * 使用words数组存储所有的二进制位，一共有64位，
 * 以标签为中心来存储，让每个标签存储包含此标签的所有用户ID，就像倒排索引一样
 *
 * User: summer
 * Date: 2020/11/27
 * Time: 5:52 AM
 */

class BitMap
{
    private $words;
    private $size;//bitmap的位数大小

    public function MyBitmap($size)
    {
        $this->size  = $size;
        $this->words = [];
    }

    /**
     * 判断bitmap某一位的状态
     */
    public function getBit($bitIndex)
    {
        if ($bitIndex < 0 || $bitIndex > $this->size - 1) {
            return '超出bitmap的有效范围';
        }
        $wordIndex = $this->getwordIndex($bitIndex);

        return $this->words[$wordIndex] & (1 << $bitIndex) != 0;

    }

    /**
     * 把bitmap某一位设置为true
     *
     * @param $bitIndex
     *
     * @return string
     */
    public function setBit($bitIndex)
    {
        if ($bitIndex < 0 || $bitIndex > $this->size - 1) {
            return '超出bitmap有效范围';
        }
        $wordIndex              = $this->getwordIndex($bitIndex);
        $this->words[$bitIndex] |= 1 << $bitIndex;

    }

    /**
     * 定位bitmap某一位所对应的word
     *
     * @param $bitIndex
     *
     * @return int
     */
    private function getWordIndex($bitIndex)
    {
        return $bitIndex >> 6;
    }
}

$bitMap = new BitMap();
$a      = $bitMap->setBit(126);
$b      = $bitMap->setBit(75);
print_r($a);
print_r($b);

