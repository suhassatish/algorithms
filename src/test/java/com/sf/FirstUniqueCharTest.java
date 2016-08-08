package com.sf;

import org.junit.Assert;
import com.sf.FirstUniqueChar;
import org.junit.Test;


public class FirstUniqueCharTest {

    @Test
    public void testfind_duplicate() {
        String s0 = "Salesforce is the best company to work for";
        String s = "ABCDabcdA0123"; //checks  repeating case
        String s2 = null;  // checks null check
        String s3 = "@&*9"; //no duplicates
        //String s4 = "UNICODE_CHARACTER";

        //assertEquals ("B", new SalesForce().find_duplicate(s)); //assert for non-static methods
        char s0_r = FirstUniqueChar.first_unique(s0);

        Assert.assertEquals("l", s0_r);
        Assert.assertEquals("B", FirstUniqueChar.first_unique(s));

        Assert.assertEquals("java.lang.NullPointerException", FirstUniqueChar.first_unique(s2));
        Assert.assertEquals(null, FirstUniqueChar.first_unique(s3));
    }
}
