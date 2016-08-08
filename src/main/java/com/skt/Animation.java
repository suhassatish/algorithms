package com.skt;
import java.util.ArrayList;
import java.util.BitSet;
import java.util.InputMismatchException;
import java.util.List;


public class Animation {
	private List<String> flow;
	BitSet bs;
	
	/**
	 * 
	 * @param s "..R...."
	 * @return  "..X...."
	 * Returns an X-depiction for current particles in chamber
	 */
	private String getSnapshot(String s) {
		if (s==null) return null;
		
		StringBuilder sb = new StringBuilder();
		for (int i=0; i< s.length(); i++){
			//state O indicates Overlap of L and R at the same index, at a time snapShot
			if (s.charAt(i)=='L' || s.charAt(i)=='R' || s.charAt(i)=='O'){
				sb.append('X');
				bs.set(i);
			}
							
			else 
				sb.append('.');
		}
		return sb.toString();
	}
	
	String [] animate(int speed, String init) throws Exception {	
		if (init==null) return null;
		if ( !(speed>=1 && speed<=10) || !(init.length()<=50 && init.length()>=1)) 
				throw new InputMismatchException("Input speed should be an integer value between 1 and 10 inclusive. " +
						"Input string size should be between 1 and 50 inclusive characters");
		
		System.out.println("Speed= "+ speed+" Init chamber = "+ init);
		bs= new BitSet(init.length());
		flow = new ArrayList<String>();
		
		//sets initial true entries in internal BitSet		
		flow.add(getSnapshot(init));
		
		StringBuilder prevSb = new StringBuilder(init);
		
		//iterates over different time snapShots till the chamber is empty
		while(bs.length()!=0){
			
			//clears sb at start of each new time snapShot 
			char[] sb = new char[init.length()];
			
			//iterates over length of chamber at any 1 time snapshot
			for (int i=0;i<prevSb.length();i++) {
				//'O' for overlap of 2 particles in a slot, moving in opposite directions
				if (prevSb.charAt(i)=='L'){
					int nextPos = i-speed;
					if (nextPos>=0){
						bs.set(nextPos);						
						if(sb[nextPos]!='R')
							sb[nextPos] = 'L';							
						else
							sb[nextPos] = 'O';						
					}
					bs.clear(i);						
				} else if (prevSb.charAt(i)=='R'){
					int nextPos = i+speed;
					if (nextPos<init.length()){
						bs.set(nextPos);
						
						if (sb[nextPos]=='L')
							sb[nextPos] = 'O';
						else
							sb[nextPos] = 'R';					
					}
					bs.clear(i);
				}else if (prevSb.charAt(i)=='O'){
					int leftPos = i-speed;
					int rightPos = i+speed;
					if (leftPos>=0){
						bs.set(leftPos);						
						if(sb[leftPos]!='R')
							sb[leftPos] = 'L';							
						else
							sb[leftPos] = 'O';						
					}
					if (rightPos<init.length()){
						bs.set(rightPos);						
						if(sb[rightPos]!='L')
							sb[rightPos] = 'R';							
						else
							sb[rightPos] = 'O';						
					}
					bs.clear(i);		
				}
			}
			
			//pad unoccupied slots with '.'
			for (int i=0; i< sb.length; i++){
				if (sb[i]!='L' && sb[i]!='R' && sb[i]!='O'){
					sb[i]='.';
					//a '.' position should have corresponding BitSet entry unset => false
					
					if (bs.get(i)) {
						throw new Exception("Invalid internal BitSet state. Fix the bug in animate()");
					}
				}
			}
			
			//we're done with 1  time snapShot of the chamber, add it to list and refresh prevSb state
			//to keep the latest chamber state
			String str = new String(sb);
			flow.add(getSnapshot(str));
			prevSb.setLength(0);			
			prevSb.append(sb);
			
			//de-reference sb for garbage collection to prevent memory leak (OutOfMemoryError)
			sb=null;
		}
		String [] chamber = new String[flow.size()];
		chamber = flow.toArray(chamber);
		return chamber;
	}
	
	public static void printSequence(String[] sequence) {
		for (String s : sequence){
			System.out.println(s);
		}
	}
	
	public static void main(String[] args){
		Animation an = new Animation();
		try {
			printSequence(an.animate(2, "..R...."));
			printSequence(an.animate(3, "RR..LRL"));
			printSequence(an.animate(2, "LRLR.LRLR"));
			printSequence(an.animate(10, "RLRLRLRLRL"));
			printSequence(an.animate(1, "..."));
			printSequence(an.animate(1, "LRRL.LR.LRR.R.LRRL."));
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
