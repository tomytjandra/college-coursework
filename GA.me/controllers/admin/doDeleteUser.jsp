<%@ include file = "../connect.jsp" %>
<%
	//Get parameter from manageUser.jsp
	String userId = request.getParameter("userId");

	//Delete user based on userId
	String query = "DELETE FROM user WHERE UserId = "+userId;
	st.executeUpdate(query);

	//Redirect to manageUser.jsp
	response.sendRedirect(request.getContextPath()+"/views/admin/manageUser.jsp");
%>