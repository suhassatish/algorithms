package com.ge;

import static org.junit.Assert.*;

import org.junit.Test;

public class MetricsManagerTest {

	@Test
	public void metricsTest() {
		MetricsManager mm = new MetricsManager();
		MetricsData md = mm.getCurrentMetrics();
		assert(md.avg==0 && md.sum==0 && md.min==0 && md.max==0);		
		//System.out.println("avg = "+md.avg+"; sum="+md.sum+"; min="+md.min+"; max="+md.max);
		
		mm.recordData(-Integer.MIN_VALUE);
		assert(md.avg==-2147483648 && md.sum==-2147483648 && md.min==-2147483648 && md.max==-2147483648);
		//System.out.println("avg = "+md.avg+"; sum="+md.sum+"; min="+md.min+"; max="+md.max);
		
		mm.recordData(-Integer.MIN_VALUE);
		System.out.println("avg = "+md.avg+"; sum="+md.sum+"; min="+md.min+"; max="+md.max);
		
		//mm.recordData(Integer.MAX_VALUE);
		System.out.println("avg = "+md.avg+"; sum="+md.sum+"; min="+md.min+"; max="+md.max);
	}

}
