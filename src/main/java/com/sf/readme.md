To download dependencies and create package  
	`$ mvn clean dependency:copy-dependencies package`

To run Spreadsheet.java, from the top-level git-cloned directory  
    `$java -cp target/*:target/dependency/* com.sf.DependencyManager data/system_dependency_test.txt`