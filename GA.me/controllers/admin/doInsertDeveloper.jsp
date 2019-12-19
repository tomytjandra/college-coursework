<%@ include file = "../connect.jsp" %>

<%
	//Get parameter from insertDeveloper.jsp
	String name = request.getParameter("txtName");

	//Initialize error message
	String errName = "";

	//Validation for name
	if(name.equals("")){
		errName = "Name must be filled";
	}else if(name.length() >= 20){
		errName = "Name length must be less than 20 characters";
	}

	if(errName == ""){
		//Insert Developer Success
		String query = "INSERT INTO developer(DeveloperName) VALUES('"+name+"')";
		st.executeUpdate(query);

		//Redirect to manageDeveloper.jsp
		response.sendRedirect(request.getContextPath()+"/views/admin/manageDeveloper.jsp");
	}else{
		//Insert Developer Failed, passing error message
		response.sendRedirect(request.getContextPath()+"/views/admin/insertDeveloper.jsp?errName="+errName);
	}
%>