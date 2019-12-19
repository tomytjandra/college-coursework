<%@ include file = "../connect.jsp" %>

<%
	//Get parameter from insertGenre.jsp
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
		//Insert Genre Success
		String query = "INSERT INTO genre(GenreName) VALUES('"+name+"')";
		st.executeUpdate(query);

		//Redirect to manageGenre.jsp
		response.sendRedirect(request.getContextPath()+"/views/admin/manageGenre.jsp");
	}else{
		//Insert Genre Failed, passing error message
		response.sendRedirect(request.getContextPath()+"/views/admin/insertGenre.jsp?errName="+errName);
	}
%>