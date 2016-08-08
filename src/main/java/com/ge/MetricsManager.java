package com.ge;

import java.util.ArrayList;
import java.util.List;


public class MetricsManager {
	private MetricsData md;
    private List<Long> currentData;
    
    public MetricsManager(){
        md = new MetricsData();
        currentData = new ArrayList<Long>();
        md.sum = 0;
        md.avg = 0;
        md.min = 0;
        md.max = 0;
    }
	/**
	 * This method is invoked to record a new data point. 
	 * 
	 * @param data new data point
	 */
    
	public synchronized void recordData(int data) {
		currentData.add((long)data);
		if (md.sum == Integer.MAX_VALUE - data)
			throw new ArithmeticException("Data sum is about to overflow");
		md.sum += data;
		if (currentData.size() !=0){
			md.avg = md.sum/(currentData.size());
		}
		if (data < md.min) {
			md.min = data;
		}
		else if (data > md.max){
			md.max = data;
		}
        if (currentData.size()==1){
            md.min = data;
            md.max = data;
        }
	}
	
	/**
	 * This method returns an instance of MetricData to give a summary of the current state
	 */
	public MetricsData getCurrentMetrics() {
		return md;
	}
	
	/**
	 * This method resets the metrics. 
	 */
	public void resetMetrics() {				
		currentData.clear();
		md = new MetricsData();
        md.sum = 0;
        md.avg = 0;
        md.min = 0;
        md.max = 0;
	}
	
}
