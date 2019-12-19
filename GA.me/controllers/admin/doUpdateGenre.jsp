<%@ include file = "../connect.jsp" %>

<%
	//Get parameter from updateGenre.jsp
	String genreId = request.getParameter("genreId");
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
		//Update Genre Success
		String query = " UPDATE genre SET GenreName = '"+name+"' WHERE GenreId = "+genreId;
		st.executeUpdate(query);

		//Redirect to manageGenre.jsp
		response.sendRedirect(request.getContextPath()+"/views/admin/manageGenre.jsp");
	}else{
		//Update Genre Failed
		session.setAttribute("genreId", genreId); //so that genreId doesn't appear in url
		response.sendRedirect(request.getContextPath()+"/views/admin/updateGenre.jsp?errName="+errName);
	}
%>