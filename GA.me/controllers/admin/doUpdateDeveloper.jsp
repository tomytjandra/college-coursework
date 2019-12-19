<%@ include file = "../connect.jsp" %>

<%
	//Get parameter from updateDeveloper.jsp
	String developerId = request.getParameter("developerId");
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
		//Update Developer Success
		String query = " UPDATE developer SET DeveloperName = '"+name+"' WHERE DeveloperId = "+developerId;
		st.executeUpdate(query);

		//Redirect to manageDeveloper.jsp
		response.sendRedirect(request.getContextPath()+"/views/admin/manageDeveloper.jsp");
	}else{
		//Update Developer Failed, passing error message
		session.setAttribute("developerId", developerId); //so that developerId doesn't appear in url
		response.sendRedirect(request.getContextPath()+"/views/admin/updateDeveloper.jsp?errName="+errName);
	}
%>