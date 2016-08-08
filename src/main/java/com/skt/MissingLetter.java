package com.skt;
import java.util.BitSet;


public class MissingLetter {
	private int NUM_ALPHABET_LETTERS = 26;
	private int a_ASCII_NUM = 97;
	
	/**
	 * 
	 * @param s 
	 * @return null if input string argument is null
	 * Returns a String of missing letters in the input string, from the English alphabet
	 * (in alphabetical order)
	 */
	public String findMissingLetters(String s) {
		if (s==null) return null;
		String st = s.toLowerCase();
		StringBuilder sb = new StringBuilder();
		BitSet bs = new BitSet(NUM_ALPHABET_LETTERS);
		for (int i=0; i< st.length(); i++) {
			char ch = st.charAt(i);
			if (ch>='a' && ch <='z') {
				bs.set(ch-'a');
			}
		}
		for (int i=0; i< NUM_ALPHABET_LETTERS;i++ ){
			if (!bs.get(i)){
				char ch = (char)(i+a_ASCII_NUM);
				sb.append(ch);				
			}
		}		
		return sb.toString();
	}
	public static void main(String[] args){
		MissingLetter ml = new MissingLetter();
		String a = ml.findMissingLetters("A slow yellow fox crawls under the proactive dog");
		assert (a.equals("bjkmqz"));
		String b = ml.findMissingLetters("Lions, and tigers, and bears, oh my!");
		assert b.equals("cfjkpquvwxz");
		String c = ml.findMissingLetters("");
		assert c.equals("abcdefghijklmnopqrstuvwxyz");
		System.out.println("a="+a);
		System.out.println("b="+b);
		System.out.println("c="+c);
		String d = ml.findMissingLetters("A quick brown fox jumps over the lazy dog");
		System.out.println("d="+d);
		
	}
}
