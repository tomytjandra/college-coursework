<%@ page import = "java.sql.*" %>

<%
	//Driver
	Class.forName("com.mysql.jdbc.Driver");

	//Connect to mysql database
	//parameter: "jdbc:mysql://localhost:[port]/[database name]", "[username]", "[password]"
	Connection connect = DriverManager.getConnection("jdbc:mysql://localhost:3306/gamedb", "root", "");
	Statement st = connect.createStatement();
%>