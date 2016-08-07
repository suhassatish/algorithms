package com.sf;
import java.io.File;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import com.google.common.collect.Lists;

import edu.princeton.cs.algorithms.Digraph;
import edu.princeton.cs.algorithms.Topological;
import edu.princeton.cs.introcs.In;
import edu.princeton.cs.introcs.Out;

/*
 * Solution submitted by Suhas Satish
 */
public class DependencyManager {
	private Map<String, Integer> map;// string -> index
	private String[] keys;           // index  -> string
	private int N=0;
	
	Digraph G;
	String inputFile;
	String inputDelimiter; 
	Digraph reverseG;
	Map<Integer, List<Integer>> dependencyMap; 
	Map<Integer, List<Integer>> usedByMap;
	
	public DependencyManager(String filename, String delimiter) {
		this.inputFile = filename;
		this.inputDelimiter = delimiter;
		map = new HashMap<String, Integer>();
		
		In in = new In(filename);
		Out out = new Out("dependency.txt");
		while (in.hasNextLine()) {
			String s = in.readLine();
			//System.out.println(s);
			
			if ((s!=null) && (s.length()>0) && s.charAt(0) == 'D') {
				String [] deps = s.split(delimiter);
				
				for (String word : deps) {
					if (word.equals("DEPEND"))
						continue;
					if (!map.containsKey(word)){
						map.put(word, N++);
					}
				}
					//System.out.println(dep+" ");
			}
			else if ((s!=null) && (s.length()>0) && s.charAt(0) == 'I') {
				String [] deps = s.split(delimiter);
				for (String word : deps) {
					if (word.equals("INSTALL"))
						continue;
					if (!map.containsKey(word)){
						map.put(word, N++);
					}
				}
			}
			
		}
		
		
		in.close();
		out.close();
		
		// inverted index to get string keys in an aray
		keys = new String[N];
		for (String name: map.keySet()){
			keys[map.get(name)] = name;
		}
		
		//second pass builds the digraph by connecting vertices according to dependencies
		
		// leaving room for more elements to be added later for those with no dependencies, eg: foo
		G = new Digraph(N); 
		dependencyMap = new HashMap<Integer, List<Integer>>();
		In in2 = new In(filename);
		while (in2.hasNextLine()) {			
			String s = in2.readLine();
			if ((s!=null) && (s.length()>0) && s.charAt(0) == 'D') {
				String [] deps = s.split(delimiter);
				String destination = deps[1];
				int srcId = map.get(destination);
				
				for (int i=2; i< deps.length;i++) {
					int sinkId = map.get(deps[i]);
					//create DAG of (item -> dependency)
					G.addEdge(srcId, sinkId);
					if(!dependencyMap.containsKey(srcId)){
						List<Integer> l = new ArrayList<Integer>();
						l.add(sinkId);
						dependencyMap.put(srcId, l);
					}else {
						List<Integer> l = dependencyMap.get(srcId);
						if (!l.contains(sinkId)){
							l.add(sinkId);
							dependencyMap.put(srcId, l);
						}
					}
					
					
				}
					//System.out.println(dep+" ");
			}
		}
		in2.close();
		reverseG = G.reverse();
		Topological reverseTop = new Topological(reverseG);
		usedByMap = new HashMap<Integer, List<Integer>>();
		
		for (int key: reverseTop.order()) {
			for (int value : reverseG.adj(key)){
				if(!usedByMap.containsKey(key)){
					List<Integer> l = new LinkedList<Integer>();
					l.add(value);
					usedByMap.put(key, l);
				} else {
					List<Integer> l = usedByMap.get(key);
					if (!l.contains(value)){
						l.add(value);
						usedByMap.put(key, l);
					}
				}
				
			}
		}
	}
	 
	public void generateOutput(){
		//precondition: DAG should already exist
		
		//stack for printing installation order
		
		Set<Integer> installed = new HashSet<Integer>(); 
		
		
		if (G == null) throw new NullPointerException("Please initialize the graph first");
		Topological topological = new Topological(G);
		
		In in = new In(this.inputFile);
		while (in.hasNextLine()) {
			String s = in .readLine();
			if (!(s.length()>0))
				return;
			String[] str = s.split(this.inputDelimiter);
			if (str[0].equals("DEPEND")){
				System.out.println(s);
			} else if (str[0].equals("INSTALL")) {
				System.out.println(s);
				String current = str[1];
				int currentId = map.get(current);				
				Iterator<Integer> it = G.adj(currentId).iterator();
				List<Integer> adjList = Lists.newArrayList(it);
				
				if (adjList.size()==0){
					if(!installed.contains(currentId)) {
						System.out.println("    Installing "+ keys[currentId]);
						installed.add(currentId);
						continue;
					} else {
						System.out.println("    "+keys[currentId]+" is already installed");
						continue;
					}
					
				}
				else {
					Set<Integer> depSet = new HashSet<Integer>();
					for (int i : G.adj(currentId) ){
						depSet.add(i);
					}
					
					//now install the dependency Set in topological order if its not already installed
					for (int j: topological.order()) {
						if (depSet.contains(j) && !installed.contains(j)){
							System.out.println("    Installing "+ keys[j]);
							installed.add(j);
						}						
					}
					
					//now install the initially requested item
					System.out.println("    Installing "+ keys[currentId]);
					installed.add(currentId);
				}				
			} else if (str[0].equals("REMOVE")) {
				System.out.println(s);
				String current = str[1];
				int currentId = map.get(current);
				if(!installed.contains(currentId)) {
					System.out.println("    "+keys[currentId] + " is not installed");
					continue;
				} else if(usedByMap.containsKey(currentId)){
						List<Integer> componentsUsingCurrentId = usedByMap.get(currentId);
						if (componentsUsingCurrentId.size() > 0) {
							System.out.println("    " + keys[currentId]+ " is still needed");
						}
				} else if(dependencyMap.containsKey(currentId)){
						//component is not being used, remove it and check all dependencies again
					System.out.println("    Removing "+keys[currentId]);
					installed.remove(currentId);
					List<Integer> depsPulledByCurr = dependencyMap.get(currentId);
					for (int dep : depsPulledByCurr){
						if(usedByMap.containsKey(dep)){
							LinkedList<Integer> nestedDeps = (LinkedList<Integer>) usedByMap.get(dep);
							if (nestedDeps.contains(currentId)){
								nestedDeps.removeFirstOccurrence(currentId);
								usedByMap.put(dep, nestedDeps);
							}
							
							if (nestedDeps.size()==0){
								System.out.println("    Removing "+keys[dep]);
								installed.remove(dep);
								usedByMap.remove(dep);
								}
							}
						}
				} else {
					System.out.println("    Removing "+keys[currentId]);
					installed.remove(currentId);
				}
			}
			else if (str[0].equals("LIST")) {
				System.out.println(s);
				Iterator<Integer> it = installed.iterator();
				while (it.hasNext())
					System.out.println("    "+keys[it.next()]);	
			}else if (str[0].equals("END")){
				System.out.println("END");
			}		
		}
		
	}
	
	
	
	public static void main(String[] args){
		try {
			if(args.length > 0) {
				File file = new File(args[0]);
				DependencyManager myDg = new DependencyManager(file.toString(), "\\s+");
				myDg.generateOutput();
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

	}
}
