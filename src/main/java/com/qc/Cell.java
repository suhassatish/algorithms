package com.qc;

public class Cell {
	
	private double value;
	private String [] expression;	
	public Cell(String strId, String[] expression){
		this.expression = expression;
	}

	public double getValue() {
		return value;
	}
	public void setValue(double value) {
		this.value = value;
	}
	public String[] getExpression() {
		return expression;
	}
	public void setExpression(String[] expression) {
		this.expression = expression;
	}

}
