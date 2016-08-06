package com.qc;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;

import java.util.Set;
import java.util.Stack;

import com.google.common.collect.HashMultimap;
import com.google.common.collect.Multimap;
import com.google.common.collect.Sets;

import edu.princeton.cs.algorithms.Digraph;
import edu.princeton.cs.algorithms.Topological;
import edu.princeton.cs.introcs.In;
import java.io.File;

/*
 * Solution submitted by Suhas Satish
 */
public class Spreadsheet {
	private int numRows;
	private int numColumns;
	private String inputFile;
	private String inputDelimiter; 
	private Multimap<String,String> dependencyMap;
	private Digraph cellDependencyGraph;
	private Digraph reverseDependencyGraph;
	private List<Cell> cells;	
	private Topological computeOrder;
	
	public Spreadsheet(String filename, String delimiter) throws Exception {
		this.inputFile = filename;
		this.inputDelimiter = delimiter;
		
		//create dependency Graph & cells and detects cycle
		createDependencyGraph(this.inputFile);		
		computeValues();
	}	
	
	/**
	 * 
	 * @param eg: strId= B7 => returns index as (14-1) 
	 * @return  returns the integer index, return value of -1 indicates error in input argument
	 */
	private int getCellIndex(String strId){
		if (!strId.matches("[A-Z]\\d+"))
			return -1;
		int rowIntId = strId.charAt(0) - 'A';
		int colId = Integer.parseInt(strId.substring(1));
		return (Math.max(rowIntId*numColumns + colId -1,0));
	}
	
	private void createDependencyGraph(String inputFile) throws Exception {
		try {
			createDependencyMap(inputFile);
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		//from the MultiMap create DirectedGraph, detect cycles and if none, evaluate expressions 
		//in reverse Topological Sort order
		Collection<String> values = dependencyMap.values();
		Set<String> valueSet = new HashSet<String>(values);
		int numVertices	= Sets.union(dependencyMap.keySet(), valueSet).size();
		cellDependencyGraph = new Digraph(numVertices);
		for (String key : dependencyMap.keySet()) {
			Set<String> dependencies = (Set<String>) dependencyMap.get(key);
			for (String dependency : dependencies) {
				cellDependencyGraph.addEdge(getCellIndex(key), getCellIndex(dependency));
			}			
		}
		reverseDependencyGraph = cellDependencyGraph.reverse();
		computeOrder = new Topological(reverseDependencyGraph);
		if (!computeOrder.hasOrder()) {
			throw new Exception("Cycle detected in excel cell dependencies");
		}
	}


	private void createDependencyMap(String inputFile) throws Exception {
		if (inputFile == null) 
			throw new Exception("Invalid input file");
		In in = new In(inputFile);				 
		//get size of sheet which is expected to be the first entry in spreadsheet.txt (precondition)
		if(in.hasNextLine()){			
			String[] dimensions = in.readLine().split(this.inputDelimiter);
			this.numColumns = Integer.parseInt(dimensions[0]);
			this.numRows = Integer.parseInt(dimensions[1]);
			this.cells = new ArrayList<Cell>(this.numRows*this.numColumns);			
			this.dependencyMap = HashMultimap.create();
		}
		String pattern = "[A-Z]\\d+";	//eg: cell = C98
		for (int i=0;i<numRows;i++){
			for (int j=1;j<=numColumns;j++){
				String currCellStrId = Character.toString((char) ('A'+i)) + Integer.toString(j) ;
				String[] expression = in.readLine().split(this.inputDelimiter);
				Cell cell = new Cell(currCellStrId, expression);
				
				
				boolean hasDependency = false; 
				for (String s : expression) {					
					if (s.matches(pattern)){
						dependencyMap.put(currCellStrId, s);
						hasDependency = true;
					}
				}
				if (!hasDependency){
					double cellValue = evaluateExpression(expression, false);
					cell.setValue(cellValue);
				}
				cells.add(cell);				
			}			
		}		
	}
	
	private double evaluateExpression(String[] expression, boolean hasVariables) {
		// TODO Auto-generated method stub
		if (expression == null) throw new NullPointerException("Expression is null");
		
		if (expression.length==0) throw new RuntimeException("Input line for a cell is blank");
		
		if (expression.length==1 && !hasVariables)
			return Double.parseDouble(expression[0]);
		else if (expression.length==1 && hasVariables) {
			//precondition is that the variable cell value  has been computed before by 
			//topological order calculation
			int cellIndex = getCellIndex(expression[0]);
			return cells.get(cellIndex).getValue();
		}
		else {
			Stack<Double> operandStack = new Stack<Double>();						
			for (String op : expression){
				if (!op.matches("[-+/*]")){
					if (!op.matches("[A-Z]\\d+"))							
						operandStack.push(Double.parseDouble(op));
					else {
						//variable detected
						double variableCellValue = cells.get(getCellIndex(op)).getValue();
						operandStack.push(variableCellValue);
					}
						
				}
				else {
					double op1 = operandStack.pop();
					double op2 = operandStack.pop();
					char operation = op.charAt(0);
					switch (operation){
						case '+': 
							operandStack.push(op2+op1);
							break;
						case '-': 
							operandStack.push(op2-op1);	
							break;
						case '*':
							operandStack.push(op2*op1);	
							break;
						case '/': 
							operandStack.push(op2/op1);	
							break;
						default: 
							throw new RuntimeException("Invalid operation attempted, only +,-,*,/ " +
									"are currently supported");
					}
						
				}
			}
			return operandStack.pop();			
		}			
	}

	private void computeValues(){
		for (int index : computeOrder.order()){
			Cell cell = cells.get(index);
			double value = cell.getValue();
			if (value == 0.0){
				String [] expr = cell.getExpression();
				boolean hasVariable=false;
				if (expr.length ==1) {
					if (expr[0].matches("[A-Z]\\d+")) {
						hasVariable = true;
					}
				}				
				cell.setValue(evaluateExpression(cell.getExpression(), hasVariable));
			}			
		}
	}
	
	public void printOutput() {
		System.out.println(numColumns+ " "+numRows);
		for (int i=0; i< cells.size(); i++){
			System.out.println(String.format("%.5f", cells.get(i).getValue()));
		}
	}
	
	public static void main(String[] args){
		try {
			//Spreadsheet sheet = new Spreadsheet("spreadsheet.txt", "\\s+");
			//sheet.printOutput();
			
			//Spreadsheet sheet2 = new Spreadsheet("spreadsheet_cycle.txt", "\\s+");
			//sheet2.printOutput();
            if(args.length > 0) {
                File file = new File(args[0]);
                Spreadsheet sheet3 = new Spreadsheet(file.toString(), "\\s+");
                sheet3.printOutput();
                // Work with your 'file' object here
            }

			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			System.out.println("Cycle exists in spreadsheet dependencies, please correct and re-try");
			e.printStackTrace();
		}
		
	}


}
