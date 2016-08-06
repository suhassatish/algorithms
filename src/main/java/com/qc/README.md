//To download dependencies and create package
mvn clean dependency:copy-dependencies package

//To run Spreadsheet.java, from the top-level git-cloned directory
java -cp target/algorithms-1.0-SNAPSHOT.jar:target/dependency/google-collections-1.0.jar:target/dependency/algorithms-4.0.1.jar:target/dependency/stdlib-1.0.1.jar: com.qc.Spreadsheet data/spreadsheet/spreadsheet.txt
