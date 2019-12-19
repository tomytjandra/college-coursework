<%@ include file = "../connect.jsp" %>
<%
	//Get parameter from manageGenre.jsp
	String genreId = request.getParameter("genreId");

	//Delete genre based on genreId
	String query = "DELETE FROM genre WHERE GenreId = "+genreId;
	st.executeUpdate(query);

	//Redirect to manageGenre.jsp
	response.sendRedirect(request.getContextPath()+"/views/admin/manageGenre.jsp");
%>