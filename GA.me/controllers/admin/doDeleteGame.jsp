<%@ include file = "../connect.jsp" %>
<%
	//Get parameter from manageGame.jsp
	String gameId = request.getParameter("gameId");

	//Delete game based on gameId
	String query = "DELETE FROM game WHERE GameId = "+gameId;
	st.executeUpdate(query);

	//Redirect to manageGame.jsp
	response.sendRedirect(request.getContextPath()+"/views/admin/manageGame.jsp");
%>